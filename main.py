import telebot
import requests
import json
import datetime

bot = telebot.TeleBot('6536600260:AAHr6yh0dTfAJHR65vfiKY6bj5ph_U')
API = '76f0c7ecdf12436a9e548857a04'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hi there. Please write the name of the city:')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:

        data = json.loads(res.text)
        temp = data["main"]["temp"]
        condition = data["weather"][0]["main"]
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        sunrise = datetime.datetime.utcfromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.utcfromtimestamp(data['sys']['sunset'])
        bot.reply_to(message, f"Now:\ntoday's date: {sunrise.day}.{sunrise.month}.{sunrise.year}\ntime: {datetime.datetime.now().hour}:{datetime.datetime.now().minute}\ntemperature: {temp}°C\nhumidity: {humidity}%\npressure: {pressure} HPA\nsunrise time: {sunrise.time()}\nsunset time: {sunset.time()}")

        if condition == 'Clear':
            image = 'sunny.jpg'
        elif condition == 'Clouds':
            image = 'sun_with_clouds.jpg'
        elif condition == 'Rain' or condition == 'Drizzle':
            image = 'rainy.jpg'
        elif condition == 'Snow':
            image = 'snow.jpg'
        elif condition == 'Thunderstorm':
            image = 'thunderstorm.jpg'
        else:
            image = 'atmosphere.jpg'

        file = open('./' + image, 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.send_message(message.chat.id, 'Oh no, this is not the name of the city. Or we do not have information about it.\nPlease type the real name of the city:')


bot.polling(none_stop=True)