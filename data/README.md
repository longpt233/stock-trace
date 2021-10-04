# DataStock

## Structure

```
data     
|--company        
|   |-- company-list.csv : crawl all company + company here [link](https://vn.tradingview.com/markets/stocks-vietnam/sectorandindustry-sector/)+category   
|   |-- category : vietsub category, **category v1**   : [link](https://vn.tradingview.com/markets/stocks-vietnam/sectorandindustry-sector/)       
|       
|--vndirect       
|   |-- all : DATA main      [link]("https://finfo-api.vndirect.com.vn/v4/stock_prices?sort=date&size=3994&page=1&q=code:AAM&date:gte=2010-10-10date:lte=2021-09-15")      
|   |-- csv-10-30 : data company price about 10~30       
|       
|--crawl-category : new **category v2**     

```




## Read data
``` python 
import pandas as pd

data= pd.read_csv("../../../data/vndirect/all/ACB.csv")
data.columns= ['date', 'adjust', 'close', 'change_perc', 'avg', 'volume_match', 'value_match', 'volume_reconcile', 'value_reconcile', 'open', 'high', 'low', 'volume']

print(data.head(5))

         date  adjust  close  change_perc   avg  volume_match   value_match  volume_reconcile  value_reconcile  open  high   low     volume
0  2013-01-03   5.078   17.0      -1.7341  17.0     1967200.0  3.379012e+10             163.0     2.624300e+06  17.5  17.8  16.7  1967363.0
1  2013-01-04   5.138   17.2       1.1765  17.1     1170100.0  1.989316e+10              95.0     1.510500e+06  16.9  17.2  16.7  1170195.0
2  2013-01-07   5.138   17.2       0.5848  17.1     1355700.0  2.333590e+10             402.0     6.432000e+06  17.0  17.5  17.0  1356102.0
3  2013-01-08   5.168   17.3       1.1696  17.1     2180000.0  3.749339e+10             418.0     6.688000e+06  17.1  17.5  16.9  2180418.0
4  2013-01-09   5.409   18.1       5.8480  18.1     3861400.0  6.945910e+10          100302.0     1.724832e+09  17.1  18.2  17.1  3961702.0

> volume = volume_match + volume_reconcile
```