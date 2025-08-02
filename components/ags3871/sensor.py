from esphome import automation
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, i2c
from esphome.const import (
    CONF_ID,
    CONF_CARBON_MONOXIDE,
    CONF_CURRENT_RESISTOR,
    CONF_MODE,
    DEVICE_CLASS_CARBON_MONOXIDE,
    STATE_CLASS_MEASUREMENT,
    UNIT_PARTS_PER_MILLION,
    UNIT_OHM,
)

CODEOWNERS = ["@synodriver"]
DEPENDENCIES = ["i2c"]

ags3871 = cg.esphome_ns.namespace("ags3871")
AGS3871Component = ags3871.class_("AGS3871Component", cg.PollingComponent, i2c.I2CDevice)

CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(AGS3871Component),
            cv.Optional(CONF_CARBON_MONOXIDE): sensor.sensor_schema(
                unit_of_measurement=UNIT_PARTS_PER_MILLION,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_CARBON_MONOXIDE,
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

FINAL_VALIDATE_SCHEMA = i2c.final_validate_device_schema("ags3871", max_frequency="100khz")

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)

    if CONF_CARBON_MONOXIDE in config:
        sens = await sensor.new_sensor(config[CONF_CARBON_MONOXIDE])
        cg.add(var.set_co_sensor(sens))
    if CONF_CURRENT_RESISTOR in config:
        sens = await sensor.new_sensor(config[CONF_CURRENT_RESISTOR])
        cg.add(var.set_resistor_sensor(sens))

AGS3871CalibrateAction = ags3871.class_("AGS3871CalibrateAction", automation.Action)
AGS3871_CALIBRATEACTION_SCHEMA = automation.maybe_simple_id(
    {
        cv.Required(CONF_ID): cv.use_id(AGS3871Component),
        cv.Required(CONF_MODE): cv.positive_int,
    }
)
@automation.register_action("ags3871.calibrate", AGS3871CalibrateAction, AGS3871_CALIBRATEACTION_SCHEMA)
async def ags3871_calibrate_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    mode = await cg.templatable(config[CONF_MODE], args, cg.uint16)
    cg.add(var.set_mode(mode))
    return var