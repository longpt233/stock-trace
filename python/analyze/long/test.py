import investpy
import datetime
import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler

start = '01/06/2009'
end = datetime.datetime.now().strftime("%d/%m/%Y")

company = "ACB"

# df = investpy.get_stock_historical_data(stock=company, country='VietNam', from_date=start, to_date=end)
# df.to_csv(f'{company}-origin.csv')
df = pd.read_csv("ACB-origin.csv")


print(df.head(5))

df['H-L'] = df['High'] - df['Low']
df['O-C'] = df['Open'] - df['Close']
ma_1 = 7
ma_2 = 14
ma_3 = 21
df[f'SMA_{ma_1}'] = df['Close'].rolling(window=ma_1).mean()
df[f'SMA_{ma_2}'] = df['Close'].rolling(window=ma_2).mean()
df[f'SMA_{ma_3}'] = df['Close'].rolling(window=ma_3).mean()

df[f'SD_{ma_1}'] = df['Close'].rolling(window=ma_1).std()
df[f'SD_{ma_3}'] = df['Close'].rolling(window=ma_3).std()

df.dropna(inplace=True)     # inplace or replace 
df.drop(columns='Currency',inplace=True)


print(df.head(5))

pre_day = 30
scala_x = MinMaxScaler(feature_range=(0, 1))
scala_y = MinMaxScaler(feature_range=(0, 1))
cols_x = ['H-L', 'O-C', f'SMA_{ma_1}', f'SMA_{ma_2}', f'SMA_{ma_3}', f'SD_{ma_1}', f'SD_{ma_3}']
cols_y = ['Close']

scaled_data_x = scala_x.fit_transform(df[cols_x].values.reshape(-1, len(cols_x)))
print(scaled_data_x[1])

scaled_data_y = scala_y.fit_transform(df[cols_y].values.reshape(-1, len(cols_y)))

x_total = []
y_total = []

for i in range(pre_day, len(df)):
    x_total.append(scaled_data_x[i-pre_day:i])
    y_total.append(scaled_data_y[i])

test_size = 365

x_train = np.array(x_total[:len(x_total)-test_size])
x_test = np.array(x_total[len(x_total)-test_size:])
y_train = np.array(y_total[:len(y_total)-test_size])
y_test = np.array(y_total[len(y_total)-test_size:])

print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)