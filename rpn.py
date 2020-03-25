import logging
from lxml import etree as ET
from tools import date_from_rus_text


report_name = 'Информационный бюллетень о ситуации и принимаемых мерах по недопущению распространения заболеваний, вызванных новым коронавирусом'


logger = logging.getLogger('CovidRuData.rpn')


def get_report_url(data, date):
    report_xpath = '//a[contains(text(),"{0}")]'.format(report_name)
    try:
        parser = ET.HTMLParser()
        tree = ET.XML(data, parser)
        for item in tree.xpath(report_xpath):
            cur_date_raw = item.getnext().text
            cur_date = date_from_rus_text(cur_date_raw, '%d %m %Y г.')
            logger.debug(cur_date)
            logger.debug(date)
            if cur_date == date:
                url = 'https://www.rospotrebnadzor.ru{0}'.format(item.get('href'))
                logger.info("Report for the date {0} is found\n{1}: {2}".format(date, cur_date_raw, url))
                return url
        logger.info("Report for the date {0} is not found".format(date))
        return
    except Exception as e:
        logger.exception(e)
        raise e
