# JPX
国内の投資関係データを扱うためのライブラリ

## JPX.data.jsf
日本証券金融HPから品貸料率と貸借残高を取得する。

### 品貸料率を取得する
```
import JPX.data.jsf as jsf
jsf.pcsl(date)
```

### 貸借残高を取得する

```
import JPX.data.jsf as jsf
jsf.balance(date)
```


## JPX.data.karauri
karauri.netから機関の空売り情報を取得する

### 機関の空売り情報を取得する

```
import JPX.data.karauri as kara
kara.institutional(code)
```

## JPX.data.kdb
k-db.comから時系列データを取得する

### 個別株、先物、指数、統計の時系列データを取得する

```
import JPX.data.kdb as kdb
kdb.historical(symbol, interval=None, start=None, end=None)
```


## JPX.data.nikkei
日本経済新聞HPから会社情報を取得する

### 会社情報を取得する

```
import JPX.data.nikkei as nk
nk.company(code)
```


## JPX.data.toushin
投信協会HPから投信関連情報を取得する

### 属性情報を取得する

```
import JPX.data.toushin as ts
ts.attrib(isin)
```


### 基準価格を取得する

```
import JPX.data.toushin as ts
ts.nav(isin, date_from, date_end)
```


### 収益率を取得する

```
import JPX.data.toushin as ts
ts.performance(isin, start, end, amount_money)
```


## JPX.data.tse
東証HPから情報を取得する

### 値幅制限を取得する

```
import JPX.data.tse as tse
tse.price_range(price)
```
