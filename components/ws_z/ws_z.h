#pragma once

#include "esphome/core/component.h"
#include "esphome/core/automation.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/uart/uart.h"

namespace esphome {
namespace ws_z {

//enum DARTABCLogic { DART_ABC_NONE = 0, DART_ABC_ENABLED, DART_ABC_DISABLED };
#define SB1_BUFFER_LEN   6     // Length of serial buffer for header + type + length

class DARTWSZComponent : public PollingComponent, public uart::UARTDevice {
 public:
  DARTWSZComponent() = default;
  void setup() override;
  float get_setup_priority() const override;
  void update() override;
  void dump_config() override;
  void set_formaldehyde_sensor(sensor::Sensor *formaldehyde_sensor)  { formaldehyde_sensor_ = formaldehyde_sensor; }
  void set_formaldehyde_ppb_sensor(sensor::Sensor *formaldehyde_ppb_sensor) { formaldehyde_ppb_sensor_ = formaldehyde_ppb_sensor; }

 
 protected:
  uint8_t uart_buffer_[SB1_BUFFER_LEN]{0};
  bool dart_write_command_(const uint8_t *command, uint8_t *response);
  sensor::Sensor *formaldehyde_sensor_{nullptr};
  sensor::Sensor *formaldehyde_ppb_sensor_{nullptr};
  
};


}  // namespace dart
}  // namespace esphome