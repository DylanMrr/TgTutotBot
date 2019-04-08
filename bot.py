import telebot
import quest

with open('config.txt') as f:
    TOKEN = f.readline()

bot = telebot.TeleBot(TOKEN)
#telebot.apihelper.proxy = {'https': 'http://92.60.237.34:4550'}

team_progress = dict()


# Обработчик команд '/start' и '/help'.
@bot.message_handler(commands=['start'])
def handle_start_help(message):
    bot.send_message(message.from_user.id, """Привет, с помощью этого бота будет проходить квест на школе тьторов.\n
    Когда квест начнется вы получите первоначальные иснтрукции для начала работы. Удачи!
    """)
    team_progress[message.from_user.id] = 0


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.lower() == "start" and team_progress[message.from_user.id] == 0:
        start_quest(message.from_user.id)
    else:
        check_answer(message.text.lower(), message.from_user.id)


def start_quest(id):
    bot.send_message(id, quest.quest[0][quest.QUESTION])


def check_answer(answer, id):
    if quest.quest[team_progress[id]][quest.ANSWER] == answer:
        team_progress[id] += 1
        bot.send_message(id, "Вы правы. \nСледующий вопрос:\n{}".format(quest.quest[team_progress[id]][quest.QUESTION]))
    else:
        bot.send_message(id, "Неправильный ответ, \n{}".format(quest.quest[team_progress[id]][quest.QUESTION]))


bot.polling(none_stop=True, interval=0)
