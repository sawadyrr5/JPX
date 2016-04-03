import JPX.data.kdb as kdb
from datetime import datetime

d_start = datetime(2014, 3, 14)
d_end = datetime(2015, 3, 20)
d_date = datetime(2016, 3, 18)

#    u_symbol = 'F101-1606'  #future
#    u_symbol = 'I101'       #index
u_symbol = '9984-T'  # stock
#    u_symbol = 'T1'         #stat

# u_df = myKDB.hist(u_symbol, 'm', d_start, d_end)
u_df = kdb.historical(u_symbol, 'd', d_start, d_end)


print('----')
print(u_df)

u_symbol = '8411-T'  # stock
#    u_symbol = 'T1'         #stat

# u_df = myKDB.hist(u_symbol, 'm', d_start, d_end)
u_df = kdb.historical(u_symbol, 'd', d_start, d_end)
print('----')
print(u_df)