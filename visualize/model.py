import time
import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt
# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.layers import LSTM


## cai tien voi loss function moi
# def loss_func(y_true, y_pred):
#     squared_difference = tf.square(y_true - y_pred)
#     sign = tf.sign(y_true - y_pred)
#     mean = tf.reduce_mean(squared_difference, axis=-1)
#     if sign < 0:
#         return mean * 1.2


# Chỉ dùng thuộc tính close để train => input shape=30, 1
def train(name, data):
    # chuẩn hóa
    print(data.shape)
    scaler = StandardScaler()
    scaled = scaler.fit_transform(data[:, 1:2])  # chỉ lấy thuộc tính close
    index = int(2*scaled.shape[0]/3)  # Train 2/3 data
    # X_train = scaled[0:index]  # 
    
    X_train=np.array(list(scaled[i:30+i] for i in range(index))) #Train 2/3 data
    y_train = scaled[30:index+30]
    X_train = np.reshape(X_train, (index, 30, 1))

    # Model
    regressor = Sequential()
    
    # cửa sổ 30, số chiều dữ liệu 1
    regressor.add(LSTM(units=1, activation='sigmoid', input_shape=(30, 1)))
    regressor.add(Dense(units=1))

    regressor.compile(optimizer='adam', loss='mean_squared_error')
    history = regressor.fit(X_train, y_train, batch_size=4, epochs=100)

    regressor.save(name+'.h5')
    print('Saved ' + name)




def predict(name, data):
    model = load_model(name+'.h5')
    
    scaler = StandardScaler()
    scaled = scaler.fit_transform(data[:, 2:3])  # chỉ lấy thuộc tính close

    inputs = np.array([scaled[-30:]])
    inputs = np.reshape(inputs, (inputs.shape[0], 30, 1))
    
    predicted_stock_price = model.predict(inputs)  # predict
    predicted_stock_price = scaler.inverse_transform(predicted_stock_price)
    
    return {'predicted' : str(predicted_stock_price[0][0])}
    


def test_model(name, data):
    model = load_model(name+'.h5')

    scaler = StandardScaler()
    scaled = scaler.fit_transform(data[:, 2:3])  # chỉ lấy thuộc tính close

    index = int(2*scaled.shape[0]/3)
    inputs = np.array([scaled[index-30+i: index+i] for i in range(index//2)])
    inputs = np.reshape(inputs, (inputs.shape[0], 30, 1))
    
    predicted_stock_price = model.predict(inputs)  # predict
    predicted_stock_price = scaler.inverse_transform(predicted_stock_price)
    predicted_stock_price = predicted_stock_price.reshape(inputs.shape[0])

    real_stock_price = data[index:, 2:3].reshape(inputs.shape[0])  # real from data
    past_stock_price = data[index-1:-1, 2:3].reshape(inputs.shape[0])  # real from data
    
    ### cac chi so danh gia
    loss = 0  # loss
    accumulation = 0  # true rate
    total = 0   # real play
    for i in range(len(real_stock_price)):
        loss += predicted_stock_price[i]-real_stock_price[i]
        if np.sign((predicted_stock_price[i]-past_stock_price[i]) * (real_stock_price[i]-past_stock_price[i])) == 1:
            accumulation += 1
    print('Sum loss: '+str(loss))
    print('True rate:', accumulation/len(real_stock_price)) # tỉ lệ dự báo đúng hướng (lên, xuống)

    n_day = 3
    profit_rate = np.zeros(len(real_stock_price)-n_day)
    for i in range(len(real_stock_price)-n_day):
        future = i + n_day
        predict_true = np.sign((predicted_stock_price[future]-past_stock_price[i]) * (
            real_stock_price[future]-past_stock_price[i]))  # 1 if true else -1
        profit = np.abs(real_stock_price[future]-past_stock_price[i])
        if predicted_stock_price[future] - past_stock_price[i] > 0:
            total += predict_true * profit
        profit_rate[i] = profit / past_stock_price[i]
    
    print('Total earned money:', total) # tổng tiền kiếm được nếu chơi theo dự đoán của model (tăng thì mua) và bán sau n ngày
    print('Profit rate:', np.mean(profit_rate))  # tỉ lệ lãi/ vốn
    
    infor = {'predicted': list(map(float, predicted_stock_price)), 
             'Sum loss': loss, 
             'True rate:': accumulation/len(real_stock_price), 
             'Total earned money:': total, 
             'Profit rate:': np.mean(profit_rate)
            }
    return infor

    # plt.plot(real_stock_price[:], color='red', label='Real Stock Price')
    # plt.plot(predicted_stock_price[:],
    #          color='green', label='Predicted Stock Price')
    # plt.title('Stock Price Prediction '+name)
    # plt.xlabel('time')
    # plt.ylabel('Stock Price')
    # plt.legend()
    # plt.show()

