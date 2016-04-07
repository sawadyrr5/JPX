import JPX.data.toushin as ts
from datetime import datetime

isin = 'JP90C000A931'

res = ts.attrib(isin)
print(res)

start = datetime(2015, 1, 1)
end = datetime(2015, 12, 31)

res = ts.nav(isin, start, end)
print(res)

res = ts.performance(isin, start, end, 1000000)
print(res)
