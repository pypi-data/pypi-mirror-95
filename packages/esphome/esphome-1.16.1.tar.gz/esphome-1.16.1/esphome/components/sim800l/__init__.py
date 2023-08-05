import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import automation
from esphome.const import CONF_ID, CONF_TRIGGER_ID
from esphome.components import uart

DEPENDENCIES = ['uart']
CODEOWNERS = ['@glmnet']
MULTI_CONF = True

sim800l_ns = cg.esphome_ns.namespace('sim800l')
Sim800LComponent = sim800l_ns.class_('Sim800LComponent', cg.Component)

Sim800LReceivedMessageTrigger = sim800l_ns.class_('Sim800LReceivedMessageTrigger',
                                                  automation.Trigger.template(cg.std_string,
                                                                              cg.std_string))

# Actions
Sim800LSendSmsAction = sim800l_ns.class_('Sim800LSendSmsAction', automation.Action)

CONF_ON_SMS_RECEIVED = 'on_sms_received'
CONF_RECIPIENT = 'recipient'
CONF_MESSAGE = 'message'

CONFIG_SCHEMA = cv.All(cv.Schema({
    cv.GenerateID(): cv.declare_id(Sim800LComponent),
    cv.Optional(CONF_ON_SMS_RECEIVED): automation.validate_automation({
        cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(Sim800LReceivedMessageTrigger),
    }),
}).extend(cv.polling_component_schema('5s')).extend(uart.UART_DEVICE_SCHEMA))


def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    yield uart.register_uart_device(var, config)

    for conf in config.get(CONF_ON_SMS_RECEIVED, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID], var)
        yield automation.build_automation(trigger, [(cg.std_string, 'message'),
                                                    (cg.std_string, 'sender')], conf)


SIM800L_SEND_SMS_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.use_id(Sim800LComponent),
    cv.Required(CONF_RECIPIENT): cv.templatable(cv.string_strict),
    cv.Required(CONF_MESSAGE): cv.templatable(cv.string),
})


@automation.register_action('sim800l.send_sms', Sim800LSendSmsAction, SIM800L_SEND_SMS_SCHEMA)
def sim800l_send_sms_to_code(config, action_id, template_arg, args):
    paren = yield cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    template_ = yield cg.templatable(config[CONF_RECIPIENT], args, cg.std_string)
    cg.add(var.set_recipient(template_))
    template_ = yield cg.templatable(config[CONF_MESSAGE], args, cg.std_string)
    cg.add(var.set_message(template_))
    yield var
