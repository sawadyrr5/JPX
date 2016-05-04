import JPX.data.jsf as jsf
from datetime import datetime

d = datetime(2016, 4, 28)
res = jsf.pcsl(d)
print(res)

res = jsf.balance(d)
print(res)
