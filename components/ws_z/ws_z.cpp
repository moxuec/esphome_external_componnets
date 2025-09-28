#include "ws_z.h"
#include "esphome/core/log.h"

namespace esphome {
namespace ws_z {

static const char *const TAG = "dart_ws_z";
static const uint8_t DART_REQUEST_LENGTH = 8;
static const uint8_t DART_RESPONSE_LENGTH = 9;
// static const uint8_t DART_COMMAND_GET_PPM[] = {0xFF,0x01,0x86,0x00,0x00,0x00,0x00,0x00,0x79};//问答模式下，请求发送
// static const uint8_t DART_COMMAND_SET_QA[]  = {0xFF,0x01,0x78,0x41,0x00,0x00,0x00,0x00,0x46};//切换到问答模式
// static const uint8_t DART_COMMAND_SET_NQA[]  = {0xFF,0x01,0x78,0x40,0x00,0x00,0x00,0x00,0x47};//切换到主动上传模式

static const uint8_t DART_COMMAND_GET_PPM[] = {0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00};  // 问答模式下，请求发送
static const uint8_t DART_COMMAND_SET_QA[] = {0xFF, 0x01, 0x78, 0x41, 0x00, 0x00, 0x00, 0x00};  // 切换到问答模式
static const uint8_t DART_COMMAND_SET_NQA[] = {0xFF, 0x01, 0x78, 0x40, 0x00, 0x00, 0x00, 0x00};  // 切换到主动上传模式

uint8_t dart_checksum(const uint8_t *command) {
  uint8_t sum = 0;
  // datasheet 算法：sum bytes[1..7], 然后取反 + 1
  for (uint8_t i = 1; i < DART_REQUEST_LENGTH; i++) {
    sum += command[i];
  }
  sum = (~sum) + 1;
  return sum;
}

void DARTWSZComponent::setup() {
  uint8_t response[DART_RESPONSE_LENGTH];

  if (this->mode_ == DARTWS_MODE_PASSIVE) {
    // 切到问答（被动）模式，等待一次响应确认
    if (!this->dart_write_command_(DART_COMMAND_SET_QA, response)) {
      ESP_LOGW(TAG, "Setting DART WS-Z to QA (passive) mode failed!");
      this->status_set_warning();
      return;
    } else {
      ESP_LOGD(TAG, "DART WS-Z set to QA (passive) mode.");
      this->status_clear_warning();
    }
  } else {  // ACTIVE
    // 切到主动上传模式（不需要等待返包，但是要发送命令并清空串口缓存）
    if (!this->dart_write_command_(DART_COMMAND_SET_NQA, nullptr)) {
      ESP_LOGW(TAG, "Setting DART WS-Z to NQA (active) mode failed!");
      this->status_set_warning();
      // don't return here — 仍然可以尝试处理来着主动上报的包
    } else {
      ESP_LOGD(TAG, "DART WS-Z set to NQA (active) mode.");
      this->status_clear_warning();
    }
    // 给模块一些时间切换并开始上报（短延时）
    delay(200);
    // 丢弃 RX buffer 的残留数据，保证后续读取的是新帧
    while (this->available()) {
      this->read();
    }
  }
}

void DARTWSZComponent::update() {
  if (this->mode_ == DARTWS_MODE_PASSIVE) {
    uint8_t response[DART_RESPONSE_LENGTH];
    if (!this->dart_write_command_(DART_COMMAND_GET_PPM, response)) {
      ESP_LOGW(TAG, "Reading data from DART WS-Z failed!");
      this->status_set_warning();
      return;
    }

    if (response[0] != 0xFF || response[1] != 0x86) {
      ESP_LOGW(TAG, "Invalid preamble from DART WS-Z!");
      this->status_set_warning();
      return;
    }

    uint8_t checksum = dart_checksum(response);
    if (response[8] != checksum) {
      ESP_LOGW(TAG, "DART WS-Z Checksum doesn't match: 0x%02X!=0x%02X", response[8], checksum);
      this->status_set_warning();
      return;
    }

    this->status_clear_warning();
    const uint16_t ch2oh_mg = uint16_t(response[2]) * 256 + response[3];
    const uint16_t ch20h_ppb = uint16_t(response[6]) * 256 + response[7];

    ESP_LOGD(TAG, "DART WS-Z Received HCHO=%u µg/m³, %u ppb, %02X %02X %02X %02X %02X %02X %02X %02X %02X",
             ch2oh_mg, ch20h_ppb,
             response[0], response[1], response[2], response[3], response[4], response[5], response[6], response[7],
             response[8]);
    if (this->formaldehyde_sensor_ != nullptr) {
      this->formaldehyde_sensor_->publish_state(ch2oh_mg);
    }
    if (this->formaldehyde_ppb_sensor_ != nullptr) {
      this->formaldehyde_ppb_sensor_->publish_state(ch20h_ppb);
    }
  }
}

void DARTWSZComponent::loop() {
  if (this->mode_ == DARTWS_MODE_ACTIVE) {
    while (this->available()) {
      uint8_t c;
      if (!this->read_byte(&c)) {
        return;
      }
      // 寻找 0xFF 帧头
      if (c != 0xFF) {
        continue;
      }

      // 找到帧头后，读取后续的8个字节数据
      uint8_t data[8];
      if (!this->read_array(data, 8)) {
        return;
      }

      // 校验和检查：对 data[0..7] 求和（包含 checksum），如果和 != 0 说明校验失败
      uint8_t sum = 0;
      for (int i = 0; i < 8; i++) {
        sum += data[i];
      }

      if (sum != 0) {
        // 校验失败的数据包直接丢弃
        ESP_LOGW(TAG, "Checksum failed! Discarding packet. Sum: 0x%02X", sum);
        continue;
      }

      // 兼容两种常见的主动上报帧格式：
      // 1) 被动/问答风格（第二字节 0x86）：格式与被动响应相同，只不过是主动发送
      //    在这里 data[0] == 0x86，此时对应被动响应中的 response[1]，index 映射如下：
      //    response[2] -> data[1], response[3] -> data[2]
      //    response[6] -> data[5], response[7] -> data[6]
      // 2) ID=0x17 + unit=0x04 风格：按照原来实现解析 data[3], data[4]
      if (data[0] == 0x86) {
        // 解析与被动响应相同
        uint16_t ugm3 = (uint16_t(data[1]) << 8) | uint16_t(data[2]);   // response[2,3]
        uint16_t ppb = (uint16_t(data[5]) << 8) | uint16_t(data[6]);    // response[6,7]

        ESP_LOGD(TAG, "Active frame (86-style) Received HCHO=%u µg/m³, %u ppb", ugm3, ppb);
        if (this->formaldehyde_sensor_ != nullptr) {
          this->formaldehyde_sensor_->publish_state(ugm3);
        }
        if (this->formaldehyde_ppb_sensor_ != nullptr) {
          this->formaldehyde_ppb_sensor_->publish_state(ppb);
        }
      } else if (data[0] == 0x17 && data[1] == 0x04) {
        // 原有的 ID/Unit 风格（保留）
        uint32_t val = (uint32_t(data[3]) << 8) | uint32_t(data[4]);
        ESP_LOGD(TAG, "Active frame (17-style) Received HCHO ppb=%u", val);
        if (this->formaldehyde_ppb_sensor_ != nullptr) {
          this->formaldehyde_ppb_sensor_->publish_state(val);
        }
      } else {
        // 未知格式：打印全部字节，便于调试真实设备上报的内容
        ESP_LOGW(TAG, "Ignoring frame with unknown ID/Unit. ID: 0x%02X, Unit: 0x%02X (raw: %02X %02X %02X %02X %02X %02X %02X %02X)",
                 data[0], data[1],
                 data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]);
      }
    }
  }
}


bool DARTWSZComponent::dart_write_command_(const uint8_t *command, uint8_t *response) {
  // Empty RX Buffer
  while (this->available()) {
    this->read();
  }
  this->write_array(command, DART_REQUEST_LENGTH);
  this->write_byte(dart_checksum(command));
  this->flush();
  if (response == nullptr)
    return true;

  return this->read_array(response, DART_RESPONSE_LENGTH);
}

float DARTWSZComponent::get_setup_priority() const { return setup_priority::DATA; }

void DARTWSZComponent::dump_config() {
  ESP_LOGCONFIG(TAG, "DART WS-Z:");
  LOG_SENSOR("  ", "HCHO ", this->formaldehyde_sensor_);
  LOG_SENSOR("  ", "HCHO PPB", this->formaldehyde_ppb_sensor_);
  this->check_uart_settings(9600);
}

}  // namespace ws_z
}  // namespace esphome
