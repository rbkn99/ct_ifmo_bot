import threading
import datetime
import time
import page_parser as pp
import database as db


def update():
    while True:
        date = str(datetime.datetime.now()).split(' ')[0]
        if date != db.get_date():
            db.set_date(date)
            db.update_abits(pp.get_abits_names())
        time.sleep(3600)


def run():
    t = threading.Thread(target=update)
    t.start()

