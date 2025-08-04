from esphome import automation
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, i2c
from esphome.const import (
    CONF_ID,
    CONF_CURRENT_RESISTOR,
    CONF_MODE,
    STATE_CLASS_MEASUREMENT,
    UNIT_OHM, ICON_RESTART, ENTITY_CATEGORY_DIAGNOSTIC, CONF_TVOC, UNIT_PARTS_PER_BILLION, ICON_RADIATOR,
    DEVICE_CLASS_VOLATILE_ORGANIC_COMPOUNDS_PARTS,
)

CODEOWNERS = ["@synodriver"]
DEPENDENCIES = ["i2c"]
ICON_GAS_BURNER = "mdi:gas-burner"

ags2602 = cg.esphome_ns.namespace("ags2602")
AGS2602Component = ags2602.class_("AGS2602Component", cg.PollingComponent, i2c.I2CDevice)
# 甲烷
CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(AGS2602Component),
            cv.Optional(CONF_TVOC): sensor.sensor_schema(
                unit_of_measurement=UNIT_PARTS_PER_BILLION,
                icon=ICON_RADIATOR,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_VOLATILE_ORGANIC_COMPOUNDS_PARTS,
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

FINAL_VALIDATE_SCHEMA = i2c.final_validate_device_schema("ags2602", max_frequency="100khz")

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)

    if CONF_TVOC in config:
        sens = await sensor.new_sensor(config[CONF_TVOC])
        cg.add(var.set_tvoc_sensor(sens))
    if CONF_CURRENT_RESISTOR in config:
        sens = await sensor.new_sensor(config[CONF_CURRENT_RESISTOR])
        cg.add(var.set_resistor_sensor(sens))

AGS2602CalibrateAction = ags2602.class_("AGS2602CalibrateAction", automation.Action)
AGS2602_CALIBRATEACTION_SCHEMA = automation.maybe_simple_id(
    {
        cv.Required(CONF_ID): cv.use_id(AGS2602Component),
        cv.Required(CONF_MODE): cv.positive_int,
    }
)
@automation.register_action("ags2602.calibrate", AGS2602CalibrateAction, AGS2602_CALIBRATEACTION_SCHEMA)
async def ags2602_calibrate_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    mode = await cg.templatable(config[CONF_MODE], args, cg.uint16)
    cg.add(var.set_mode(mode))
    return var