from telegram.ext import filters
import telegram
import logging
import settings
import os
import time
import buttons

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class WordFilter(filters.BaseFilter):
    def __init__(self, what):
        self.what = what.lower()
        logger.debug("filter: {}".format(self.what))

    def filter(self, message):
        logger.debug("filter triggered: {}".format(message.text.lower()))
        return True


def message_handler(bot, update):
    print(update)
    try:
        who = update.message.from_user.username
        chat_id = update.message.chat_id
        value = update.message.text
        action = settings.Context['states'].get(chat_id)
        action = action if action else "unknown"
        where = os.path.join(settings.Context['data-folder'], who)
        answer = "{}\t{}\t{}\n".format(int(time.time()), action, value)
        with open(where, 'at', encoding='utf-8') as f:
            f.write(answer)
        # возвращаемся в базовый диалог, выставляем кнопки верхнего меню
        settings.Context['states'][chat_id] = None
        bot.send_message(
            text="Спасибо, я записал событие:\n `{}`".format(answer),
            chat_id=chat_id,
            reply_markup=telegram.ReplyKeyboardMarkup(buttons.START_BUTTONS),
            parse_mode=telegram.ParseMode.MARKDOWN
        )
    except Exception as e:
        print(e)

