# -*- coding: utf-8 -*-
import pandas as pd
import urllib.request
from datetime import datetime

__response = urllib.request.urlopen('http://k-db.com/?p=all&download=csv')
__master = pd.read_csv(__response, encoding='Shift_JIS', skiprows=1)
__master.set_index('コード', inplace=True)


def symbols():
    """
    Return all symbols.
    """
    result = list(__master.index)
    return result


def historical(symbol, interval=None, start=None, end=None):
    """
    Download historical data of stock, future, index and statistics from k-db.com.

    :param symbol: stock, index, future or statistics symbol
    :param interval: d, a, m5, m
    :param start: when interval is 'd' or 'a', start date.
                  when interval is 'm5' or 'm', specify date.
    :param end: when interval is 'd' or 'a', end date.
                when interval is 'm5' or 'm', ignored.
    :return: pandas.DataFrame
    """
    if isinstance(start, datetime):
        if isinstance(end, datetime) and interval in ('d', 'a') and start > end:
            end = start
    else:
        return

    # make url list
    urls = __make_urls(symbol, interval, start, end)

    # fetch by url list
    df = pd.concat([__fetch_csv(url) for url in urls])

    # set index
    df = __set_index(df, symbol, interval)

    # truncate outer period
    if interval in ('d', 'a'):
        result = df.ix[start:end]
    else:
        result = df
    return result


class __SymbolType:
    # define columns sequence.
    column_type = dict(
        all=('Symbol', 'Name', 'Exchange', 'Sector', 'Open', 'High', 'Low', 'Close', 'Volume', 'DollarVolume'),
        day=('Date', 'Open', 'High', 'Low', 'Close'),
        day_v=('Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'DollarVolume'),
        session=('Date', 'Session', 'Open', 'High', 'Low', 'Close'),
        session_v=('Date', 'Session', 'Open', 'High', 'Low', 'Close', 'Volume', 'DollarVolume'),
        minute=('Date', 'Time', 'Open', 'High', 'Low', 'Close'),
        minute_v=('Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'DollarVolume'),
        statistics=('Date', 'Volume', 'DollarVolume', 'Numbers', 'Pricing', 'Up', 'Unchange', 'Down', 'Incomparable')
    )

    # define index sequence.
    index_type = dict(
        day=['Date'],
        session=['Date', 'Session'],
        minute=['Date', 'Time']
    )

    @property
    def index(self):
        return

    @property
    def column(self):
        return


class __Stocks(__SymbolType):
    category = 'stocks'

    def __init__(self, interval):
        self.interval = interval
        return

    @property
    def index(self):
        result = dict(
            d=self.index_type['day'],
            a=self.index_type['session'],
            m5=self.index_type['minute'],
            m=self.index_type['minute']
        )
        return result[self.interval]

    @property
    def column(self):
        result = dict(
            d=self.column_type['day_v'],
            a=self.column_type['session_v'],
            m5=self.column_type['minute_v'],
            m=self.column_type['minute_v']
        )
        return result[self.interval]


class __Indices(__SymbolType):
    category = 'indices'

    def __init__(self, interval):
        self.interval = interval
        return

    @property
    def index(self):
        result = dict(
            d=self.index_type['day'],
            a=self.index_type['session'],
            m5=self.index_type['minute']
        )
        return result[self.interval]

    @property
    def column(self):
        result = dict(
            d=self.column_type['day'],
            a=self.column_type['session'],
            m5=self.column_type['minute']
        )
        return result[self.interval]


class __Futures(__SymbolType):
    category = 'futures'

    def __init__(self, interval):
        self.interval = interval
        return

    @property
    def index(self):
        result = dict(
            d=self.index_type['session'],
            a=self.index_type['session'],
            m5=self.index_type['minute'],
            m=self.index_type['minute']
        )
        return result[self.interval]

    @property
    def column(self):
        result = dict(
            d=self.column_type['session_v'],
            a=self.column_type['session_v'],
            m5=self.column_type['minute_v'],
            m=self.column_type['minute_v']
        )
        return result[self.interval]


class __Statistics(__SymbolType):
    category = 'statistics'

    def __init__(self, interval):
        self.interval = interval
        return

    @property
    def index(self):
        result = dict(
            d=self.index_type['day']
        )
        return result[self.interval]

    @property
    def column(self):
        result = dict(
            d=self.column_type['statistics'],
        )
        return result[self.interval]


def __get_symbol_type(symbol, interval):
    # define statistic symbols
    symbols_stat = (
        'T1', 'T2', 'TM', 'JQS',
        'T1-I201', 'T1-I202', 'T1-I203', 'T1-I204', 'T1-I205', 'T1-I206', 'T1-I207', 'T1-I208', 'T1-I209', 'T1-I210',
        'T1-I211', 'T1-I212', 'T1-I213', 'T1-I214', 'T1-I215', 'T1-I216', 'T1-I217', 'T1-I218', 'T1-I219', 'T1-I220',
        'T1-I221', 'T1-I222', 'T1-I223', 'T1-I224', 'T1-I225', 'T1-I226', 'T1-I227', 'T1-I228', 'T1-I229', 'T1-I230',
        'T1-I231', 'T1-I232', 'T1-I233'
    )

    if symbol in symbols_stat:
        result = __Statistics(interval)
    elif any(__master[__master['業種'] == '先物'].index.isin([symbol])):
        result = __Futures(interval)
    elif any(__master[__master['業種'] == '指数'].index.isin([symbol])):
        result = __Indices(interval)
    else:
        result = __Stocks(interval)

    return result


# set index
def __set_index(df, symbol, interval):
    symbol_type = __get_symbol_type(symbol, interval)  # select historical data type

    df.columns = symbol_type.column  # set column name
    if interval in ('d', 'a'):
        df.set_index(pd.to_datetime(df['Date']), inplace=True)
        df.drop('Date', axis=1, inplace=True)
    elif interval in ('m5', 'm'):
        df['Date'] = df['Date'] + ' ' + df['Time']
        df.set_index(pd.to_datetime(df['Date']), inplace=True)
        df.drop(symbol_type.index, axis=1, inplace=True)

    result = df.sort_index(ascending=True)
    return result


# making url string.
def __make_urls(symbol, interval, start, end):
    symbol_type = __get_symbol_type(symbol, interval)

    url_base = 'http://k-db.com/{category}/{symbol}{interval}?{date}download=csv'
    url_interval = dict(
        d='',
        a='/a',
        m5='/5min',
        m='/minutely'
    )
    params = [dict(
        category=symbol_type.category,
        symbol=symbol,
        interval=url_interval[interval],
        date=date
    ) for date in __make_date_string(interval, start, end)]

    result = [url_base.format(**param) for param in params]
    return result


# making date part string.
def __make_date_string(interval, start, end):
    if interval in ('d', 'a') and isinstance(start, datetime) and isinstance(end, datetime):
        result = ['year=' + str(year) + '&' for year in range(start.year, end.year + 1)]
    elif interval in ('m5', 'm') and isinstance(start, datetime):
        result = ['date=' + datetime.strftime(start, '%Y-%m-%d') + '&']
    else:
        result = []

    return result


# fetch csv data from k-db.com
def __fetch_csv(url):
    response = urllib.request.urlopen(url)
    result = pd.read_csv(response, encoding='Shift_JIS', skiprows=1)
    return result
