import logging
import datetime
import urllib.request, urllib.error
import os
import csv
from yandex_map import parse_yandex_covid


yandex_url = 'https://yandex.ru/web-maps/covid19'


logger = logging.getLogger('CovidRuData')


def logger_settings():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler('logs\{0}.log'.format(datetime.date.today()), encoding = "UTF-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)


def get_webpage(url):
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as response:
            return response.read()
    except urllib.error.HTTPError as e:
        logger.error("Error: {0}\n=======\n{1}\n=======\n{2}".format(e.code, e.reason, e.read()))
        raise e
    except urllib.error.URLError as e:
        logger.error("'{0}' is incorrect or not available\n{1}".format(url, e.reason))
        raise e


def dict_to_csv(data, filepath):
    try:
        with open(filepath, 'w', newline='', encoding='UTF-8') as csvfile:
            fieldnames = data.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
            writer.writeheader()
            writer.writerow(data)
    except Exception as e:
        logger.exception(e)
        raise e


def main():
    logger_settings()
    page = get_webpage(yandex_url)
    data = parse_yandex_covid(page)
    dict_to_csv(data, 'CovidRuStat.csv')

main()
# logger_settings()
# logger.error('123')
# print(parse_yandex_date("22 марта 2020, 16:27 (по московскому времени)↵источники: Роспотребнадзор, WHO, US CDC, China NHC, ECDC, DXY"))
