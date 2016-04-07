#  -*- coding: utf-8 -*-
import urllib.request
import lxml.html
from datetime import datetime


def company(code):
    param = dict(scode=code)
    url = 'http://www.nikkei.com/markets/company/gaiyo/gaiyo.aspx?scode={scode}&ba=1'.format(**param)

    response = urllib.request.urlopen(url).read()
    root = lxml.html.fromstring(response)

    xpath_k = '//*[@id="CONTENTS_MARROW"]/div[3]/div[2]/table/tbody/tr//th'
    xpath_v = '//*[@id="CONTENTS_MARROW"]/div[3]/div[2]/table/tbody/tr//td'
    xpaths = [xpath_k, xpath_v]

    [k, v] = [[content.text for content in contents] for contents in [root.xpath(xpath) for xpath in xpaths]]

    result = dict(zip(k, v))

    def erase_kabu(s): return int(s.replace(',', '').replace(' (株)', ''))

    result['売買単位'] = erase_kabu(result['売買単位'])
    result['発行済み株式数'] = erase_kabu(result['発行済み株式数'])
    result['普通株式数（自己株除く）'] = erase_kabu(result['普通株式数（自己株除く）'])
    result['普通株式数'] = erase_kabu(result['普通株式数'])
    result['決算期'] = int(result['決算期'].replace('月', ''))

    result['指数採用'] = result['指数採用'].split(' ')
    result['上場市場名'] = result['上場市場名'].split(' ')

    result['設立年月日'] = datetime.strptime(result['設立年月日'], '%Y年%m月%d日')
    result['株主総会日'] = datetime.strptime(result['株主総会日'], '%Y年%m月%d日')

    result['資本金'] = result['資本金'].split(' ')
    result['資本金'][0] = int(result['資本金'][0].replace(',', '').replace('(百万円)', '')) * 1000000

    return result
