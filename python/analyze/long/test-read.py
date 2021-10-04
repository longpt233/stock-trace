import pandas as pd

data= pd.read_csv("../../../data/vndirect/all/ACB.csv")
data.columns= ['date', 'adjust', 'close', 'change_perc', 'avg',
                        'volume_match', 'value_match', 'volume_reconcile', 'value_reconcile',
                        'open', 'high', 'low', 'volume']

print(data.head(5))