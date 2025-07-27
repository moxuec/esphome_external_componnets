import esphome.codegen as cg
from esphome.components import sensor
import esphome.config_validation as cv
from esphome.const import (
    CONF_TEMPERATURE,
    CONF_DEBUG,
    UNIT_CELSIUS,
    DEVICE_CLASS_TEMPERATURE,
    STATE_CLASS_MEASUREMENT,
)

from . import CONF_MAX30105_ID, MAX30105Component

DEPENDENCIES = ["max30105"]

CONF_LED1 = "led1"
CONF_LED2 = "led2"
CONF_LED3 = "led3"
CONF_LED4 = "led4"
CONF_FIFO_OVERFLOW_COUNTER = "fifo_overflow_counter"
CONF_WR_PTR = "wr_ptr"
CONF_RD_PTR = "rd_ptr"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_MAX30105_ID): cv.use_id(MAX30105Component),
        cv.Optional(CONF_TEMPERATURE): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=3,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LED1): sensor.sensor_schema(
            # unit_of_measurement=UNIT_CELSIUS,
            icon="mdi:led-variant-on",
            accuracy_decimals=1,
            # device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LED2): sensor.sensor_schema(
            # unit_of_measurement=UNIT_CELSIUS,
            icon="mdi:led-variant-on",
            accuracy_decimals=1,
            # device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LED3): sensor.sensor_schema(
            # unit_of_measurement=UNIT_CELSIUS,
            icon="mdi:led-variant-on",
            accuracy_decimals=1,
            # device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LED4): sensor.sensor_schema(
            # unit_of_measurement=UNIT_CELSIUS,
            icon="mdi:led-variant-on",
            accuracy_decimals=1,
            # device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_FIFO_OVERFLOW_COUNTER): sensor.sensor_schema(
            icon="mdi:counter",
            accuracy_decimals=1,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_DEBUG): cv.Schema({
            cv.Optional(CONF_WR_PTR): sensor.sensor_schema(
                icon="mdi:counter",
                accuracy_decimals=1,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_RD_PTR): sensor.sensor_schema(
                icon="mdi:counter",
                accuracy_decimals=1,
                state_class=STATE_CLASS_MEASUREMENT,
            )
        })
    }
)


async def to_code(config):
    max30105_component = await cg.get_variable(config[CONF_MAX30105_ID])
    if temperature := config.get(CONF_TEMPERATURE):
        sens = await sensor.new_sensor(temperature)
        cg.add(max30105_component.set_temperature_sensor(sens))
    if led1 := config.get(CONF_LED1):
        sens = await sensor.new_sensor(led1)
        cg.add(max30105_component.set_led1_sensor(sens))
    if led2 := config.get(CONF_LED2):
        sens = await sensor.new_sensor(led2)
        cg.add(max30105_component.set_led2_sensor(sens))
    if led3 := config.get(CONF_LED3):
        sens = await sensor.new_sensor(led3)
        cg.add(max30105_component.set_led3_sensor(sens))
    if led4 := config.get(CONF_LED4):
        sens = await sensor.new_sensor(led4)
        cg.add(max30105_component.set_led4_sensor(sens))
    if fifo_overflow_counter := config.get(CONF_FIFO_OVERFLOW_COUNTER):
        sens = await sensor.new_sensor(fifo_overflow_counter)
        cg.add(max30105_component.set_fifo_overflow_counter_sensor(sens))
    if debug_conf := config.get(CONF_DEBUG):
        if wr_ptr := debug_conf.get(CONF_WR_PTR):
            sens = await sensor.new_sensor(wr_ptr)
            cg.add(max30105_component.set_wr_ptr_sensor(sens))
        if rd_ptr := debug_conf.get(CONF_RD_PTR):
            sens = await sensor.new_sensor(rd_ptr)
            cg.add(max30105_component.set_rd_ptr_sensor(sens))
