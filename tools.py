import logging
import datetime
import urllib.request, urllib.error
import os
import csv


logger = logging.getLogger('CovidRuData.tools')


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
    fieldnames = ['Дата','Дата обновления','Заражений за всё время','Заражений за все время, РПН','Заражений за последние сутки','Выздоровлений','Смертей','Под медицинским наблюдением','Под контролем','Тестов сделано','Москва','Московская область','Санкт-Петербург','Архангельская область', 'Белгородская область', 'Брянская область', 'Волгоградская область', 'Воронежская область', 'Забайкальский край', 'Ивановская область', 'Кабардино-Балкарская Республика', 'Калининградская область', 'Калужская область', 'Кемеровская область', 'Кировская область', 'Краснодарский край', 'Красноярский край', 'Курганская область', 'Ленинградская область', 'Липецкая область', 'Мурманская область', 'Нижегородская область', 'Новгородская область', 'Новосибирская область', 'Оренбургская область', 'Орловская область', 'Пензенская область', 'Пермский край', 'Приморский край', 'Псковская область', 'Республика Башкортостан', 'Республика Коми', 'Республика Крым', 'Республика Саха (Якутия)', 'Республика Татарстан', 'Республика Хакасия', 'Ростовская область', 'Рязанская область', 'Самарская область', 'Саратовская область', 'Свердловская область', 'Ставропольский край', 'Тамбовская область', 'Тверская область', 'Томская область', 'Тульская область', 'Тюменская область', 'Удмуртская Республика', 'Ульяновская область', 'Хабаровский край', 'Ханты-Мансийский АО', 'Челябинская область', 'Чеченская Республика', 'Чувашская Республика', 'Ярославская область','Сумма по регионам','Сумма по регионам отличается от статистики заражений за все время']
    with open(csvf1, 'r', encoding='UTF-8') as csv1, open(csvf2, 'r', encoding='UTF-8') as csv2, open(csvf_res, 'w', newline='', encoding='UTF-8') as csv_res:
        reader1 = csv.DictReader(csv1)
        reader2 = csv.DictReader(csv2)
        writer = csv.DictWriter(csv_res, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        writer.writerows(reader1)
        writer.writerows(reader2)