from JPX.data.kdb_new import Futures, Indices, Stocks, Statistics
from datetime import datetime

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
res = mykdb.get_historical_price('1301-T', '1d', sd, ed)
print(res.head(10))  # プライス一覧

# 統計
mykdb = Statistics()
res = mykdb.symbols
print(res)  # コード一覧
res = mykdb.names
print(res)  # 名称一覧
# res = mykdb.get_historical_price('T1', '1d', sd, ed)
# print(res.head(10))  # プライス一覧