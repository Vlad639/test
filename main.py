from urllib import response
import requests
import datetime
from pprint import pprint
import config
import aiogram


def get_coordinates(city, open_weather_token):
    try:
        r = requests.get(
            f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={1}&appid={open_weather_token}"
        )
        workrequest = r.json()
        sql_json = []
        for i in range(len(workrequest)):
            sql_json.append(workrequest[i]['lat'])
            sql_json.append(workrequest[i]['lon'])
        lat = sql_json[0]
        lon = sql_json[1]
        sql_json.clear()
        get_weather(lat, lon, open_weather_token)
    except Exception as ex:
        print(ex)
        print("Проверьте название города")

def get_weather(lat, lon, open_weather_token):
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        #pprint(data)

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
        print(f'Сейчас: {datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}\n'
            f'Отчет по погоде в городе: {city}\nТемпуратура: {cur_weather}°C {wd}\nВлажность: {humidity}%'
            f'\nДавление: {pressure} мм рт. ст.\nСкорость ветра: {wind} м/с\nВосход солнца: {sunrise_timestamp}\n'
            f'Закат солнца: {sunset_timestamp}\nХорошего дня!')

    except Exception as ex:
        print(ex)
        print("Проверьте название города")

def main():
    city = input('Введите город:' )
    get_coordinates(city, config.open_weather_token)

if __name__ == '__main__':
    main()