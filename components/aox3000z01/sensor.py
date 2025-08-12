import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, uart
from esphome.const import (
    CONF_ID,
    STATE_CLASS_MEASUREMENT,
    UNIT_PERCENT
)

CODEOWNERS = ["@synodriver"]
DEPENDENCIES = ["uart"]

aox3000z01 = cg.esphome_ns.namespace("aox3000z01")
AOX3000Z01Component = aox3000z01.class_("AOX3000Z01Component", cg.PollingComponent, uart.UARTDevice)

CONF_O2 = "O2"
ICON_LEAF = "mdi:leaf"

CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(AOX3000Z01Component),
            cv.Optional(CONF_O2): sensor.sensor_schema(
                unit_of_measurement=UNIT_PERCENT,
                icon=ICON_LEAF,
                accuracy_decimals=1,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
        }
    )
    .extend(cv.polling_component_schema("20s"))
    .extend(uart.UART_DEVICE_SCHEMA)
)

FINAL_VALIDATE_SCHEMA = uart.final_validate_device_schema("aox3000z01", baud_rate=2400)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    if CONF_O2 in config:
        sens = await sensor.new_sensor(config[CONF_O2])
        cg.add(var.set_o2_sensor(sens))