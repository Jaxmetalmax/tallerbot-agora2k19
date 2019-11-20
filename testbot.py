import sys
from time import sleep
import traceback
#Buenas practicas (los primeros modulos si son del sistema, van al inicio)

from twx.botapi import TelegramBot
from decouple import config
import pyowm

TOKEN = config('TOKEN')
OWMTOKEN = config('OWMTOKEN')
LAST_UPDATE_ID = 0

#Iniciamos el bot con el token que nos dio el BotFather
bot = TelegramBot(TOKEN)
bot.update_bot_info().wait()
print (bot.username)

#Iniciamos la API de OpenWeather
owm = pyowm.OWM(OWMTOKEN, language='es')

def get_clima(bot, chat_id, id_location):
    try:
        location = id_location[7:]
        print(location)
        observation = owm.weather_at_place(location)
        weather = observation.get_weather()
    
        location = observation.get_location()
        status = str(weather.get_detailed_status())
        city = str(location.get_name())
        temperature = str(weather.get_temperature('celsius').get('temp'))
        bot.send_message(chat_id, 'Estatus de clima: ' +status +' en '+city+' y la temperatura es: '+ temperature+ 'C')
    except Exception:
        bot.send_message(chat_id, 'Ciudad no encontrada o sintaxis incorrecta... \n prueba de nuevo')

def process_message(bot, upd):
    chat_id = upd.message.chat.id

    try:
        message = upd.message.text
        if message.lower() == "/clima":
            bot.send_message(chat_id, 'Dame tu ubicacion...')
        elif "ciudad-" in message.lower():
            get_clima(bot, chat_id, message)
    except Exception:
        print(traceback.format_exc())

while True:
#    print last_update_id
    updates = bot.get_updates(offset = LAST_UPDATE_ID).wait()
    #comenzamos a cachar los updates del chat
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