from telegram import ReplyKeyboardMarkup

from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CallbackContext, CommandHandler

from my_data import data

VERSE = '''Зима!.. Крестьянин, торжествуя,
На дровнях обновляет путь;
Его лошадка, снег почуя,
Плетется рысью как-нибудь;
Бразды пушистые взрывая,
Летит кибитка удалая;
Ямщик сидит на облучке
В тулупе, в красном кушаке.
Вот бегает дворовый мальчик,
В салазки жучку посадив,
Себя в коня преобразив;
Шалун уж заморозил пальчик:
Ему и больно и смешно,
А мать грозит ему в окно…'''.split('\n')


def bot_command_start(update, context):
    reply_keyboard = [['/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    update.message.reply_text('Привет! Давай расскажем стих?\n\n' + VERSE[0], reply_markup=markup)

    return 1


def first_response(update, context):
    if update.message.text == VERSE[1]:
        reply_keyboard = [['/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        update.message.reply_text(VERSE[2], reply_markup=markup)
        return 2
    else:
        reply_keyboard = [['/stop', '/suphler']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        update.message.reply_text('Нет, не так :(\nНаберите /suphler для подсказки', reply_markup=markup)
        context.user_data['line'] = 1
        return 1


def second_response(update, context):
    if update.message.text == VERSE[3]:
        reply_keyboard = [['/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        update.message.reply_text(VERSE[4], reply_markup=markup)
        return 3
    else:
        reply_keyboard = [['/stop', '/suphler']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        update.message.reply_text('Нет, не так :(\nНаберите /suphler для подсказки', reply_markup=markup)
        context.user_data['line'] = 3
        return 2


def third_response(update, context):
    if update.message.text == VERSE[5]:
        reply_keyboard = [['/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        update.message.reply_text(VERSE[6], reply_markup=markup)
        return 4
    else:
        reply_keyboard = [['/stop', '/suphler']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        update.message.reply_text('Нет, не так :(\nНаберите /suphler для подсказки', reply_markup=markup)
        context.user_data['line'] = 5
        return 3


def fourth_response(update, context):
    if update.message.text == VERSE[7]:
        reply_keyboard = [['/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        update.message.reply_text(VERSE[8], reply_markup=markup)
        return 5
    else:
        reply_keyboard = [['/stop', '/suphler']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        update.message.reply_text('Нет, не так :(\nНаберите /suphler для подсказки', reply_markup=markup)
        context.user_data['line'] = 7
        return 4


def fifth_response(update, context):
    if update.message.text == VERSE[9]:
        reply_keyboard = [['/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        update.message.reply_text(VERSE[10], reply_markup=markup)
        return 6
    else:
        reply_keyboard = [['/stop', '/suphler']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        update.message.reply_text('Нет, не так :(\nНаберите /suphler для подсказки', reply_markup=markup)
        context.user_data['line'] = 9
        return 5


def sixth_response(update, context):
    if update.message.text == VERSE[11]:
        reply_keyboard = [['/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        update.message.reply_text(VERSE[12], reply_markup=markup)
        return 7
    else:
        reply_keyboard = [['/stop', '/suphler']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        update.message.reply_text('Нет, не так :(\nНаберите /suphler для подсказки', reply_markup=markup)
        context.user_data['line'] = 11
        return 6


def seventh_response(update, context):
    if update.message.text == VERSE[13]:
        reply_keyboard = [['/start']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        update.message.reply_text('(А.С. Пушкин)\n\nУра! Спасибо за игру! :)\nМожет, еще раз?', reply_markup=markup)
        return ConversationHandler.END
    else:
        reply_keyboard = [['/stop', '/suphler']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        update.message.reply_text('Нет, не так :(\nНаберите /suphler для подсказки', reply_markup=markup)
        context.user_data['line'] = 13
        return 7


def bot_command_suphler(update, context):
    if 'line' in context.user_data:
        update.message.reply_text(f'({VERSE[context.user_data["line"]]})')
        del context.user_data['line']
    else:
        update.message.reply_text('Сначала попробуйте сами, без подсказки!')


def bot_command_stop(update, context):
    reply_keyboard = [['/start']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    update.message.reply_text('Уже уходите? Жаль... Буду ждать вас снова!', reply_markup=markup)

    return ConversationHandler.END


def main():
    updater = Updater(data['TOKEN_T'], use_context=True)

    dp = updater.dispatcher

    reply_keyboard = [['/start']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', bot_command_start)],
        states={
            1: [CommandHandler('stop', bot_command_stop),
                CommandHandler('suphler', bot_command_suphler, pass_user_data=True),
                MessageHandler(Filters.text, first_response, pass_user_data=True)],
            2: [CommandHandler('stop', bot_command_stop),
                CommandHandler('suphler', bot_command_suphler, pass_user_data=True),
                MessageHandler(Filters.text, second_response, pass_user_data=True)],
            3: [CommandHandler('stop', bot_command_stop),
                CommandHandler('suphler', bot_command_suphler, pass_user_data=True),
                MessageHandler(Filters.text, third_response, pass_user_data=True)],
            4: [CommandHandler('stop', bot_command_stop),
                CommandHandler('suphler', bot_command_suphler, pass_user_data=True),
                MessageHandler(Filters.text, fourth_response, pass_user_data=True)],
            5: [CommandHandler('stop', bot_command_stop),
                CommandHandler('suphler', bot_command_suphler, pass_user_data=True),
                MessageHandler(Filters.text, fifth_response, pass_user_data=True)],
            6: [CommandHandler('stop', bot_command_stop),
                CommandHandler('suphler', bot_command_suphler, pass_user_data=True),
                MessageHandler(Filters.text, sixth_response, pass_user_data=True)],
            7: [CommandHandler('stop', bot_command_stop),
                CommandHandler('suphler', bot_command_suphler, pass_user_data=True),
                MessageHandler(Filters.text, seventh_response, pass_user_data=True)]
        },

        fallbacks=[CommandHandler('stop', bot_command_stop)]
    )
    dp.add_handler(conv_handler)

    updater.start_polling()

    # закрытие приложения
    updater.idle()


if __name__ == '__main__':
    main()
