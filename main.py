import time

from telegram import ReplyKeyboardMarkup

from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CallbackContext, CommandHandler

from my_data import data


def bot_command_start(update, context):
    update.message.reply_text(
        "Привет. Пройдите небольшой опрос, пожалуйста!\n"
        "Вы можете прервать опрос, послав команду /stop.\n"
        "В каком городе вы живёте?", reply_markup=markup)

    return 1


def first_response(update, context):
    context.user_data['locality'] = update.message.text

    reply_keyboard = [['/start', '/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    update.message.reply_text(f"Какая погода в городе {context.user_data['locality']}?", reply_markup=markup)

    return 2


def second_response(update, context):
    weather = update.message.text

    if 'locality' in context.user_data:
        update.message.reply_text(f"Спасибо за участие в опросе! Привет, {context.user_data['locality']}!")
    else:
        update.message.reply_text('Спасибо за участие в опросе!')

    return ConversationHandler.END


def skip_command(update, context):
    reply_keyboard = [['/start', '/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text('Какая погода у вас за окном?', reply_markup=markup)
    return 2


def bot_stop(update, context):
    update.message.reply_text('Было приятно пообщаться, всего доброго!')
    return ConversationHandler.END


def main():
    global markup

    updater = Updater(data['TOKEN_T'], use_context=True)

    dp = updater.dispatcher

    reply_keyboard = [['/start', '/skip'],
                      ['/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', bot_command_start)],
        states={
            1: [CommandHandler('stop', bot_stop), CommandHandler('skip', skip_command),
                MessageHandler(Filters.text, first_response, pass_user_data=True)],
            2: [CommandHandler('stop', bot_stop), MessageHandler(Filters.text, second_response, pass_user_data=True)]
        },

        fallbacks=[CommandHandler('stop', bot_stop)]
    )
    dp.add_handler(conv_handler)

    updater.start_polling()

    # закрытие приложения
    updater.idle()


if __name__ == '__main__':
    main()
