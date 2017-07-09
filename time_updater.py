import threading
import datetime
import time
import page_parser as pp
import database as db


def update():
    print(777)
    while True:
        time.sleep(3600)
        date = str(datetime.datetime.now()).split(' ')[0]
        if date != db.get_date():
            db.set_date(date)
            db.update_abits(pp.get_abits_names())


def run():
    print(228)
    t = threading.Thread(target=update)
    print(228228)
    t.start()
    print(228322)

