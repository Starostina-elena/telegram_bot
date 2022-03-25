import time

from telegram import ReplyKeyboardMarkup

from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CallbackContext, CommandHandler

from random import randint

from my_data import data


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def bot_command_start(update, context):
    reply_keyboard = [['/dice', '/timer']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    update.message.reply_text('Привет. Я - бот-помощник для игр.\n' +
                              'Я умею засекать время и имитировать бросок кубика.\n' +
                              'Выбери команду с клавиатуры', reply_markup=markup)


def bot_command_back(update, context):
    reply_keyboard = [['/dice', '/timer']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    update.message.reply_text('Хорошо, возвращаемся в главное меню', reply_markup=markup)


def bot_command_dice(update, context):
    reply_keyboard = [['/throw 1 6', '/throw 2 6'],
                      ['/throw 1 20', '/back']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    update.message.reply_text('Хорошо, бросаем кубики!\n' +
                              'Выбери команду из предложенных или напечатай свою: ' +
                              '1-ое число - количество кубиков, 2-ое - количество граней на каждом кубике',
                              reply_markup=markup)


def bot_command_timer(update, context):
    reply_keyboard = [['/set_timer 0 30', '/set_timer 1 0'],
                      ['/set_timer 5 0', '/back']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    update.message.reply_text('Хорошо, засекаем время!\n' +
                              'Выбери команду из предложенных или напечатай свою:\n' +
                              '1-ое число - кол-во минут, 2-ое - кол-во секунд', reply_markup=markup)


def bot_command_throw(update, context):
    if len(context.args) < 2:
        update.message.reply_text('Недостаточно аргументов')
    elif len(context.args) > 2:
        update.message.reply_text('Слишком много аргументов')
    else:
        try:
            n_cubes, n_fields = int(context.args[0]), int(context.args[1])
        except ValueError:
            update.message.reply_text('Аргументы должны быть целыми числами')
            return
        reply = []
        for i in range(n_cubes):
            reply.append(str(randint(1, n_fields)))
        if n_cubes == 1:
            update.message.reply_text(f'На кубике выпало: {reply[0]}')
        else:
            update.message.reply_text(f'На кубиках выпало: {" ".join(reply)}')


def bot_command_set_timer(update, context):
    global user_storage

    chat_id = update.message.chat_id
    try:
        due = int(context.args[0]) * 60 + int(context.args[1])
        if due < 0:
            update.message.reply_text(
                'Извините, не умеем возвращаться в прошлое')
            return

        job_removed = remove_job_if_exists(
            str(chat_id),
            context
        )

        user_storage[chat_id] = due

        context.job_queue.run_once(
            task,
            due,
            context=chat_id,
            name=str(chat_id),
        )

        text = f'Засек {due}!'
        if job_removed:
            text += ' Старая задача удалена.'

        reply_keyboard = [['/close']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

        update.message.reply_text(text, reply_markup=markup)

    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set <секунд>')


def task(context):
    job = context.job
    context.bot.send_message(job.context, text=f'{user_storage[job.context]} истекло!')


def bot_command_close_timer(update, context):
    reply_keyboard = [['/set_timer 0 30', '/set_timer 1 0'],
                      ['/set_timer 5 0', '/back']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер сброшен' if job_removed else 'Нет активного таймера.'
    update.message.reply_text(text, reply_markup=markup)


def main():
    updater = Updater(data['TOKEN_T'], use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", bot_command_start))
    dp.add_handler(CommandHandler("dice", bot_command_dice))
    dp.add_handler(CommandHandler('timer', bot_command_timer))
    dp.add_handler(CommandHandler("set_timer", bot_command_set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True,
                                  pass_user_data=True
                                  ))
    dp.add_handler(CommandHandler('back', bot_command_back))
    dp.add_handler(CommandHandler('throw', bot_command_throw,
                                  pass_args=True))
    dp.add_handler(CommandHandler("close", bot_command_close_timer,
                                  pass_chat_data=True))

    updater.start_polling()

    # закрытие приложения
    updater.idle()


if __name__ == '__main__':
    user_storage = dict()
    main()
