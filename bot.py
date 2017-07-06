import telebot
import strings
import config as cfg

bot = telebot.TeleBot(cfg.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, strings.hello_mes)
