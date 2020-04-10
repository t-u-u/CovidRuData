import logging
import datetime
import urllib.request, urllib.error
import os
import csv
import time


logger = logging.getLogger('CovidRuData.tools')


rus_months = {'января': '01',
              'февраля': '02',
              'марта': '03',
              'апреля': '04',
              'мая': '05',
              'июня': '06',
              'июля': '07',
              'августа': '08',
              'сентября': '09',
              'октября': '10',
              'ноября': '11',
              'декабря': '12',
              }


def date_from_rus_text(date_str, format):
    """
    Get date in russian string format, like "25 марта 2020" and convert to datetime
    :param date_str: 25 марта 2020
    :return: 25.03.2020
    """
    for k, v in rus_months.items():
        if k in date_str:
            date_str = date_str.replace(k, v)
    logger.debug(date_str)
    try:
        res_date = time.strptime(date_str, format)
    except Exception as e:
        logger.exception(e)
        raise e
    return res_date



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


def add_dict_to_csv(data, filepath):
    try:
        is_new_file = False
        if not os.path.exists(filepath):
            is_new_file = True
        with open(filepath, 'a+', newline='', encoding='UTF-8') as csvfile:
            fieldnames = data.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
            if is_new_file:
                writer.writeheader()
            writer.writerow(data)
    except Exception as e:
        logger.exception(e)
        raise e


def merge_csv(csvf1, csvf2, csvf_res):
    # with open('Data\\2020-03-24.csv', 'r', encoding='UTF-8') as fn:
    #     reader = csv.reader(fn, delimiter=',')
    #     fieldnames = next(reader)
        # logger.debug(fieldnames)
    #fieldnames = ['Дата','Дата обновления','Заражений за всё время','Заражений за все время, РПН','Заражений за последние сутки','Выздоровлений','Смертей','Под медицинским наблюдением','Под контролем','Тестов сделано','Москва','Московская область','Санкт-Петербург','Архангельская область', 'Белгородская область', 'Брянская область', 'Волгоградская область', 'Воронежская область', 'Забайкальский край', 'Ивановская область', 'Кабардино-Балкарская Республика', 'Калининградская область', 'Калужская область', 'Кемеровская область', 'Кировская область', 'Краснодарский край', 'Красноярский край', 'Курганская область', 'Ленинградская область', 'Липецкая область', 'Мурманская область', 'Нижегородская область', 'Новгородская область', 'Новосибирская область', 'Оренбургская область', 'Орловская область', 'Пензенская область', 'Пермский край', 'Приморский край', 'Псковская область', 'Республика Башкортостан', 'Республика Бурятия', 'Республика Дагестан', 'Республика Коми', 'Республика Крым', 'Республика Мордовия', 'Республика Саха (Якутия)', 'Республика Татарстан', 'Республика Хакасия', 'Ростовская область', 'Рязанская область', 'Самарская область', 'Саратовская область', 'Свердловская область', 'Ставропольский край', 'Тамбовская область', 'Тверская область', 'Томская область', 'Тульская область', 'Тюменская область', 'Удмуртская Республика', 'Ульяновская область', 'Хабаровский край', 'Ханты-Мансийский АО', 'Челябинская область', 'Чеченская Республика', 'Чувашская Республика', 'Ярославская область','Сумма по регионам','Сумма по регионам отличается от статистики заражений за все время']
    with open(csvf1, 'r', encoding='UTF-8') as csv1, open(csvf2, 'r', encoding='UTF-8') as csv2, open(csvf_res, 'w', newline='', encoding='UTF-8') as csv_res:
        reader1 = csv.DictReader(csv1)
        reader2 = csv.DictReader(csv2)
        fieldnames = reader2.fieldnames
        logger.debug(fieldnames)
        writer = csv.DictWriter(csv_res, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        writer.writerows(reader1)
        writer.writerows(reader2)


def add_new_csv_to_full(new_csv_path, full_csv_path):
    full_backup_path = '{0}.bak'.format(full_csv_path)
    try:
        if os.path.exists(full_backup_path):
            os.remove(full_backup_path)
        os.rename(full_csv_path, full_backup_path)
        merge_csv(full_backup_path, new_csv_path.format(datetime.date.today()), full_csv_path)
    except Exception as e:
        logger.exception()
        if os.path.exists(full_csv_path):
            os.remove(full_csv_path)
        os.rename(full_backup_path, full_csv_path)
        raise e
