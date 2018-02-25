from telegram.ext import Updater, CommandHandler, MessageHandler
from handlers import command_handlers as ch
from handlers import message_handlers as mh
import settings
import buttons

###########################################
def load_keys():
    settings.Context['keys']['telegram'] = open('.keys/.telegram').read()
###########################################


def run_bot():
    # sync with command_handlers
    known_commands = [x[1:] for x in ch.CommandMap.keys()]
    updater = Updater(settings.Context['keys']['telegram'])
    updater.dispatcher.add_handler(CommandHandler(known_commands, ch.handler))
    updater.dispatcher.add_handler(
        MessageHandler(
                mh.WordFilter(""), 
                mh.message_handler
        )
    )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    settings.__init__()
    buttons.__init__()
    load_keys()
    run_bot()
