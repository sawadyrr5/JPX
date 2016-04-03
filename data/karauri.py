# -*- coding: utf-8 -*-
import urllib.request
import lxml.html
import pandas as pd
from JPX.util.convert import str2num


def institutional(code):
    param = dict(code=code)

    url = 'http://karauri.net/{code}/'.format(**param)
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
    xpath_column = '//*[@id="sort"]/thead/tr/th'

    datas = [root.xpath(xpath) for xpath in xpaths]

    ser2 = [pd.Series([d.text for d in data]) for data in datas]

    # ser2[0] = pd.Series(data=[d.text) for d in datas[0]])
    ser2[2] = pd.Series([str2num(d.text) for d in datas[2]])
    ser2[3] = pd.Series([str2num(d.text) for d in datas[3]])
    ser2[4] = pd.Series([d.text.replace('株', '').replace(',', '') for d in datas[4]])
    ser2[5] = pd.Series([str2num(d.text) for d in datas[5]])

    df = pd.DataFrame(data=ser2)
    df = df.transpose()

    columns = root.xpath(xpath_column)
    df.columns = [col.text for col in columns]

    df['計算日'] = pd.to_datetime(df['計算日'])

    return df
