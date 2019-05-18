import config
import const
import io
import vedisdb as db
import telebot
from flask import Flask, request

bot = telebot.TeleBot(config.TOKEN)
app = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, %s. А как тебя по настоящему зовут?' % message.from_user.first_name)
    db.set_user_state(message.chat.id, const.STATE_NAME)


@bot.message_handler(func=lambda message: db.get_user_state(message.chat.id) == const.STATE_NAME)
def name_state(message):
    bot.send_message(message.chat.id, 'Очень приятно %s, а сколько тебе лет?' % message.text)
    db.set_user_state(message.chat.id, const.STATE_AGE)


@bot.message_handler(func=lambda message: db.get_user_state(message.chat.id) == const.STATE_AGE)
def age_state(message):
    if message.text.isdigit():
        age = int(message.text)
        if age < 18:
            bot.send_message(message.chat.id, 'Ты слишком молод =(')
            db.set_user_state(message.chat.id, const.STATE_DEFAULT)
        else:
            bot.send_message(message.chat.id, 'Ты слишком стар =(')
            db.set_user_state(message.chat.id, const.STATE_DEFAULT)
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю, попробуй еще раз ввести свой возраст')
    


@app.route("/{}".format(config.TOKEN), methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=config.URL + config.TOKEN)
    return 'Привет, я случайный чат бот. Ты можешь пообщаться со мной в telegram @', 200
