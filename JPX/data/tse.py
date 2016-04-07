#  -*- coding: utf-8 -*-
import lxml.html
import urllib.request


def price_range(price):
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

