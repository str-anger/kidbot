import telegram
import logging
import settings
import buttons
import time
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

############ Command Handlers ##########################
def hello_handler(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


def start_handler(bot, update):
    text = update.message.text
    author = update.message.from_user.username
    intro = ("Привет @{}! Пиши мне различные факты о своём родительстве" +
            ", а я потихоньку научусь делать на них аналитику. " + 
            "Если какого-то события ещё нет в меню, просто напиши сообщение").format(author)
    bot.send_message(
        text=intro,
        chat_id=update.message.chat_id,
        reply_markup=telegram.ReplyKeyboardMarkup(buttons.START_BUTTONS)
    )


def ask_for_params_handler(bot, update, state, text, keys=None):
    chat_id = update.message.chat_id
    settings.Context['states'][chat_id] = state
    bot.send_message(text=text, chat_id=chat_id, reply_markup=keys)


def record_no_ask(bot, update, state):
    try:
        who = update.message.from_user.username
        chat_id = update.message.chat_id
        where = os.path.join(settings.Context['data-folder'], who)
        answer = "{}\t{}\n".format(int(update.message.date.timestamp()), state)
        with open(where, 'at', encoding="utf-8") as f:
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


CommandMap = {
    '/hello': hello_handler,
    '/start': start_handler,
    '/👩🍔': lambda b, u: ask_for_params_handler(b, u, "mom_food", "Напиши, что ты сегодня ела:"),
    '/🚼🍔': lambda b, u: ask_for_params_handler(b, u, "child_food", "Напиши, что ел ребёнок:"),
    '/🚼рост': lambda b, u: ask_for_params_handler(b, u, "child_len", "Напиши рост (см):"),
    '/🚼вес': lambda b, u: ask_for_params_handler(b, u, "child_weight", "Напиши вес (кг):"),
    '/🚼💊': lambda b, u: ask_for_params_handler(b, u, "child_pills", "Что дали ребёнку:"),
    '/👩💊': lambda b, u: ask_for_params_handler(b, u, "mom_pills", "Что дали маме:"),
    '/🚼🤒': lambda b, u: ask_for_params_handler(b, u, "child_ill", "Напиши симптом или диагноз ребёнка:"),
    '/👩🤒': lambda b, u: ask_for_params_handler(b, u, "mom_ill", "Напиши симптом или диагноз мамы:"),
    # '/🌏': lambda b, u: record_no_ask(b, u, "location"),
    '/🚼😴': lambda b, u: record_no_ask(b, u, "sleep"),
    '/🚼😜': lambda b, u: record_no_ask(b, u, "wakeup"),
}

def handler(bot, update):
    print(update)
    cmd = update.message.text.split()[0]
    CommandMap[cmd](bot, update)
