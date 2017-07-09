import threading
import datetime
import time
import page_parser as pp
import database as db


def update():
    clk = int(time.time())
    delta = 3600  # every hour
    while True:
        _clk = int(time.time())
        if _clk - clk >= delta:
            clk = int(time.time())
            date = str(datetime.datetime.now()).split(' ')[0]
            if date != db.get_date():
                db.set_date(date)
                db.update_abits(pp.get_abits_names())


def run():
    t = threading.Thread(target=update)
    t.start()
    t.join()
