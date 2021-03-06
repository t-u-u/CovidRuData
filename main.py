import logging
import datetime
import os
import time
from tools import merge_csv, add_dict_to_csv, get_webpage, add_new_csv_to_full
from yandex_map import parse_yandex_covid
from rpn import get_report_url


yandex_url = 'https://yandex.ru/web-maps/covid19'
rpn_url = 'https://www.rospotrebnadzor.ru/about/info/news/'


logger = logging.getLogger('CovidRuData')


def logger_settings():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler('logs\{0}.log'.format(datetime.date.today()), encoding="UTF-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)


def main():
    page = get_webpage(yandex_url)
    data = parse_yandex_covid(page)
    if not os.path.exists('Data'):
        os.makedirs('Data')
    add_dict_to_csv(data, r'Data\{0}.csv'.format(datetime.date.today()))
    add_new_csv_to_full(r'Data\{0}.csv'.format(datetime.date.today()), 'CovidRuStat.csv')


logger_settings()
main()
# page = get_webpage(rpn_url)
# date = time.strptime("29 03 2020", "%d %m %Y")
# get_report_url(page, date)
# add_new_csv_to_full(r'Data\2020-03-30.csv', 'CovidRuStat.csv')
