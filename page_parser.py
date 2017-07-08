from bs4 import BeautifulSoup
import requests
import itertools
import strings
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


def get_abit(name):
    html = requests.get(cfg.ABIT_LIST_URL).text
    soup = BeautifulSoup(html, "lxml")
    raw_rows = soup.find_all('tr', {'class': ''})
    rows = []
    for row in raw_rows:
        rows.append([el.text for el in row.find_all('td')])

    # лишняя колонка: условие поступления
    rows = [row[1:] if len(row) == 16 else row for row in rows]

    return search_abit(name, rows)


def get_new_abits():
    pass
