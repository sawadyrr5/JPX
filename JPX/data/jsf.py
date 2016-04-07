# -*- coding: utf-8 -*-
import urllib.request
from datetime import datetime
import numpy as np
import pandas as pd


def pcsl(date):
    """
    Download stock lending fee.
    :param date:
    :return:
    """
    result = __fetch(date, 'pcsl')

    try:
        result['貸借申込日'] = pd.to_datetime(result['貸借申込日'], format='%Y%m%d')
        result['決済日'] = pd.to_datetime(result['決済日'], format='%Y%m%d')
        result['当日品貸料率（円）'] = result['当日品貸料率（円）'].replace('*****', np.NaN)
        result['当日品貸日数'] = result['当日品貸日数'].replace('*****', np.NaN)
        result['前日品貸料率（円）'] = result['前日品貸料率（円）'].replace('*****', np.NaN)
    except(KeyError):
        result = pd.DataFrame()

    return result


def balance(date):
    """
    Download stock lending balance.
    :param date:
    :return:
    """
    result = __fetch(date, 'balance')
    result['申込日'] = pd.to_datetime(result['申込日'], format='%Y%m%d')
    return result


def __fetch(date, target):
    params = dict(
        date=datetime.strftime(date, '%Y-%m-%d'),
        target=target
    )
    url = 'http://www.jsf.co.jp/de/stock/dlcsv.php?target={target}&date={date}'.format(**params)
    response = urllib.request.urlopen(url)
    try:
        df = pd.read_csv(response, encoding='Shift_JIS', skiprows=3)
    except(pd.parser.CParserError):
        df = pd.DataFrame()
    return df
