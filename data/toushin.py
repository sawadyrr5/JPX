# -*- coding: utf-8 -*-
import urllib.request
import pandas as pd
from datetime import datetime, timedelta
import lxml.html
import decimal


def attrib(isin):
    params = dict(isinCd=isin)
    url = 'http://tskl.toushin.or.jp/FdsWeb/view/FDST030000.seam?isinCd={isinCd}'.format(**params)

    response = urllib.request.urlopen(url).read()
    root = lxml.html.fromstring(response)

    xpaths = ('//*[@id="contents"]/div[2]/div/table[1]//label',
              '//*[@id="contents"]/div[2]/div/table[3]//label',
              '//*[@id="contents"]//table[@class="dividend"]//label')

    labels = [[t.text.replace('\n', '') for t in l] for l in [root.xpath(x) for x in xpaths]]

    result = dict()
    result['ISIN'] = isin
    result['決算日'] = labels[0][0]
    result['インデックス型'] = labels[0][1]
    result['信託報酬'] = labels[0][2]
    result['単位'] = labels[0][3]
    result['設定日'] = labels[0][4]
    result['カテゴリ1'] = labels[0][5]
    result['カテゴリ2'] = labels[0][6]
    result['ファンド名'] = labels[0][7]
    result['ファンド略名'] = labels[0][8]
    result['委託会社'] = labels[0][9]

    result['独立区分'] = labels[1][0]
    result['投資対象資産'] = labels[1][1]
    result['資産属性'] = labels[1][2]
    result['償還日'] = labels[1][4]

    result['信託報酬(委託)'] = labels[2][0]
    # 無報酬の場合は'購入手数料'が取れず要素数が5になる
    if len(labels[2]) == 5:
        result['購入手数料'] = 0
        result['信託財産留保金'] = labels[2][1]
        result['信託報酬(販売)'] = labels[2][3]
        result['信託報酬(受託)'] = labels[2][4]
    else:
        result['購入手数料'] = labels[2][1]
        result['信託財産留保金'] = labels[2][2]
        result['信託報酬(販売)'] = labels[2][4]
        result['信託報酬(受託)'] = labels[2][5]

    return result


def nav(isin, date_from, date_end):
    date_est = datetime.strptime(attrib(isin)['設定日'], '%Y/%m/%d')
    date_from = max([date_from, date_est])

    base_url = ('http://tskl.toushin.or.jp/FdsWeb/view/FDST030004.seam?isinCd={isinCd}'
               '&stdDateFromY={sy}&stdDateFromM={sm}&stdDateFromD={sd}&stdDateToY={ey}'
               '&stdDateToM={em}&stdDateToD={ed}&showFlg=csv&adminFlag=2')
    k = ['sy', 'sm', 'sd', 'ey', 'em', 'ed']

    result = pd.DataFrame()
    while True:
        date_to = date_from + timedelta(days=90)
        if date_to > date_end:
            date_to = date_end

        v = [date_from.year, date_from.month, date_from.day, date_to.year, date_to.month, date_to.day]
        v = [str(s).zfill(2) for s in v]
        params = dict(zip(k, v))
        params['isinCd'] = isin

        url = base_url.format(**params)
        response = urllib.request.urlopen(url)

        try:
            df = pd.read_csv(response, encoding='Shift_JIS')
        except:
            df = pd.DataFrame()
        result = result.append(df)

        date_from = date_to + timedelta(days=1)
        if date_from > date_end:
            break

    result.columns = ('日付', '基準価格', '純資産', '分配金', '決算期')
    result['日付'] = pd.to_datetime(result['日付'], format='%Y年%m月%d日')
    result.set_index('日付', inplace=True)

    return result


def performance(isin, start, end, amount_money):
    k = ['sy', 'sm', 'sd', 'ey', 'em', 'ed']
    v = [str(s).zfill(2) for s in [start.year, start.month, start.day, end.year, end.month, end.day]]
    args = dict(zip(k, v))
    args['isinCd'] = isin
    args['buyAmntMoney'] = amount_money

    url = ('http://tskl.toushin.or.jp/FdsWeb/view/FDST030002.seam?isinCd={isinCd}&'
           'initFlag=1&stdDateFromY={sy}&stdDateFromM={sm}&stdDateFromD={sd}&'
           'stdDateToY={ey}&stdDateToM={em}&stdDateToD={ed}&buyAmntMoney={buyAmntMoney}').format(**args)

    html = urllib.request.urlopen(url).read()
    root = lxml.html.fromstring(html)

    xpath = '//div[@id="showList"]/table[2]/tr[2]//td'
    cnts = root.xpath(xpath)

    k = ['所有期間損益', '分配金累計', '所有期間損益(分配金含む)', '収益率(年換算)']
    try:
        v = [float(c.text_content().replace(',', '').replace('円', '')) for c in [cnts[0], cnts[1], cnts[2]]]
        v.append(float(cnts[3].text_content().replace('%', '').replace('\n', '')) / 100)
        result = dict(zip(k, v))
    except IndexError:
        result = dict()

    return result
