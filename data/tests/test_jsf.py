import JPX.data.jsf as jsf
from datetime import datetime

d = datetime(2016, 3, 28)
res = jsf.pcsl(d)
print(res)

res = jsf.balance(d)
print(res)