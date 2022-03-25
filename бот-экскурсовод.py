from telegram import ReplyKeyboardMarkup

from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CallbackContext, CommandHandler

from my_data import data


def bot_command_start(update, context):
    reply_keyboard = [['/go_2', '/exit']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    update.message.reply_text('Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб!\n' +
                              'В этом зале представлены скульптуры Древней Греции.\n' +
                              'Дальше вы можете перейти во второй зал - зал Древнего Египта', reply_markup=markup)

    return 1


def first_response(update, context):

    reply_keyboard = [['/go_2', '/exit']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    update.message.reply_text('В этом зале представлены скульптуры Древней Греции\n' +
                              'Дальше вы можете перейти во второй зал - зал Древнего Египта или покинуть музей',
                              reply_markup=markup)

    return 1


def second_response(update, context):

    reply_keyboard = [['/go_3']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    update.message.reply_text('В этом зале представлены папирусы из Древнего Египта\n' +
                              'Дальше вы можете перейти в третий зал - зал Древней Индии', reply_markup=markup)

    return 2


def third_response(update, context):

    reply_keyboard = [['/go_1', '/go_4']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    update.message.reply_text('В этом зале представлены сокровища из Древней Индии\n' +
                              'Дальше вы можете перейти в первый зал - зал Древней Греции ' +
                              'или четвертый зал - арт-галерею', reply_markup=markup)

    return 3


def fourth_response(update, context):
    reply_keyboard = [['/go_1']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    update.message.reply_text('В этом зале представлены картины великих художников\n' +
                              'Дальше вы можете перейти в первый зал - зал Древней Греции', reply_markup=markup)

    return 4


def bot_command_exit(update, context):

    reply_keyboard = ['/start']
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    update.message.reply_text('Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!', reply_markup=markup)

    return ConversationHandler.END


def main():
    global markup

    updater = Updater(data['TOKEN_T'], use_context=True)

    dp = updater.dispatcher

    reply_keyboard = [['/start']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', bot_command_start)],
        states={
            1: [CommandHandler('exit', bot_command_exit), CommandHandler('go_2', second_response)],
            2: [CommandHandler('exit', bot_command_exit), CommandHandler('go_3', third_response)],
            3: [CommandHandler('exit', bot_command_exit), CommandHandler('go_1', first_response),
                CommandHandler('go_4', fourth_response)],
            4: [CommandHandler('exit', bot_command_exit), CommandHandler('go_1', first_response)]
        },

        fallbacks=[CommandHandler('exit', bot_command_exit)]
    )
    dp.add_handler(conv_handler)

    updater.start_polling()

    # закрытие приложения
    updater.idle()


if __name__ == '__main__':
    main()
