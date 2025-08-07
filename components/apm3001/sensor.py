import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, uart
from esphome.const import (
    CONF_ID,
    CONF_PM_2_5,
    CONF_PM_4_0,
    UNIT_MICROGRAMS_PER_CUBIC_METER,
    DEVICE_CLASS_PM25,
    STATE_CLASS_MEASUREMENT,
    ICON_CHEMICAL_WEAPON,
    CONF_PM_1_0,
    DEVICE_CLASS_PM1,
    CONF_PM_10_0,
    DEVICE_CLASS_PM10,
)

CODEOWNERS = ["@synodriver"]
DEPENDENCIES = ["uart"]

apm3001 = cg.esphome_ns.namespace("apm3001")
APM3001Component = apm3001.class_("APM3001Component", cg.PollingComponent, uart.UARTDevice)

CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(APM3001Component),
            cv.Optional(CONF_PM_1_0): sensor.sensor_schema(
                unit_of_measurement=UNIT_MICROGRAMS_PER_CUBIC_METER,
                icon=ICON_CHEMICAL_WEAPON,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_PM1,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_PM_2_5): sensor.sensor_schema(
                unit_of_measurement=UNIT_MICROGRAMS_PER_CUBIC_METER,
                icon=ICON_CHEMICAL_WEAPON,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_PM25,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_PM_4_0): sensor.sensor_schema(
                unit_of_measurement=UNIT_MICROGRAMS_PER_CUBIC_METER,
                icon=ICON_CHEMICAL_WEAPON,
                accuracy_decimals=0,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_PM_10_0): sensor.sensor_schema(
                unit_of_measurement=UNIT_MICROGRAMS_PER_CUBIC_METER,
                icon=ICON_CHEMICAL_WEAPON,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_PM10,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
        }
    )
    .extend(cv.polling_component_schema("20s"))
    .extend(uart.UART_DEVICE_SCHEMA)
)

FINAL_VALIDATE_SCHEMA = uart.final_validate_device_schema("apm3001", baud_rate=9600, data_bits=8, stop_bits=1, parity=None)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    if CONF_PM_1_0 in config:
        sens = await sensor.new_sensor(config[CONF_PM_1_0])
        cg.add(var.set_pm1_sensor(sens))
    if CONF_PM_2_5 in config:
        sens = await sensor.new_sensor(config[CONF_PM_2_5])
        cg.add(var.set_pm2_5_sensor(sens))
    if CONF_PM_4_0 in config:
        sens = await sensor.new_sensor(config[CONF_PM_4_0])
        cg.add(var.set_pm4_sensor(sens))
    if CONF_PM_10_0 in config:
        sens = await sensor.new_sensor(config[CONF_PM_10_0])
        cg.add(var.set_pm10_sensor(sens))

