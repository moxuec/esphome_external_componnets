from esphome import automation
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, i2c
from esphome.const import (
    CONF_ID,
    CONF_TYPE,
    CONF_CURRENT_RESISTOR,
    CONF_MODE,
    STATE_CLASS_MEASUREMENT,
    UNIT_PARTS_PER_MILLION,
    UNIT_OHM, ICON_RESTART,
    ENTITY_CATEGORY_DIAGNOSTIC,
)

CODEOWNERS = ["@synodriver"]
DEPENDENCIES = ["i2c"]

agsxxxx = cg.esphome_ns.namespace("agsxxxx")
AGSXXXXComponent = agsxxxx.class_("AGSXXXXComponent", cg.PollingComponent, i2c.I2CDevice)

CONF_GAS = "gas"

CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(AGSXXXXComponent),
            cv.Optional(CONF_GAS): sensor.sensor_schema(
                unit_of_measurement=UNIT_PARTS_PER_MILLION,
                accuracy_decimals=0,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Required(CONF_TYPE): cv.string,
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

FINAL_VALIDATE_SCHEMA = i2c.final_validate_device_schema("agsxxxx", max_frequency="100khz")

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)

    if CONF_GAS in config:
        sens = await sensor.new_sensor(config[CONF_GAS])
        cg.add(var.set_gas_sensor(sens))
    cg.add(var.set_type(config[CONF_TYPE]))
    if CONF_CURRENT_RESISTOR in config:
        sens = await sensor.new_sensor(config[CONF_CURRENT_RESISTOR])
        cg.add(var.set_resistor_sensor(sens))

AGSXXXXCalibrateAction = agsxxxx.class_("AGSXXXXCalibrateAction", automation.Action)
AGSxxxx_CALIBRATEACTION_SCHEMA = automation.maybe_simple_id(
    {
        cv.Required(CONF_ID): cv.use_id(AGSXXXXComponent),
        cv.Required(CONF_MODE): cv.positive_int,
    }
)
@automation.register_action("agsxxxx.calibrate", AGSXXXXCalibrateAction, AGSxxxx_CALIBRATEACTION_SCHEMA)
async def agsxxxx_calibrate_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    mode = await cg.templatable(config[CONF_MODE], args, cg.uint16)
    cg.add(var.set_mode(mode))
    return var