from pymongo import MongoClient
import config as cfg

client = MongoClient(cfg.MONGODB_URI)
db = client[cfg.DATABASE]


def get_db_abits():
    return [abit['name'] for abit in db.abits.find({})]


def update_abits(new_abits):
    db.abits.delete_many({})
    db.abits.insert_many([{'name': abit} for abit in new_abits])


def get_date():
    try:
        return db.time.find({})[0]['date']
    except IndexError:
        return ""


def set_date(new_date):
    db.time.delete_many({})
    db.time.insert_one({'date': new_date})
