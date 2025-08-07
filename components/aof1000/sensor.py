import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, uart
from esphome.const import (
    CONF_ID,
    STATE_CLASS_MEASUREMENT,
    CONF_TEMPERATURE,
    DEVICE_CLASS_VOLUME_FLOW_RATE, UNIT_PERCENT, UNIT_CELSIUS, ICON_THERMOMETER, DEVICE_CLASS_TEMPERATURE
)

CODEOWNERS = ["@synodriver"]
DEPENDENCIES = ["uart"]

aof1000 = cg.esphome_ns.namespace("aof1000")
AOF1000Component = aof1000.class_("AOF1000Component", cg.PollingComponent, uart.UARTDevice)

CONF_O2 = "O2"
CONF_VOLUME_FLOW_RATE = "volume_flow_rate"
ICON_LEAF = "mdi:leaf"
UNIT_L_PER_MINUTE  = "L/min"

CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(AOF1000Component),
            cv.Optional(CONF_O2): sensor.sensor_schema(
                unit_of_measurement=UNIT_PERCENT,
                icon=ICON_LEAF,
                accuracy_decimals=1,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_VOLUME_FLOW_RATE): sensor.sensor_schema(
                unit_of_measurement=UNIT_L_PER_MINUTE,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_VOLUME_FLOW_RATE,
            ),
            cv.Optional(CONF_TEMPERATURE): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                icon=ICON_THERMOMETER,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
            )
        }
    )
    .extend(cv.polling_component_schema("20s"))
    .extend(uart.UART_DEVICE_SCHEMA)
)

FINAL_VALIDATE_SCHEMA = uart.final_validate_device_schema("aof1000", baud_rate=9600)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    if CONF_O2 in config:
        sens = await sensor.new_sensor(config[CONF_O2])
        cg.add(var.set_o2_sensor(sens))
    if CONF_VOLUME_FLOW_RATE in config:
        sens = await sensor.new_sensor(config[CONF_VOLUME_FLOW_RATE])
        cg.add(var.set_volume_flow_rate_sensor(sens))
    if CONF_TEMPERATURE in config:
        sens = await sensor.new_sensor(config[CONF_TEMPERATURE])
        cg.add(var.set_temperature_sensor(sens))
