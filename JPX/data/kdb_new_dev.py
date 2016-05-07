# -*- coding: utf-8 -*-
import urllib.request
import lxml.html
from datetime import datetime
import pandas as pd


class __SymbolType:
    _url = str()
    _category = str()
    _session = dict()
    _col_order = dict()
    _xpath = dict(
        symbol='',
        name='',
        contract=''
    )

    def __init__(self):
        response = urllib.request.urlopen(self._url).read().decode('utf-8-sig')
        root = lxml.html.fromstring(response)

        def root_parse(xpath):
            return [e.text for e in root.xpath(xpath)]

        try:
            self.symbols = [symbol.split('/')[-1] for symbol in root.xpath(self._xpath['symbol'])]
        except KeyError:
            pass

        try:
            self.names = dict(zip(self.symbols, root_parse(self._xpath['name'])))
        except KeyError:
            pass

        try:
            self.contracts = dict(zip(self.symbols, root_parse(self._xpath['contract'])))
        except KeyError:
            pass

    def price(self, date_from: datetime, date_to: datetime, symbol=None, session=None, freq=None) -> pd.DataFrame:
        """
        Download historical data of specified symbol. or all symbols.
        :param symbol:
            Specify symbol. if not specified, get all symbols.
        :param session:
            Specify session.
        :param freq:
            Specify frequency.
        :param date_from:
        :param date_to:
        :return: pandas.DataFrame
        """
        if symbol is not None:
            web = _Single(category=self._category, date_from=date_from, date_to=date_to, symbol=symbol, freq=freq)
        else:
            web = _All(category=self._category, date_from=date_from, date_to=date_to, session=session)

        df = pd.concat(
            [_fetch_csv(url) for url in web.url()]
        )
        if symbol is not None:
            df = df[self._col_order[freq]]
        if symbol is None:
            pass

        return df


class __Historical:
    base_url = str()
    params = dict()
    date_from = None
    date_to = None

    def dates(self, date_format):
        return set(
            [datetime.strftime(date, date_format) for date in pd.date_range(self.date_from, self.date_to, freq='D')]
        )

    def url(self):
        return [self.base_url.format(**param) for param in self.params]


class _Single(__Historical):
    base_url = 'http://k-db.com/{category}/{symbol}/{freq}/{date}?download=csv'
    format_table = {'1d': '%Y', '4h': '%Y', '1h': '%Y%m', '30m': '%Y%m', '15m': '%Y%m%d', '5m': '%Y%m%d'}

    def __init__(self, category, date_from, date_to, symbol, freq):
        self.date_from = date_from
        self.date_to = date_to
        self.params = [dict(category=category, date=date, symbol=symbol, freq=freq) for date in self.dates(format_table[f])]


class _All(__Historical):
    base_url = 'http://k-db.com/{category}/{date}{session}?download=csv'
    date_format = '%Y-%m-%d'

    def __init__(self, category, date_from, date_to, session):
        self.date_from = date_from
        self.date_to = date_to
        self.params = [dict(category=category, date=date, session=session) for date in self.dates(self.date_format)]


def _fetch_csv(url):
    try:
        df = pd.read_csv(urllib.request.urlopen(url), encoding='Shift_JIS')
    except ValueError:
        df = pd.DataFrame()
    return df


class Futures(__SymbolType):
    _category = 'futures'
    _session = {'e': '/e'}
    __dtohlcv = ['日付', '時刻', '始値', '高値', '安値', '終値', '出来高', '売買代金']
    _col_order = {
        "1d": __dtohlcv,
        "4h": __dtohlcv,
        "1h": __dtohlcv,
        "30m": __dtohlcv,
        "15m": __dtohlcv,
        "5m": __dtohlcv
    }
    _url = 'http://k-db.com/futures/'
    _xpath = dict(
        symbol='//*[@id="maintable"]/tbody//tr/td[4]/a/@href',
        name='//*[@id="maintable"]/tbody//tr/td[1]',
        contract='//*[@id="maintable"]/tbody//tr/td[4]/a'
    )


class Indices(__SymbolType):
    _category = 'indices'
    _session = {'a': '/a', 'b': '/b'}
    __dtohlc = ['日付', '時刻', '始値', '高値', '安値', '終値']
    _col_order = {
        "1d": ['日付', '始値', '高値', '安値', '終値'],
        "4h": __dtohlc,
        "1h": __dtohlc,
        "30m": __dtohlc,
        "15m": __dtohlc,
        "5m": __dtohlc
    }
    _url = 'http://k-db.com/indices/'
    _xpath = dict(
        symbol='//*[@id="maintable"]/tbody//tr/td[1]/a/@href',
        name='//*[@id="maintable"]/tbody//tr/td[1]/a'
    )


class Stocks(__SymbolType):
    _category = 'stocks'
    _session = {'a': '/a', 'b': '/b'}
    __dtohlcv = ['日付', '時刻', '始値', '高値', '安値', '終値', '出来高', '売買代金']
    _col_order = {
        "1d": ['日付', '始値', '高値', '安値', '終値', '出来高', '売買代金'],
        "4h": __dtohlcv,
        "1h": __dtohlcv,
        "30m": __dtohlcv,
        "15m": __dtohlcv,
        "5m": __dtohlcv
    }
    _url = 'http://k-db.com/stocks/'
    _xpath = dict(
        symbol='//*[@id="maintable"]/tbody//tr/td[1]/a/@href',
        name='//*[@id="maintable"]/tbody//tr/td[1]/a'
    )


class Statistics(__SymbolType):
    _category = 'statistics'
    _session = None
    _col_order = {
        "1d": ['日付', '出来高', '売買代金', '銘柄数', '値付き', '値上がり', '変わらず', '値下がり', '比較不可']
    }
    _url = 'http://k-db.com/statistics/'
    _xpath = dict(
        symbol='//*[@id="maintable"]/tbody//tr/td[1]/a/@href',
        name='//*[@id="maintable"]/tbody//tr/td[1]/a'
    )


# TEST
sd = datetime(2015, 4, 25)
ed = datetime(2016, 4, 25)

myc = Stocks()
s = '1301-T'
f = '1d'

res = myc.price(date_from=sd, date_to=ed, symbol=s, freq=f)
print(res)



# res = myc.symbols
# print(res)
#
# res = myc.names
# print(res)
#
# res = myc.contracts
# print(res)
