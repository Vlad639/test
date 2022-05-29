from email.message import Message
import requests
import datetime
import config
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=config.tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Привет! Я Погодник. Напиши мне любой город, чтобы узнать погоду в нем на данный момент!')

@dp.message_handler()
async def get_weather(message: types.Message):
    r = requests.get(
            f"http://api.openweathermap.org/geo/1.0/direct?q={message.text}&limit={1}&appid={config.open_weather_token}"
        )
    workrequest = r.json()
    sql_json = []
    for i in range(len(workrequest)):
        sql_json.append(workrequest[i]['lat'])
        sql_json.append(workrequest[i]['lon'])
        lat = sql_json[0]
        lon = sql_json[1]
        sql_json.clear()
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={config.open_weather_token}&units=metric"
        )
        data = r.json()
        city = data["name"]
        cur_weather = int(data['main']['temp'])
        weather_description = data['weather'][0]['main']
        if weather_description in config.code_to_smile:
            wd = config.code_to_smile[weather_description]
        else:
            wd = 'не могу определить погодные условия'
        humidity = data['main']['humidity']
        pressure = int(data['main']['pressure'] * 0.750062)
        wind = int(data['wind']['speed'])
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        await message.reply(f'Сейчас: {datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}\n'
            f'Отчет по погоде в городе: {city}\nТемпуратура: {cur_weather}°C {wd}\nВлажность: {humidity}%'
            f'\nДавление: {pressure} мм рт. ст.\nСкорость ветра: {wind} м/с\nВосход солнца: {sunrise_timestamp}\n'
            f'Закат солнца: {sunset_timestamp}\nХорошего дня!')
    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")
    

if __name__ == '__main__':
    executor.start_polling(dp)