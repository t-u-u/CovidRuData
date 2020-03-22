import xml.etree.ElementTree as ET1
from lxml import etree as ET
import logging
import time


logger = logging.getLogger('CovidRuData.yandex_map')


def parse_yandex_date(subtitle: str):
    """
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


def parse_yandex_item():
    pass


def parse_yandex_covid(data):
    date_xpath = '//div[@class="covid-panel-view__subtitle"]'
    data_xpath = '//div[@class="covid-panel-view__item"]'
    res = {}

    try:
        parser = ET.HTMLParser()
        tree = ET.XML(data, parser)
        ya_date = parse_yandex_date(tree.xpath(date_xpath)[0].text)
        res.update({'Дата обновления': time.strftime('%d-%m-%Y %H:%M', ya_date)})

        # ya_items = tree.xpath(data_xpath)
        # for item in ya_items:
        #     name = item.xpath('//div[@class="covid-panel-view__item-name"]')[0].text
        #     cases = item.xpath('//div[@class="covid-panel-view__item-cases"]')[0].text
        #     res.update({name: cases})

        names = tree.xpath('//div[@class="covid-panel-view__item-name"]')
        cases = tree.xpath('//div[@class="covid-panel-view__item-cases"]')

        if len(names) != len(cases):
            raise ValueError("Parsing error: number of names isn't equal to the number of cases")

        for i in range(len(names)):
            res.update({names[i].text: cases[i].text})


    except Exception as e:
        logger.exception(e.reason)
        raise e

    return res