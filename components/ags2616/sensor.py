from esphome import automation
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, i2c
from esphome.const import (
    CONF_ID,
    CONF_CURRENT_RESISTOR,
    CONF_HYDROGEN,
    CONF_MODE,
    DEVICE_CLASS_CARBON_MONOXIDE,
    STATE_CLASS_MEASUREMENT,
    UNIT_PARTS_PER_MILLION,
    UNIT_OHM, ICON_RESTART,
    ENTITY_CATEGORY_DIAGNOSTIC,
)

CODEOWNERS = ["@synodriver"]
DEPENDENCIES = ["i2c"]

ags2616 = cg.esphome_ns.namespace("ags2616")
AGS2616Component = ags2616.class_("AGS2616Component", cg.PollingComponent, i2c.I2CDevice)

ICON_HYDROGEN = "mdi:hydrogen-station"

CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(AGS2616Component),
            cv.Optional(CONF_HYDROGEN): sensor.sensor_schema(
                unit_of_measurement=UNIT_PARTS_PER_MILLION,
                accuracy_decimals=0,
                icon=ICON_HYDROGEN,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_CURRENT_RESISTOR): sensor.sensor_schema(
                unit_of_measurement=UNIT_OHM,
                icon=ICON_RESTART,
                accuracy_decimals=0,
                state_class=STATE_CLASS_MEASUREMENT,
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
            ),
        }
    )
    .extend(cv.polling_component_schema("20s"))
    .extend(i2c.i2c_device_schema(0x1A)),
)

FINAL_VALIDATE_SCHEMA = i2c.final_validate_device_schema("ags2616", max_frequency="100khz")


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)

    if CONF_HYDROGEN in config:
        sens = await sensor.new_sensor(config[CONF_HYDROGEN])
        cg.add(var.set_h2_sensor(sens))
    if CONF_CURRENT_RESISTOR in config:
        sens = await sensor.new_sensor(config[CONF_CURRENT_RESISTOR])
        cg.add(var.set_resistor_sensor(sens))


AGS2616CalibrateAction = ags2616.class_("AGS2616CalibrateAction", automation.Action)
AGS2616_CALIBRATEACTION_SCHEMA = automation.maybe_simple_id(
    {
        cv.Required(CONF_ID): cv.use_id(AGS2616Component),
        cv.Required(CONF_MODE): cv.positive_int,
    }
)


@automation.register_action("ags2616.calibrate", AGS2616CalibrateAction, AGS2616_CALIBRATEACTION_SCHEMA)
async def ags2616_calibrate_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    mode = await cg.templatable(config[CONF_MODE], args, cg.uint16)
    cg.add(var.set_mode(mode))
    return var
