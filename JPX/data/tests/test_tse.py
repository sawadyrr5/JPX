import JPX.data.tse as tse

# example
last_price = 50000000
range = tse.price_range(last_price)
print(last_price)
print(range)

res = tse.includes('Core30')
print(res)