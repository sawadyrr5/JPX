#  -*- coding: utf-8 -*-
import lxml.html
import urllib.request
import re


__topix = topix()


def price_range(price):
    """
    引数に渡した価格に対して制限値幅を返す
    :param price:
    :return:
    """
    url = 'http://www.jpx.co.jp/equities/trading/domestic/06.html'
    response = urllib.request.urlopen(url).read()
    root = lxml.html.fromstring(response)

    xpath_prices = '//*[@id="readArea"]/div[4]/div/table//tr/td[1]'
    xpath_ranges = '//*[@id="readArea"]/div[4]/div/table//tr/td[2]'

    prices = root.xpath(xpath_prices)
    ranges = root.xpath(xpath_ranges)

    def clear(s): return s.replace('円', '').replace('未満', '').replace('以上', '').replace('上下', '').replace(',', '')
    prices = [int(clear(p.text)) for p in prices[1:]]
    ranges = [int(clear(r.text)) for r in ranges[1:]]

    for p, r in zip(prices, ranges):
        if price < p:
            return r
        elif price >= prices[-1]:
            return ranges[-1]


def newindex(code):
    return __topix.newindex[code]


def float_ratio(code):
    return __topix.float_ratio[code]


def weight(code):
    return __topix.weight[code]


def includes(newindex):
    return __topix.includes[newindex]


class topix():
    """
    使い方

    1. 準備
    http://www.jpx.co.jp/markets/indices/topix/tvdivq00000030ne-att/list-j.pdf
    をDLして、スクリプトと同じ場所にlist-j.txtとして保存。(Acrobat Readerのtxt保存)
    """
    def __init__(self):
        re_date = re.compile(r"\d{4}/\d{2}/\d{2}")

        self.result = dict()
        for line in open('list-j.txt', 'r'):
            matchOB = re_date.match(line)
            if matchOB:
                line = line.replace('Small ', 'Small').replace('○ ', '').replace('-', '- ').replace('\n', '')
                line = line.replace(matchOB.group(), matchOB.group() + ' ')
                l = line.split(' ')
                self.result[l[2]] = dict(
                    newindex=l[3],
                    float_ratio=l[4],
                    weight=l[5]
                )

    def newindex(self, code):
        return self.result[code]['newindex']

    def float_ratio(self, code):
        return self.result[code]['float_ratio']

    def weight(self, code):
        return self.result[code]['weight']

    def includes(self, newindex):
        result = [code for code in self.result if self.result[code]['newindex'] == newindex]
        return result