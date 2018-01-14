import datetime
import traceback

from telegram import ReplyKeyboardMarkup, ChatAction
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater, CommandHandler
from tinydb import TinyDB

token = '485681211:AAEmirKpeyBWkXImfBVwy-m4rmH5MDjOcqo'

updater = Updater(token=token)
dispatcher = updater.dispatcher

db = TinyDB('./db.json')

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


def log_error(f):
    def log(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            traceback.print_exc()
    return log


def log_command(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

    user = update.message.from_user.username
    command = update.message.text
    date = update.message.date.strftime("%Y-%m-%d %H:%M:%S")

    print("%s %s: %s" % (date, user, command))
    db.insert(dict(
        user=user,
        date=date,
        command=command
    ))


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

        text += "%s \n%s\n max:%sC° min:%sC°\n\n" % (datum, wetter, max, min)
        # print(forecast.date())
        # print(forecast.high())
        # print(forecast.low())
    return text


@log_error
def start(bot, update):
    log_command(bot, update)
    custom_keyboard = [
        ["/start"],
        ["/plan"],
        ["emden", "veenhusen"],
    ]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Hallo, ich kann dir das Wetter und den Vertretungsplan der FCSO zeigen. Grüße von Moritz",
        reply_markup=reply_markup)


@log_error
def echo(bot, update):
    log_command(bot, update)
    stadt = update.message.text
    wetter = get_wetter(stadt)
    bot.send_message(chat_id=update.message.chat_id, text=wetter)


def urls_vertretungsplan():
    from lxml import html
    import requests
    from lxml.cssselect import CSSSelector

    # Öffne Homepage
    page = requests.get('https://www.fcso.de/ueber-die-fcso/vertretungsplan.html')
    tree = html.fromstring(page.content)

    ## Lese erstes iFrame
    sel = CSSSelector('iframe')
    iframe1 = sel(tree)[0]

    # Öffne iFrame
    page = requests.get(iframe1.get('src'))
    tree = html.fromstring(page.content)

    iframe2 = sel(tree)[0]
    url = 'https://fcso-schule.de/idesk/infodisplay/' + iframe2.get('src')

    # Öffne PDF Seite
    page = requests.get(url)
    tree = html.fromstring(page.content)

    img_sel = CSSSelector('img')

    urls = []
    for img in img_sel(tree):
        img_id = img.get('alt')
        img_url = 'https://fcso-schule.de/idesk/infodisplay/img.php?pdf=' + img_id + '&width=606&height=800'
        urls.append(img_url)
    return urls


@log_error
def vertretungsplan(bot, update):
    log_command(bot, update)
    chat_id = update.message.chat_id
    for url in urls_vertretungsplan():
        bot.send_photo(chat_id=chat_id,
                       photo=url + '&date=%s' % datetime.datetime.now().isoformat())


handler = CommandHandler('start', start)
dispatcher.add_handler(handler)

handler = CommandHandler('plan', vertretungsplan)
dispatcher.add_handler(handler)

handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(handler)

updater.start_polling()
