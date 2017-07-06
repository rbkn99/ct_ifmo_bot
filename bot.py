from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import os
import strings
import page_parser as pp
import config as cfg

updater = Updater(token=cfg.TOKEN)
dispatcher = updater.dispatcher

wait_for_abit_mode = False


def hello(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=strings.hello_mes)


def send_stats(bot, update):
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
    bot.send_message(chat_id=update.message.chat_id, text=stats)


def search(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=strings.wait_abit_mes)
    global wait_for_abit_mode
    wait_for_abit_mode = True


def send_faq(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=strings.faq)


def handle_message(bot, update):
    global wait_for_abit_mode
    if not wait_for_abit_mode:
        return

    wait_for_abit_mode = False
    abits = pp.get_abit(update.message.text)
    if len(abits) == 0:
        bot.send_message(chat_id=update.message.chat_id, text=strings.not_found_mes)
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
    bot.send_message(chat_id=update.message.chat_id, text=result_text)


dispatcher.add_handler(CommandHandler('start', hello))
dispatcher.add_handler(CommandHandler('help', hello))
dispatcher.add_handler(CommandHandler('stats', send_stats))
dispatcher.add_handler(CommandHandler('search', search))
dispatcher.add_handler(CommandHandler('faq', send_faq))
dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

updater.start_webhook(listen="0.0.0.0",
                      port=int(os.environ.get('PORT', '5000')),
                      url_path=cfg.TOKEN)
updater.bot.set_webhook(cfg.HOST + cfg.TOKEN)
updater.idle()
