from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters

token = '485681211:AAEmirKpeyBWkXImfBVwy-m4rmH5MDjOcqo'

updater = Updater(token=token)
dispatcher = updater.dispatcher

symbole = {
    'Sun': '☀️',
    'Rain': '🌧',
    'Snow': '❄️',
    'Rain And Snow': '❄️🌧',
    'Showers': '🌦',
    'Scattered Showers': '🌦',
    'Partly Cloudy': '🌤',
    'Mostly Cloudy': '⛅️',
    'sturmisch': '💨',
    'Cloudy': '☁️'
}


def to_cel(f):
    return int((int(f) - 32) * 5 / 9)


def get_wetter(stadt):
    from weather import Weather
    weather = Weather()
    location = weather.lookup_by_location(stadt)
    text = ''
    forecasts = location.forecast()
    for forecast in forecasts[0:5]:
        datum = forecast.date()
        wetter = forecast.text()
        wetter = wetter + symbole.get(wetter, '')

        min = to_cel(forecast.low())
        max = to_cel(forecast.high())

        text += f"{datum} \n{wetter}\n max:{max}C° min:{min}C°\n\n"
        # print(forecast.date())
        # print(forecast.high())
        # print(forecast.low())
    return text


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hallo Welt!")


def echo(bot, update):
    stadt = update.message.text
    wetter = get_wetter(stadt)
    bot.send_message(chat_id=update.message.chat_id, text=wetter)


def vertretungsplan(bot, update):
    chat_id = update.massage.chat_id
    print('Test')
    bot.send_photo(chat_id=chat_id, photo='https://fcso-schule.de/idesk/infodisplay/img.php?pdf=1eac696ba2025e9045852bc51e722ea4-1&width=606&height=85')

handler = CommandHandler('start', start)
dispatcher.add_handler(handler)

handler = CommandHandler('abc', vertretungsplan)
dispatcher.add_handler(handler)

handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(handler)

updater.start_polling()
