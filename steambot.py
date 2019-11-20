import sys
from time import sleep
import traceback
import json
import datetime

from twx.botapi import TelegramBot
from decouple import config
import requests

TOKEN = config('TOKEN_STEAM')
LAST_UPDATE_ID = 1
BASE_API_URL = 'http://127.0.0.1:3000/'

#Iniciamos el bot con el token que nos dio el BotFather
bot = TelegramBot(TOKEN)
bot.update_bot_info().wait()
print (bot.username)

def get_listgames(bot, chat_id):
    response = requests.get(f'{BASE_API_URL}games')

    if response.status_code == 200:
        list_games = json.loads(response.content.decode('utf-8'))
        list_games = list_games["games"]
        
        list_titles = ""
        for game in list_games:
            list_titles = list_titles+" "+game+ "\n"

        bot.send_message(chat_id, "La lista de juegos es: \n"+list_titles)

def get_today_list(bot, chat_id):
    response = requests.get(f'{BASE_API_URL}games/today')

    now = datetime.date.today().strftime("%Y-%m-%d")

    if response.status_code == 200:
        list_games = json.loads(response.content.decode('utf-8'))
        list_games = list_games[now]
        
        list_titles = ""
        for game in list_games:
            for key, value in game.items():
                list_titles = " " + list_titles + key + " " + value

            list_titles = list_titles + "\n"

        bot.send_message(chat_id, "La lista de juegos de hoy es: \n"+list_titles)

def get_game_history(bot, chat_id, title):
    pass

BOT_OPTIONS = {"/game_list": get_listgames, "/game_today": get_today_list}

def process_message(bot, upd):

    chat_id = upd.message.chat.id

    try:
        message = upd.message.text

        if message == "/get_history":
            bot.send_message(chat_id, 'Que titulo quieres consultar?')
        try:
            BOT_OPTIONS[message.lower()](bot, chat_id)
        except Exception:
            print(traceback.format_exc())

    except Exception:
        print(traceback.format_exc())

while True:
#    print last_update_id
    updates = bot.get_updates(offset = LAST_UPDATE_ID).wait()
    try:
        for update in updates:
            if int(update.update_id) > int(LAST_UPDATE_ID):
                LAST_UPDATE_ID = update.update_id
                process_message(bot, update)
                continue
        continue
    except Exception:
        ex = None
        print (traceback.format_exc())
        continue