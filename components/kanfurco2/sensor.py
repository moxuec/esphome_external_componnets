import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import automation
from esphome.automation import maybe_simple_id
from esphome.components import sensor, uart
from esphome.const import (
    CONF_ID,
    CONF_CO2,
    CONF_UPDATE_INTERVAL,
    UNIT_PARTS_PER_MILLION,
    ICON_MOLECULE_CO2,
    STATE_CLASS_MEASUREMENT, CONF_PERIOD,
)

CODEOWNERS = ["@synodriver"]
DEPENDENCIES = ["uart"]

CONF_SELF_CALIBRATE = "self_calibrate"
CONF_BASE = "base"

kanfurco2 = cg.esphome_ns.namespace("kanfurco2")
KANFURCO2Component = kanfurco2.class_("KANFURCO2Component", cg.PollingComponent, uart.UARTDevice)

CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(KANFURCO2Component),
            cv.Optional(CONF_CO2): sensor.sensor_schema(
                unit_of_measurement=UNIT_PARTS_PER_MILLION,
                icon=ICON_MOLECULE_CO2,
                accuracy_decimals=0,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_SELF_CALIBRATE, default=True): cv.boolean,
            cv.Optional(CONF_PERIOD, default=7): cv.int_,
            cv.Optional(CONF_BASE, default=400): cv.int_,
        }
    )
    .extend(cv.polling_component_schema("20s"))
    .extend(uart.UART_DEVICE_SCHEMA)
)

# ToggleSelfCalibrateAction = kanfurco2.class_("ToggleSelfCalibrateAction", automation.Action)
#
# KANFURCO2_ACTION_SCHEMA = maybe_simple_id(
#     {
#         cv.Required(CONF_ID): cv.use_id(KANFURCO2Component),
#         cv.Optional("open", default=True): cv.templatable(cv.boolean),
#         cv.Optional("period", default=7): cv.templatable(cv.int_range(min=1, max=15)),
#         cv.Optional("base", default=400): cv.templatable(cv.int_)
#     }
# )
#
# @automation.register_action("kanfurco2.toggle_self_calibrate", ToggleSelfCalibrateAction, KANFURCO2_ACTION_SCHEMA)
# async def toggle_self_calibrate_to_code(config, action_id, template_arg, args):
#     paren = await cg.get_variable(config[CONF_ID])
#     # template_ = await cg.templatable(config.get(CONF_MODE), args, int)
#     # cg.add(var.set_auto_mute_mode(template_))
#     var = cg.new_Pvariable(action_id, template_arg, paren)
#     #
#     # open1 = await cg.templatable(config.get("open"), args, bool)
#     # period = await cg.templatable(config.get("period"), args, int)
#     # base = await cg.templatable(config.get("base"), args, int)
#     # cg.add(var.toggle_self_calibrate(open1, period, base))
#
#     return var



async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    cg.add(var.set_self_calibrate(config[CONF_SELF_CALIBRATE]))
    cg.add(var.set_period(config[CONF_PERIOD]))
    cg.add(var.set_base(config[CONF_BASE]))

    if CONF_CO2 in config:
        sens = await sensor.new_sensor(config[CONF_CO2])
        cg.add(var.set_co2_sensor(sens))