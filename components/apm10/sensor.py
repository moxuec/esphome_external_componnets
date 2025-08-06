import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, i2c
from esphome.const import (
    CONF_ID,
    CONF_PM_1_0,
    CONF_PM_2_5,
    CONF_PM_10_0,
    CONF_TYPE,
    STATE_CLASS_MEASUREMENT,
    UNIT_MICROGRAMS_PER_CUBIC_METER,
    ICON_CHEMICAL_WEAPON,
    DEVICE_CLASS_PM1,
    DEVICE_CLASS_PM25,
    DEVICE_CLASS_PM10, CONF_PM_4_0,
)

CODEOWNERS = ["@synodriver"]
DEPENDENCIES = ["i2c"]

apm10 = cg.esphome_ns.namespace("apm10")
APM10Component = apm10.class_("APM10Component", cg.PollingComponent, i2c.I2CDevice)

APM10_TYPE = apm10.enum("APM10_TYPE")
APM10_TYPE_OPTIONS = {
    "apm10": APM10_TYPE.APM10_TYPE_10,
    "apm3000": APM10_TYPE.APM10_TYPE_3000,
}

def validate_config(config):
    type_ = config[CONF_TYPE]
    if type_ == "apm10" and CONF_PM_4_0 in config:
        raise cv.Invalid(
            "PM 4.0 sensor is not supported for APM10 or APM2000, please use APM3000 instead."
        )
    return config


CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(APM10Component),
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
            cv.Optional(CONF_TYPE, default="apm10"): cv.enum(APM10_TYPE_OPTIONS),
        }
    )
    .extend(cv.polling_component_schema("20s"))
    .extend(i2c.i2c_device_schema(0x08)),
    validate_config,
)

FINAL_VALIDATE_SCHEMA = i2c.final_validate_device_schema("apm10", max_frequency="100khz")


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)

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
    cg.add(var.set_type(config[CONF_TYPE]))

