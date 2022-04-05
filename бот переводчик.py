from requests import get

from telegram import ReplyKeyboardMarkup

from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler

from my_data import data


def bot_command_start(update, context):
    reply_keyboard = [['/stop'],
                      ['русский -> английский'], ['английский -> русский']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    update.message.reply_text(
        "Доброго времени суток! Выберите направление перевода с помощью клавиатуры и введите слово для перевода!\n",
        reply_markup=markup)
    update.message.reply_text('Текущее направление перевода: русский -> английский')
    context.user_data['direction'] = 'ru|en'


def translate(update, context):
    if update.message.text == 'русский -> английский':
        context.user_data['direction'] = 'ru|en'
        update.message.reply_text('Текущее направление перевода: русский -> английский')
    elif update.message.text == 'английский -> русский':
        context.user_data['direction'] = 'en|ru'
        update.message.reply_text('Текущее направление перевода: английский -> русский')
    else:
        url = "https://translated-mymemory---translation-memory.p.rapidapi.com/api/get"
        querystring = {
            "langpair": context.user_data['direction'],
            "q": update.message.text,
            "mt": "1",
            "onlyprivate": "0",
            "de": "a@b.c"}
        headers = {
            "X-RapidAPI-Host": "translated-mymemory---translation-memory.p.rapidapi.com",
            "X-RapidAPI-Key": "6ad936017dmsh99edf262e93f309p168ab5jsn174535694072"
        }
        response = get(url, headers=headers, params=querystring)

        update.message.reply_text(response.json()['responseData']['translatedText'])


def bot_command_stop(update, context):
    reply_keyboard = [['/start']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    update.message.reply_text('Было приятно пообщаться, всего доброго!',
                              reply_markup=markup)


def main():
    updater = Updater(data['TOKEN_T'], use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", bot_command_start, pass_user_data=True))
    dp.add_handler(CommandHandler("stop", bot_command_stop))
    dp.add_handler(MessageHandler(Filters.text, translate, pass_user_data=True))

    updater.start_polling()

    # закрытие приложения
    updater.idle()


if __name__ == '__main__':
    main()
