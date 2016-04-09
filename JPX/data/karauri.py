# -*- coding: utf-8 -*-
import urllib.request
import lxml.html
import pandas as pd
from JPX.util.convert import str2num


def institutional(code, kikan_code=None):
    param = dict(
        code=code,
        kikan_code=''
    )

    if kikan_code:
        param['kikan_code'] = '?f=' + kikan_code

    url = 'http://karauri.net/{code}/{kikan_code}'.format(**param)
    html = urllib.request.urlopen(url).read()
    root = lxml.html.fromstring(html)

    xpaths = [
        '//*[@id="sort"]/tbody/tr/td[1]',
        '//*[@id="sort"]/tbody/tr/td[2]/a',
        '//*[@id="sort"]/tbody/tr/td[3]',
        '//*[@id="sort"]/tbody/tr/td[4]',
        '//*[@id="sort"]/tbody/tr/td[5]',
        '//*[@id="sort"]/tbody/tr/td[6]',
        '//*[@id="sort"]/tbody/tr/td[7]'
    ]
    datas = [root.xpath(xpath) for xpath in xpaths]

    ser2 = [pd.Series([d.text for d in data]) for data in datas]

    ser2[2] = pd.Series([str2num(d.text) for d in datas[2]])
    ser2[3] = pd.Series([str2num(d.text) for d in datas[3]])
    ser2[4] = pd.Series([d.text.replace('株', '').replace(',', '') for d in datas[4]])
    ser2[5] = pd.Series([str2num(d.text) for d in datas[5]])

    df = pd.DataFrame(data=ser2)
    df = df.transpose()

    columns = ('Date', 'Name', 'Short_pct', 'Short_pct_chg', 'Short_amount', 'Short_amount_chg', 'Note')
    df.columns = columns

    df['Date'] = pd.to_datetime(df['Date'])

    return df
