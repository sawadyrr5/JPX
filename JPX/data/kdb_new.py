# -*- coding: utf-8 -*-
import urllib.request
import lxml.html
from datetime import datetime
import pandas as pd


class __Symbol:
    # get root of category
    @classmethod
    def _get_root(cls, url):
        response = urllib.request.urlopen(url).read().decode('utf-8-sig')
        root = lxml.html.fromstring(response)
        return root

    @classmethod
    def _get_historical_price(cls, category, symbol, freq, date_from, date_to):
        date_format = {
            '1d': '%Y',
            '4h': '%Y',
            '1h': '%Y%m',
            '30m': '%Y%m',
            '15m': '%Y%m%d',
            '5m': '%Y%m%d',
        }
        dates = set(
            [datetime.strftime(date, date_format[freq]) for date in pd.date_range(date_from, date_to, freq='D')]
        )

        params = [dict(category=category, symbol=symbol, freq=freq, date=date) for date in dates]
        urls = ['http://k-db.com/{category}/{symbol}/{freq}/{date}?download=csv'.format(**param) for param in params]
        df = pd.concat(
            [_fetch_csv(url) for url in urls]
        )
        return df

    # download csv data.
    @classmethod
    def _fetch_csv(cls, url):
        df = pd.read_csv(urllib.request.urlopen(url), encoding='Shift_JIS')
        return df

    # create index.
    @classmethod
    def _indexing(cls, df, columns):
        df.columns = columns
        df.set_index('Date', inplace=True)
        df.index = pd.to_datetime(df.index)
        df.sort_index(inplace=True)
        return df

    # cut out of specified period
    @classmethod
    def _truncate(cls, df, freq, date_from, date_to):
        __sd = min(df[df.index >= date_from].index)
        __ed = max(df[df.index <= date_to].index)

        # truncate outer period
        if freq in ('1d', '4h'):
            df = df.ix[__sd:__ed]
        return df


# Parameter for futures
class Futures(__Symbol):
    __category = 'futures'

    __col = dict(
        dsohlcv=('Date', 'Session', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dollar_Volume'),
        dtohlcv=('Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dollar_Volume')
    )
    __columns = {
        '1d': __col['dsohlcv'],
        '4h': __col['dtohlcv'],
        '1h': __col['dtohlcv'],
        '30m': __col['dtohlcv'],
        '15m': __col['dtohlcv'],
        '5m': __col['dtohlcv']
    }

    def __init__(self):
        url = 'http://k-db.com/futures/'
        root = self._get_root(url)

        xpath_symbols = '//*[@id="maintable"]/tbody//tr/td[4]/a/@href'
        self.symbols = [symbol.replace('/' + self.__category + '/', '') for symbol in root.xpath(xpath_symbols)]

        xpath_names = '//*[@id="maintable"]/tbody//tr/td[1]'
        self.names = dict(zip(self.symbols, [name.text for name in root.xpath(xpath_names)]))

        xpath_contracts = '//*[@id="maintable"]/tbody//tr/td[4]/a'
        self.contracts = dict(zip(self.symbols, [name.text for name in root.xpath(xpath_contracts)]))

    def get_historical_price(self, symbol, freq, date_from, date_to):
        df = self._get_historical_price(self.__category, symbol, freq, date_from, date_to)
        df = self._indexing(df, self.__columns[freq])
        df = self._truncate(df, freq, date_from, date_to)
        return df


# Parameter for indices
class Indices(__Symbol):
    __category = 'indices'

    __col = dict(
        dohlc=('Date', 'Open', 'High', 'Low', 'Close'),
        dsohlc=('Date', 'Session', 'Open', 'High', 'Low', 'Close'),
        dtohlc=('Date', 'Time', 'Open', 'High', 'Low', 'Close')
    )
    __columns = {
            '1d': __col['dohlc'],
            '4h': __col['dsohlc'],
            '1h': __col['dtohlc'],
            '30m': __col['dtohlc'],
            '15m': __col['dtohlc'],
            '5m': __col['dtohlc']
        }

    def __init__(self):
        url = 'http://k-db.com/indices/'
        root = self._get_root(url)

        xpath_symbols = '//*[@id="maintable"]/tbody//tr/td[1]/a/@href'
        self.symbols = [symbol.replace('/' + self.__category + '/', '') for symbol in root.xpath(xpath_symbols)]

        xpath_names = '//*[@id="maintable"]/tbody//tr/td[1]/a'
        self.names = dict(zip(self.symbols, [name.text for name in root.xpath(xpath_names)]))

    def get_historical_price(self, symbol, freq, date_from, date_to):
        df = self._get_historical_price(self.__category, symbol, freq, date_from, date_to)
        df = self._indexing(df, self.__columns[freq])
        df = self._truncate(df, freq, date_from, date_to)
        return df


# Parameter for stocks
class Stocks(__Symbol):
    __category = 'stocks'

    __col = dict(
        dohlcv=('Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dollar_Volume'),
        dsohlcv=('Date', 'Session', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dollar_Volume'),
        dtohlcv=('Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dollar_Volume')
    )

    __columns = {
        '1d': __col['dohlcv'],
        '4h': __col['dsohlcv'],
        '1h': __col['dtohlcv'],
        '30m': __col['dtohlcv'],
        '15m': __col['dtohlcv'],
        '5m': __col['dtohlcv']
    }

    def __init__(self):
        url = 'http://k-db.com/stocks/'
        root = self._get_root(url)

        xpath_symbols = '//*[@id="maintable"]/tbody//tr/td[1]/a/@href'
        self.symbols = [symbol.replace('/' + self.__category + '/', '') for symbol in root.xpath(xpath_symbols)]

        xpath_names = '//*[@id="maintable"]/tbody//tr/td[1]/a'
        self.names = dict(zip(self.symbols, [name.text for name in root.xpath(xpath_names)]))

    def get_historical_price(self, symbol, freq, date_from, date_to):
        df = self._get_historical_price(self.__category, symbol, freq, date_from, date_to)
        df = self._indexing(df, self.__columns[freq])
        df = self._truncate(df, freq, date_from, date_to)
        return df


# Parameter for statistics
class Statistics(__Symbol):
    __category = 'statistics'

    __col = dict(
        stat=('Date', 'Volume', 'DollarVolume', 'Numbers', 'Pricing', 'Up', 'Unchange', 'Down', 'Incomparable')
    )

    __columns = {
        '1d': __col['stat']
    }

    def __init__(self):
        url = 'http://k-db.com/statistics/'
        root = self._get_root(url)

        xpath_symbols = '//*[@id="maintable"]/tbody//tr/td[1]/a/@href'
        self.symbols = [symbol.replace('/' + self.__category + '/', '') for symbol in root.xpath(xpath_symbols)]

        xpath_names = '//*[@id="maintable"]/tbody//tr/td[1]/a'
        self.names = dict(zip(self.symbols, [name.text for name in root.xpath(xpath_names)]))

    def get_historical_price(self, symbol, freq, date_from, date_to):
        df = self._get_historical_price(self.__category, symbol, freq, date_from, date_to)
        df = self._indexing(df, self.__columns[freq])
        df = self._truncate(df, freq, date_from, date_to)
        return df


if __name__ == '__main__':
    sd = datetime(2016, 3, 1)
    ed = datetime(2016, 4, 22)

    # 先物
    mykdb = Futures()
    res = mykdb.symbols
    print(res)  # コード一覧
    res = mykdb.names
    print(res)  # 名称一覧
    res = mykdb.contracts
    print(res)  # 限月一覧
    # res = mykdb.get_historical_price('F101-0000', '1d', sd, ed)
    # print(res.head(10))  # プライス一覧

    # 指数
    mykdb = Indices()
    res = mykdb.symbols
    print(res)  # コード一覧
    res = mykdb.names
    print(res)  # 名称一覧
    # res = mykdb.get_historical_price('I101', '1d', sd, ed)
    # print(res.head(10))  # プライス一覧

    # 個別株
    mykdb = Stocks()
    res = mykdb.symbols
    print(res)  # コード一覧
    res = mykdb.names
    print(res)  # 名称一覧
    # res = mykdb.get_historical_price('I101', '1d', sd, ed)
    # print(res.head(10))  # プライス一覧

    # 統計
    mykdb = Statistics()
    res = mykdb.symbols
    print(res)  # コード一覧
    res = mykdb.names
    print(res)  # 名称一覧
    # res = mykdb.get_historical_price('I101', '1d', sd, ed)
    # print(res.head(10))  # プライス一覧
