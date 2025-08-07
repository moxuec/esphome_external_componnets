import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, i2c
from esphome.const import (
    CONF_ID,
    DEVICE_CLASS_VOLUME_FLOW_RATE,
)

CODEOWNERS = ["@synodriver"]
DEPENDENCIES = ["i2c"]

afs01 = cg.esphome_ns.namespace("afs01")
AFS01Component = afs01.class_("AFS01Component", cg.PollingComponent, i2c.I2CDevice)

CONF_VOLUME_FLOW_RATE = "volume_flow_rate"
UNIT_CUBIC_CENTIMETER_PER_MINUTE = "cm³/min"

CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(AFS01Component),
            cv.Optional(CONF_VOLUME_FLOW_RATE): sensor.sensor_schema(
                unit_of_measurement=UNIT_CUBIC_CENTIMETER_PER_MINUTE,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_VOLUME_FLOW_RATE,
            ),
        }
    )
    .extend(cv.polling_component_schema("20s"))
    .extend(i2c.i2c_device_schema(0x40)),
)

FINAL_VALIDATE_SCHEMA = i2c.final_validate_device_schema("afs01", max_frequency="100khz")


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)

    if CONF_VOLUME_FLOW_RATE in config:
        sens = await sensor.new_sensor(config[CONF_VOLUME_FLOW_RATE])
        cg.add(var.set_volume_flow_rate_sensor(sens))


