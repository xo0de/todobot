from random import choice
import telebot

token = '5717734841:AAHigJ6JrEpzprJKGcsHSOJOyhPgLiT6dJk'
bot = telebot.TeleBot(token)

RANDOM_TASKS = ['Сходить на прогулку', 'Выучить новый язык программирования', 'Приготовить что-то вкусное',
                'Начать смотреть новый сериал']  # спсибо можно расширять

todos = dict()

HELP = """
Список доступных команд:
* print  - напечатать все задачи на заданную дату в формате 'Дата' 'Задача'
* add_todo - добавить задачу в формате 'Дата Задача'
* random - добавить на сегодня случайную задачу
* help - Напечатать help
"""


def add_todo(date, task):
    date = date.lower()
    if todos.get(date) is not None:
        todos[date].append(task)
    else:
        todos[date] = [task]


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, HELP)
    bot.send_message(message.chat.id, 'Команды должны записываться с "/" знаком перед текстом')


@bot.message_handler(commands=['random'])
def random_task(message):
    task = choice(RANDOM_TASKS)
    add_todo('сегодня', task)
    bot.send_message(message.chat.id, f'Задача "{task}" добавлена на сегодня')


@bot.message_handler(commands=['add_todo'])
def add(message):
    _, date, task = message.text.split(maxsplit=2)

    if len(task) < 3:
        bot.send_message(message.chat.id, 'Задачи должны быть больше 3-х символов')
        return

    add_todo(date, task)
    bot.send_message(message.chat.id, f'Задача "{task}" добавлена на дату {date}')


@bot.message_handler(commands=['print'])
def print_(message):
    # TODO: 2
    dates = message.text.split(maxsplit=1)[1].lower().split()
    response = ''
    for date in dates:
        tasks = todos.get(date)
        if tasks:
            response += f'{date}: \n'
            for task in tasks:
                response += f'[ ] {task}\n'
            response += '\n'
        else:
            response += f'На {date} задач нет\n\n'
    bot.send_message(message.chat.id, response)


bot.polling(none_stop=True)
