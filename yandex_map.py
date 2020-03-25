from lxml import etree as ET
import logging
import time


logger = logging.getLogger('CovidRuData.yandex_map')


def parse_yandex_date(subtitle: str):
    """
    Takes date from yandex map subtitle, and convert it to datetime.
    :param subtitle: "22 марта 2020, 16:27 (по московскому времени)↵источники: Роспотребнадзор, WHO, US CDC, China NHC, ECDC, DXY"
    :return: '22.03.2020 16:27': datetime
    """
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
    logger.info('Parsing subtitle: "{0}"'.format(subtitle))
    date_str = subtitle.split('(')[0].strip()
    for k, v in rus_months.items():
        if k in date_str:
            date_str = date_str.replace(k, v)
    logger.debug(date_str)
    try:
        res_date = time.strptime(date_str, '%d %m %Y, %H:%M')
    except Exception as e:
        logger.exception(e.read())
        raise e
    return res_date


def parse_yandex_covid(data):
    """
    Get data about number of covid cases per Russian region from yandex covid map
    :param data:
    :return:
    """
    date_xpath = '//div[@class="covid-panel-view__subtitle"]'
    data_xpath = '//div[@class="covid-panel-view__item"]'
    stat_xpath = '//div[@class="covid-panel-view__stat-item-value"]'
    names_xpath = '//div[@class="covid-panel-view__item-name"]'
    cases_xpath = '//div[@class="covid-panel-view__item-cases"]'
    res = {}

    try:
        parser = ET.HTMLParser()
        tree = ET.XML(data, parser)
        ya_date = parse_yandex_date(tree.xpath(date_xpath)[0].text)
        res.update({'Дата': time.strftime('%d-%m-%Y', ya_date)})
        res.update({'Дата обновления': time.strftime('%d-%m-%Y %H:%M', ya_date)})
        stats = tree.xpath(stat_xpath)
        res.update({'Заражений за всё время': stats[0].text})
        res.update({'Заражений за все время, РПН': ''})
        res.update({'Заражений за последние сутки': stats[1].text})
        res.update({'Выздоровлений': stats[2].text})
        res.update({'Смертей': stats[3].text})
        res.update({'Под медицинским наблюдением': ''})
        res.update({'Под контролем': ''})
        res.update({'Тестов сделано': ''})

        names = tree.xpath(names_xpath)
        cases = tree.xpath(cases_xpath)
        cases_total = 0
        if len(names) != len(cases):
            raise ValueError("Parsing error: number of names isn't equal to the number of cases")
        for i in range(len(names)):
            res.update({names[i].text: cases[i].text})
            cases_total = cases_total + int(cases[i].text)
        res.update({'Сумма по регионам': cases_total})
        if cases_total != int(res['Заражений за всё время']):
            logger.warning('{2}: Сумма по регионам ({0}) отличается от статистики заражений за все время ({1})'.format(cases_total, res['Заражений за всё время'], res['Дата']))
            res.update({'Сумма по регионам отличается от статистики заражений за все время': 'true'})

    except Exception as e:
        logger.exception(e.reason)
        raise e

    return res