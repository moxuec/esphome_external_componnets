import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, uart
from esphome.const import (
    CONF_ID,
    CONF_FORMALDEHYDE,
    CONF_UPDATE_INTERVAL,
CONF_MODE,
    UNIT_MICROGRAMS_PER_CUBIC_METER,
    UNIT_PARTS_PER_BILLION,
    ICON_CHEMICAL_WEAPON,
	STATE_CLASS_MEASUREMENT,
)
CONF_FORMALDEHYDE_PPB = "formaldehyde_ppb"


DEPENDENCIES = ["uart"]

dart_ns = cg.esphome_ns.namespace("ws_z")
DARTWSZComponent = dart_ns.class_("DARTWSZComponent", cg.PollingComponent, uart.UARTDevice)
DARTWS_MODE = dart_ns.enum("DARTWS_MODE")
DARTWS_MODE_OPTIONS = {
    "passive": DARTWS_MODE.DARTWS_MODE_PASSIVE,
    "active": DARTWS_MODE.DARTWS_MODE_ACTIVE,
}

CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(DARTWSZComponent),
            cv.Optional(CONF_FORMALDEHYDE): sensor.sensor_schema(
                unit_of_measurement=UNIT_MICROGRAMS_PER_CUBIC_METER,
                icon=ICON_CHEMICAL_WEAPON,
                accuracy_decimals=0,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_FORMALDEHYDE_PPB): sensor.sensor_schema(
                unit_of_measurement=UNIT_PARTS_PER_BILLION,
                icon=ICON_CHEMICAL_WEAPON,
                accuracy_decimals=0,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_MODE, default="passive"): cv.enum(DARTWS_MODE_OPTIONS),
		}
    )
    .extend(cv.polling_component_schema("20s"))
    .extend(uart.UART_DEVICE_SCHEMA)
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    if CONF_FORMALDEHYDE in config:
        sens = await sensor.new_sensor(config[CONF_FORMALDEHYDE])
        cg.add(var.set_formaldehyde_sensor(sens))
    if CONF_FORMALDEHYDE_PPB in config:
        sens = await sensor.new_sensor(config[CONF_FORMALDEHYDE_PPB])
        cg.add(var.set_formaldehyde_ppb_sensor(sens))
    cg.add(var.set_mode(config[CONF_MODE]))
    # if CONF_UPDATE_INTERVAL in config:
    #     cg.add(var.set_update_interval(config[CONF_UPDATE_INTERVAL]))