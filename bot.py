import telebot
import quest
import datetime

with open('config.txt') as f:
    TOKEN = f.readline()

bot = telebot.TeleBot(TOKEN)
#telebot.apihelper.proxy = {'https': 'http://92.60.237.34:4550'}



team_progress = dict()
team_finish = dict()
teams = dict()


# Обработчик команд '/start' и '/help'.
@bot.message_handler(commands=['start'])
def handle_start_help(message):
    bot.send_message(message.from_user.id, """Привет, с помощью этого бота будет проходить квест на школе тьторов.\n
    Когда квест начнется вы получите первоначальные иснтрукции для начала работы. А пока что отправьте id \n
    свой команды в формате 'id:{номер команды}' без кавычек и скобок. Например, id:4. Удачи:)
    """)
    #team_progress[message.from_user.id] = 0


@bot.message_handler(content_types=["text"])
def handle_text(message):
    global team_progress
    global team_finish
    global teams
    if message.text.lower() == "newquestzero":
        team_progress = dict()
        team_finish = dict()
        teams = dict()
    elif message.text.lower() == "getprogress":
        bot.send_message(message.from_user.id, team_progress)
    elif message.text.lower().startswith("id") or teams.get(message.from_user.id) is None:
        if teams.get(message.from_user.id) is None:
        #if message.text.lower().startswith("id"):
            id = message.text.lower().split(":")[1]
            if not id.isdigit() and id.isdigit() is None:
                bot.send_message(message.from_user.id, "Отправьте id своей команды")
            else:
                teams[message.from_user.id] = id
        else:
            bot.send_message(message.from_user.id, "Отправьте id своей команды")
    else:
        if message.text.lower() == "start": # and team_progress[message.from_user.id] == 0:
            start_quest(message.from_user.id)
        else:
            check_answer(message.text.lower(), teams[message.from_user.id])


def start_quest(bot_id):
    bot.send_message(bot_id, quest.quest[0][quest.QUESTION])


def check_answer(answer, id):
    global team_progress
    global team_finish
    global teams
    if quest.quest[team_progress[id]][quest.ANSWER] == answer:
        if team_progress[id] == len(quest.quest):
            team_finish[id] = datetime.datetime.now()
            bot.send_message(id, "Вы правы. Квест завершен, ожидайте результатов")
        else:
            team_progress[id] += 1#
            bot.send_message(id, "Вы правы. \nСледующий вопрос:\n{}".format(quest.quest[team_progress[id]][quest.QUESTION]))
    else:
        bot.send_message(id, "Неправильный ответ, \n{}".format(quest.quest[team_progress[id]][quest.QUESTION]))


bot.polling(none_stop=True, interval=0)
