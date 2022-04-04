import json
from random import shuffle

from telegram import ReplyKeyboardMarkup

from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler

from my_data import data


def bot_command_start(update, context):
    reply_keyboard = [['/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    update.message.reply_text(
        "Доброго времени суток! Давайте проверим ваши знания!\n"
        "Вы можете прервать опрос, послав команду /stop.", reply_markup=markup)

    context.user_data['score'] = 0
    context.user_data['current_question'] = 0

    with open('testing_system.json', encoding='utf-8') as f:
        test_data = json.loads(f.read())['test']
        shuffle(test_data)

    context.user_data['test_data'] = test_data

    update.message.reply_text(f'{context.user_data["current_question"] + 1}. ' +
                              f'{context.user_data["test_data"][context.user_data["current_question"]]["question"]}')


def check_answer(update, context):
    if update.message.text == context.user_data["test_data"][context.user_data["current_question"]]["response"]:
        update.message.reply_text('Верно!')
        context.user_data['score'] += 1
    else:
        update.message.reply_text(f'Нет. Правильный ответ - ' +
                                  f'{context.user_data["test_data"][context.user_data["current_question"]]["response"]}')

    context.user_data['current_question'] += 1

    if context.user_data['current_question'] < len(context.user_data['test_data']):
        update.message.reply_text('Следующий вопрос:')
        update.message.reply_text(f'{context.user_data["current_question"] + 1}. ' +
                                  f'{context.user_data["test_data"][context.user_data["current_question"]]["question"]}')
    else:
        reply_keyboard = [['/start']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        update.message.reply_text(f'Опрос завершен, спасибо за участие! ' +
                                  f'Вы ответили правильно на {context.user_data["score"]} вопросов ' +
                                  f'из {len(context.user_data["test_data"])}', reply_markup=markup)


def bot_command_stop(update, context):
    reply_keyboard = [['/start']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    update.message.reply_text('Было приятно пообщаться, всего доброго! Вы ответили правильно на ' +
                              f'{context.user_data["score"]} вопросов из {context.user_data["current_question"]}',
                              reply_markup=markup)


def main():
    updater = Updater(data['TOKEN_T'], use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", bot_command_start, pass_user_data=True))
    dp.add_handler(CommandHandler("stop", bot_command_stop, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, check_answer, pass_user_data=True))

    updater.start_polling()

    # закрытие приложения
    updater.idle()


if __name__ == '__main__':
    main()
