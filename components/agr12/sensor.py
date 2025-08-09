import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, i2c
from esphome.const import (
    STATE_CLASS_MEASUREMENT,
    CONF_ID, CONF_PRESSURE, DEVICE_CLASS_PRESSURE, CONF_TYPE,
)

CODEOWNERS = ["@synodriver"]
DEPENDENCIES = ["i2c"]

agr12 = cg.esphome_ns.namespace("agr12")
AGR12Component = agr12.class_("AGR12Component", cg.PollingComponent, i2c.I2CDevice)

AGR_TYPE = agr12.enum("AGR_TYPE")
AGR_TYPE_OPTIONS = {
    "agr12": AGR_TYPE.AGR12,
    "apr5852": AGR_TYPE.APR5852
}

UNIT_KPASCAL = "kPa"

CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(AGR12Component),
            cv.Optional(CONF_PRESSURE): sensor.sensor_schema(
                unit_of_measurement=UNIT_KPASCAL,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_PRESSURE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_TYPE, default="agr12"): cv.enum(AGR_TYPE_OPTIONS),
        }
    )
    .extend(cv.polling_component_schema("20s"))
    .extend(i2c.i2c_device_schema(0x50)),
)

FINAL_VALIDATE_SCHEMA = i2c.final_validate_device_schema("agr12", max_frequency="100khz")


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)

    if CONF_PRESSURE in config:
        sens = await sensor.new_sensor(config[CONF_PRESSURE])
        cg.add(var.set_pressure_sensor(sens))
    cg.add(var.set_type(config[CONF_TYPE]))
