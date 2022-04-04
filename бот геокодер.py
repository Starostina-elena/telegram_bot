import geocoder

from requests import get

from telegram import ReplyKeyboardMarkup

from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler

from my_data import data


def bot_command_start(update, context):
    reply_keyboard = [['/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    update.message.reply_text(
        "Доброго времени суток! Напишите адрес, и я покажу это место на карте!\n", reply_markup=markup)


def send_picture(update, context):
    ll, spn = geocoder.get_ll_span(update.message.text)  # адрес
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=sat,skl&size=650,450&pt={ll},comma"

    if ll is None:
        update.message.reply_text('Похоже, такого адреса не существует')
    else:
        response = get(map_request)
        if not response:
            update.message.reply_text(f'Ошибка выполнения запроса: {response.status_code}, {response.reason}')
        else:
            update.message.reply_photo(caption=update.message.text, photo=map_request)


def bot_command_stop(update, context):
    reply_keyboard = [['/start']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    update.message.reply_text('Было приятно пообщаться, всего доброго!',
                              reply_markup=markup)


def main():
    updater = Updater(data['TOKEN_T'], use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", bot_command_start))
    dp.add_handler(CommandHandler("stop", bot_command_stop))
    dp.add_handler(MessageHandler(Filters.text, send_picture))

    updater.start_polling()

    # закрытие приложения
    updater.idle()


if __name__ == '__main__':
    main()
