#pragma once

#include "esphome/core/component.h"
#include "esphome/core/automation.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/uart/uart.h"

namespace esphome {
namespace kanfurco2 {

//enum DARTABCLogic { DART_ABC_NONE = 0, DART_ABC_ENABLED, DART_ABC_DISABLED };
#define SB1_BUFFER_LEN   6     // Length of serial buffer for header + type + length

class KANFURCO2Component : public PollingComponent, public uart::UARTDevice {
 public:
  void setup() override;
  float get_setup_priority() const override;
  void update() override;
  void dump_config() override;
  void set_co2_sensor(sensor::Sensor *co2_sensor)  { co2_sensor_ = co2_sensor; }
  void set_self_calibrate(bool b) {self_calibrate = b;}
  void set_period(uint8_t p) { period = p;}
  void set_base(uint16_t b) {base = b;}
  void calibrate(uint16_t data);
  optional<std::string> version();
  void toggle_self_calibrate(bool open, uint8_t period, uint16_t base);
  optional<std::string> sn();
 protected:
  bool self_calibrate;
  uint8_t period;
  uint16_t base;
  optional<uint32_t> read_co2();
  bool write_command(uint8_t command, const uint8_t *data, uint8_t data_size, uint8_t *response_buf);
  sensor::Sensor *co2_sensor_{nullptr};
  
};

//template<typename... Ts> class ToggleSelfCalibrateAction : public Action<Ts...> {
// public:
//  ToggleSelfCalibrateAction(KANFURCO2Component *kanfurco2) : kanfurco2_(kanfurco2) {}
//
//  void play(Ts... x) override { this->kanfurco2_->toggle_self_calibrate(x...); }
//
// protected:
//  KANFURCO2Component *kanfurco2_;
//};

}  // namespace kanfurco2
}  // namespace esphome