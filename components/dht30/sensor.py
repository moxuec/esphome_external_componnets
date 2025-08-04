from esphome import automation
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, i2c
from esphome.const import (
    STATE_CLASS_MEASUREMENT,
    CONF_TEMPERATURE,
    UNIT_CELSIUS,
    ICON_THERMOMETER,
    DEVICE_CLASS_TEMPERATURE,
    CONF_HUMIDITY,
    UNIT_PERCENT,
    ICON_WATER_PERCENT,
    DEVICE_CLASS_HUMIDITY, CONF_ID,
)

CODEOWNERS = ["@synodriver"]
DEPENDENCIES = ["i2c"]

dht30 = cg.esphome_ns.namespace("dht30")
DHT30Component = dht30.class_("DHT30Component", cg.PollingComponent, i2c.I2CDevice)

CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(DHT30Component),
            cv.Optional(CONF_TEMPERATURE): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                icon=ICON_THERMOMETER,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_HUMIDITY): sensor.sensor_schema(
                unit_of_measurement=UNIT_PERCENT,
                icon=ICON_WATER_PERCENT,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_HUMIDITY,
                state_class=STATE_CLASS_MEASUREMENT,
            )}
    )
    .extend(cv.polling_component_schema("20s"))
    .extend(i2c.i2c_device_schema(0x38)),
)

FINAL_VALIDATE_SCHEMA = i2c.final_validate_device_schema("dht30", max_frequency="400khz")

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)

    if CONF_TEMPERATURE in config:
        sens = await sensor.new_sensor(config[CONF_TEMPERATURE])
        cg.add(var.set_temperature_sensor(sens))
    if CONF_HUMIDITY in config:
        sens = await sensor.new_sensor(config[CONF_HUMIDITY])
        cg.add(var.set_humidity_sensor(sens))
