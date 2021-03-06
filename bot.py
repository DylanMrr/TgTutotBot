import telebot
import quest
import datetime
import json

with open('config.txt') as f:
    TOKEN = f.readline()

bot = telebot.TeleBot(TOKEN)
TEAM_PROGRESS = "team_progress.txt"
TEAM_RESULT = "team_result.txt"
TEAMS = "teams.txt"


team_progress = dict()
team_finish = dict()
teams = dict()


# Обработчик команд '/start' и '/help'.
@bot.message_handler(commands=['start'])
def handle_start_help(message):
    bot.send_message(message.from_user.id,
        "Привет, с помощью этого бота будет проходить квест на школе тьюторов." +
        "Когда квест начнется вы получите первоначальные иснтрукции для начала работы. \nА пока что отправьте id " +
        "свой команды в формате 'id:{номер команды}' без кавычек и скобок. Например, id:4. \nУдачи:)")


@bot.message_handler(content_types=["text"])
def handle_text(message):
    global team_progress
    global team_finish
    global teams
    telegram_id = message.from_user.id
    receive_message = message.text.lower()
    if message.text.lower() == "newquestzero":
        new_quest_zero()
    elif receive_message == "getprogress":
        bot.send_message(telegram_id, create_progress())
    elif receive_message == 'getresult':
        bot.send_message(telegram_id, create_result())
    elif receive_message == 'getteams':
        bot.send_message(telegram_id, create_teams())
    elif receive_message.startswith("id") or teams.get(telegram_id) is None:
        if teams.get(telegram_id) is None:
            try:
                id = receive_message.split(":")[1]
                if not id.isdigit() and id.isdigit() is None:
                    bot.send_message(telegram_id, "Отправьте id своей команды")
                else:
                    teams[telegram_id] = id
                    team_progress[id] = 0
            except IndexError:
                bot.send_message(telegram_id, "Отправьте id своей команды")
        else:
            bot.send_message(telegram_id, "Отправьте id своей команды")
    else:
        if receive_message == "start": # and team_progress[message.from_user.id] == 0:
            start_quest(telegram_id)
        else:
            check_answer(receive_message, teams[telegram_id], telegram_id)


def new_quest_zero():
    global teams
    global team_finish
    global team_progress
    team_progress = dict()
    team_finish = dict()
    teams = dict()


def start_quest(bot_id):
    bot.send_message(bot_id, quest.quest[0][quest.QUESTION])


def check_answer(answer, id, id_tg):
    global team_progress
    global team_finish
    global teams
    if quest.quest[team_progress[id]][quest.ANSWER] == answer:
        if team_progress[id] == len(quest.quest) - 1:#s
            current_time = datetime.datetime.now()
            time_str = "{}:{}:{}".format(current_time.hour + 3, current_time.minute, current_time.second)
            team_finish[id] = time_str#
            bot.send_message(id_tg, "Вы правы. Квест завершен, ожидайте результатов")
        else:
            team_progress[id] += 1
            bot.send_message(id_tg, "Вы правы. Следующий вопрос: \n\n{}".format(quest.quest[team_progress[id]][quest.QUESTION]))
    else:
        bot.send_message(id_tg, "Неправильный ответ. \n\n{}".format(quest.quest[team_progress[id]][quest.QUESTION]))


def create_result():
    global team_finish
    return json.dumps(team_finish)


def create_progress():
    global team_progress
    return json.dumps(team_progress)


def create_teams():
    global teams
    return json.dumps(teams)


bot.polling(none_stop=True, interval=0)
