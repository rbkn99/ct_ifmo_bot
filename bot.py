import telebot
import strings
import os
from flask import Flask
import page_parser as pp
import config as cfg

bot = telebot.TeleBot(cfg.TOKEN)

wait_for_abit_mode = False


@bot.message_handler(commands=['start', 'help'])
def send_hello_message(message):
    bot.send_message(message.chat.id, strings.hello_mes)


@bot.message_handler(commands=['stats'])
def send_stats(message):
    raw_stats = pp.get_current_stats()
    stats = ""
    tab4 = "\t\t\t\t"
    tab8 = tab4 * 2
    for stat in raw_stats:
        stats += "Конкурсная группа: {0}\n" \
                 "Кол. мест: {1}\n" \
                 "Заявления\n" \
                 "%sВсего: {2}\n" \
                 "%sБВИ: {3}\n" \
                 "%sПо номерам\n" \
                 "%s1: {4}\n" \
                 "%s2: {5}\n" \
                 "%s3: {6}\n\n".format(*stat) % (tab4, tab4, tab4, tab8, tab8, tab8)
    bot.send_message(message.chat.id, stats)


@bot.message_handler(commands=['search'])
def send_details(message):
    bot.send_message(message.chat.id, strings.wait_abit_mes)
    global wait_for_abit_mode
    wait_for_abit_mode = True


@bot.message_handler(commands=['faq'])
def send_faq(message):
    bot.send_message(message.chat.id, strings.faq)


@bot.message_handler(content_types=['text'])
def handle_message(message):
    global wait_for_abit_mode
    if not wait_for_abit_mode:
        bot.send_message(message.chat.id, strings.error_mes)
        return

    wait_for_abit_mode = False
    abits = pp.get_abit(message.text)
    if len(abits) == 0:
        bot.send_message(message.chat.id, strings.not_found_mes)
        return

    tab4 = "\t\t\t\t"
    result_text = ""
    for abit in abits:
        abit = ['-' if el == '' else el for el in abit]
        result_text += "№ п/п: {0}\n" \
                       "Номер заявления: {1}\n" \
                       "ФИО: {2}\n" \
                       "Вступительные испытания\n" \
                       "%sВид: {3}\n" \
                       "%sМатематика: {4}\n" \
                       "%sРусский язык: {5}\n" \
                       "%sИнформатика: {6}\n" \
                       "%sЕГЭ + ИД: {7}\n" \
                       "%sЕГЭ: {8}\n" \
                       "%sИД: {9}\n" \
                       "Наличие оригинала документов: {10}\n" \
                       "Наличие согласия на зачисление: {11}\n" \
                       "Преимущественное право: {12}\n" \
                       "Олимпиада: {13}\n" \
                       "Статус: {14}\n\n".format(*abit) % (tab4, tab4, tab4, tab4, tab4, tab4, tab4)
    bot.send_message(message.chat.id, result_text)

app = Flask(__name__)
context = (cfg.SSL_CERT, cfg.SSL_PRIV)


@app.route('/')
def hello():
    return 'Hello World!'


if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=cfg.HOST, certificate=open(cfg.SSL_CERT, 'rb'))

    app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
