from bs4 import BeautifulSoup
import requests
import itertools
import strings
import database as db
import config as cfg


def get_current_stats():
    html = requests.get(cfg.STATS_URL).text
    soup = BeautifulSoup(html, 'lxml')
    rows = soup.find_all('tr')
    ami_rows = list(filter(lambda row: strings.ami in str(row), rows))
    data = []
    for row in ami_rows:
        data.append([el.text for el in row.find_all('td')])
    data[0][0] += " (бюджет)"
    data[1][0] += " (контракт)"
    return data


def search_abit(name, abits_list):
    name_parts = list(itertools.permutations(name))
    result = []
    for part in name_parts:
        result += list(filter(lambda x: ' '.join(part).lower() in x[2].lower(), abits_list))
    return result


def get_all_abits():
    html = requests.get(cfg.ABIT_LIST_URL).text
    soup = BeautifulSoup(html, "lxml")
    raw_rows = soup.find_all('tr', {'class': ''})
    rows = []
    for row in raw_rows:
        rows.append([el.text for el in row.find_all('td')])
    # лишняя колонка: условие поступления
    rows = [row[1:] if len(row) == 16 else row for row in rows]
    return rows


def get_abits_names():
    return [abit[2] for abit in get_all_abits()]


def get_abit(name):
    return search_abit(name, get_all_abits())


def get_new_abits():
    abits = get_all_abits()
    abits_names = get_abits_names()
    db_abits_names = db.get_db_abits()
    new_abits = []
    for abit in abits_names:
        if abit not in db_abits_names:
            new_abits.append(search_abit(abit, abits)[0])
    return new_abits
