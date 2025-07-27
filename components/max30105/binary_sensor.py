import esphome.codegen as cg
from esphome.const import DEVICE_CLASS_POWER, DEVICE_CLASS_EMPTY
from esphome.components import binary_sensor
import esphome.config_validation as cv
from esphome.const import (
    CONF_HAS_TARGET,
    DEVICE_CLASS_PRESENCE,
    ICON_MOTION_SENSOR,
    ICON_POWER, ICON_LIGHTBULB, DEVICE_CLASS_LIGHT, ICON_COUNTER,
)

from . import CONF_MAX30105_ID, MAX30105Component, CONF_DATA_READY, CONF_ALC_OVERFLOW, CONF_TEMPERATURE_READY

DEPENDENCIES = ["max30105"]
CONF_POWER_READY = "power_ready"
CONF_FIFO_FULL = "fifo_full"

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_MAX30105_ID): cv.use_id(MAX30105Component),
    cv.Optional(CONF_POWER_READY): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_POWER,
        icon=ICON_POWER,
    ),
    cv.Optional(CONF_HAS_TARGET): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_PRESENCE,
        icon=ICON_MOTION_SENSOR,
    ),
    cv.Optional(CONF_ALC_OVERFLOW): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_LIGHT,
        icon=ICON_LIGHTBULB,
    ),
    cv.Optional(CONF_DATA_READY): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_POWER,
        icon=ICON_COUNTER,
    ),
    cv.Optional(CONF_FIFO_FULL): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_POWER,
        icon=ICON_COUNTER,
    ),
    cv.Optional(CONF_TEMPERATURE_READY): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_POWER,
        icon=ICON_COUNTER,
    )
})

async def to_code(config):
    max30105_component = await cg.get_variable(config[CONF_MAX30105_ID])
    if power_ready_config := config.get(CONF_POWER_READY):
        sens = await binary_sensor.new_binary_sensor(power_ready_config)
        cg.add(max30105_component.set_power_ready_binary_sensor(sens))
    if has_target_config := config.get(CONF_HAS_TARGET):
        sens = await binary_sensor.new_binary_sensor(has_target_config)
        cg.add(max30105_component.set_target_binary_sensor(sens))
    if alc_overflow_config := config.get(CONF_ALC_OVERFLOW):
        sens = await binary_sensor.new_binary_sensor(alc_overflow_config)
        cg.add(max30105_component.set_alc_overflow_binary_sensor(sens))
    if data_ready_config := config.get(CONF_DATA_READY):
        sens = await binary_sensor.new_binary_sensor(data_ready_config)
        cg.add(max30105_component.set_data_ready_binary_sensor(sens))
    if fifo_full_config := config.get(CONF_FIFO_FULL):
        sens = await binary_sensor.new_binary_sensor(fifo_full_config)
        cg.add(max30105_component.set_fifo_full_binary_sensor(sens))
    if temperature_ready_config := config.get(CONF_TEMPERATURE_READY):
        sens = await binary_sensor.new_binary_sensor(temperature_ready_config)
        cg.add(max30105_component.set_temperature_ready_binary_sensor(sens))