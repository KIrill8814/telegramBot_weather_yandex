from pprint import pprint
import telebot
import requests

token = ''  # токен телегарам бота

bot = telebot.TeleBot(token=token)


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, {message.from_user.first_name}!  Пришли геолакацию, я отправлю тебе погодные сводки.'
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(content_types=['location'])
def location(message):
    try:
        if message.location is not None:
            longitude = message.location.longitude
            latitude = message.location.latitude

            r = requests.get(
                f'https://api.weather.yandex.ru/v2/forecast?lat={latitude}&lon={longitude}&limit=1&lang=ru_RU', # часть адреса может меняться, всё зависит от тарифа. На данный момент, тариф "Тестовый".
                headers={'Accept': 'application/json',
                         'X-Yandex-API-Key': ''}  # API Yandex нужно получить из кабинета разработчика
            )

            data = r.json()
            pprint(data)

            temp = data['fact']['temp']
            geo_object = data['geo_object']
            geo_object_country = geo_object.get('country')
            geo_object_district = geo_object.get('district')
            geo_object_province = geo_object.get('province') #

            msg = f'{temp}C'
            if geo_object_district:
                msg = f'{geo_object_district["name"]} - {msg}'

            if geo_object_province:
                msg = f'{geo_object_province["name"]} - {msg}'

            if geo_object_country:
                msg = f'{geo_object_country["name"]} - {msg}'

            bot.send_message(message.chat.id, msg)

    except Exception as err:
        print(err)


bot.polling(non_stop=True)
