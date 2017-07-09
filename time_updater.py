import threading
import datetime
import time
import page_parser as pp
import database as db


def update():
    while True:
        print(1)
        date = str(datetime.datetime.now()).split(' ')[0]
        print(2)
        if date != db.get_date():
            print(3)
            db.set_date(date)
            print(4)
            db.update_abits(pp.get_abits_names())
            print(5)
        time.sleep(3600)


def run():
    t = threading.Thread(target=update)
    t.start()

