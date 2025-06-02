# external components for esphome

- 1 dart ws-z sensor
- 2 ltr390 with ```sensitivity_max``` variable，default 1400 for new version

```yaml
uart:
  id: uart_bus
  tx_pin: 17
  rx_pin: 16
  baud_rate: 9600
  stop_bits: 1
  rx_buffer_size: 512

i2c:
  sda: 18
  scl: 19
  scan: true
  id: i2cbus

sensor:
  - platform: ws_z
    uart_id: uart_bus
    formaldehyde:
      name: "甲醛"
    formaldehyde_ppb:
      name: "甲醛ppb"
    update_interval: 5s

  - platform: newltr390
    i2c_id: i2cbus
    uv_index:
      name: "UV Index"
    uv:
      name: "UV Sensor Counts"
    light:
      name: "Light"
    ambient_light:
      name: "Light Sensor Counts"
    sensitivity_max: 1400
```