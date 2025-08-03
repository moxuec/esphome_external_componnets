from esphome import automation
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, i2c
from esphome.const import (
    CONF_ID,
    CONF_METHANE,
    CONF_CURRENT_RESISTOR,
    CONF_MODE,
    STATE_CLASS_MEASUREMENT,
    UNIT_PARTS_PER_MILLION,
    UNIT_OHM,
)

CODEOWNERS = ["@synodriver"]
DEPENDENCIES = ["i2c"]
ICON_GAS_BURNER = "mdi:gas-burner"

ags3870 = cg.esphome_ns.namespace("ags3870")
AGS3870Component = ags3870.class_("AGS3870Component", cg.PollingComponent, i2c.I2CDevice)
# 甲烷
CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(AGS3870Component),
            cv.Optional(CONF_METHANE): sensor.sensor_schema(
                unit_of_measurement=UNIT_PARTS_PER_MILLION,
                accuracy_decimals=0,
                icon=ICON_GAS_BURNER,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_CURRENT_RESISTOR): sensor.sensor_schema(
                unit_of_measurement=UNIT_OHM,
                accuracy_decimals=0,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
        }
    )
    .extend(cv.polling_component_schema("20s"))
    .extend(i2c.i2c_device_schema(0x1A)),
)

FINAL_VALIDATE_SCHEMA = i2c.final_validate_device_schema("ags3870", max_frequency="100khz")

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)

    if CONF_METHANE in config:
        sens = await sensor.new_sensor(config[CONF_METHANE])
        cg.add(var.set_ch4_sensor(sens))
    if CONF_CURRENT_RESISTOR in config:
        sens = await sensor.new_sensor(config[CONF_CURRENT_RESISTOR])
        cg.add(var.set_resistor_sensor(sens))

AGS3870CalibrateAction = ags3870.class_("AGS3870CalibrateAction", automation.Action)
AGS3870_CALIBRATEACTION_SCHEMA = automation.maybe_simple_id(
    {
        cv.Required(CONF_ID): cv.use_id(AGS3870Component),
        cv.Required(CONF_MODE): cv.positive_int,
    }
)
@automation.register_action("ags3870.calibrate", AGS3870CalibrateAction, AGS3870_CALIBRATEACTION_SCHEMA)
async def ags3870_calibrate_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    mode = await cg.templatable(config[CONF_MODE], args, cg.uint16)
    cg.add(var.set_mode(mode))
    return var