import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class stock_util(object):

    def __init__(self):
        pass

    def make_data(self, stock):

        # 3 days before to mean
        mu = []
        for n,i in enumerate(stock['Close']):
            if n > 1:
                mu.append((stock['Close'][n-2]+stock['Close'][n-1]+stock['Close'][n]).mean()/3)

        # Stock Price per
        stock_per = [(stock['Close'][i] - stock['Open'][i]) / stock['Close'][i] * 100 for i in range(len(stock['Open']))]

        # Stock vol %
        stock_t_vol = stock['Volume'][2:]
        stock_y_vol = stock['Volume'][1:-1]
        stock_per_vol = [(t - y) / t * 100 for t,y in zip(stock_t_vol, stock_y_vol)]


        #Today open up and close upper & vol down than yester vol  -> tomorrow down
        stock_op = stock['Open'][2:]
        stock_cl = stock['Close'][2:]

        pre1 = [op < cl and t_vol < y_vol for op, cl, t_vol, y_vol in zip(stock_op, stock_cl, stock_t_vol,stock_y_vol)]

        pre2 =[]
        pre_che = stock['Close'][2:]
        for i in range(len(stock_per_vol)):
            if stock_per_vol[i] > 0:
                pre2.append(True)

            else:
                pre2.append(False)


        # make data
        data = pd.DataFrame(data=stock['Close'][2:], index=stock.index[2:])

        data['mu'] = mu
        data["per"] = stock_per[2:]

        open_t = stock['Open'][2:]
        close_y = stock['Close'][1:-1]
        close_t = stock['Close'][2:]
        data['open_y_up'] = [t > y for t,y in zip(open_t, close_y)]

        data["open_t_up"] = stock['Open'][2:] < stock['Close'][2:]

        data["Close_y_up"] = [t > y for t,y in zip(close_t, close_y)]

        data['vol'] = stock["Volume"][2:]
        data['vol_per'] = stock_per_vol
        data['predict'] = pre1
        data['predict2'] = pre2
        data.columns = ["Close",
                        "Mu_3_days",
                        "Price_Per",
                        "Open_Y_UP",
                        "Open_T_UP",
                        "Close_Y_UP",
                        "Vol",
                        "Vol_Per",
                        "Predict_1",
                        "Predict_2"]

        return data

    def make_data_index(self, index):

        # 3 days before to mean
        mu = []
        for n,i in enumerate(index['Close']):
            if n > 1:
                mu.append((index['Close'][n-2]+index['Close'][n-1]+index['Close'][n]).mean()/3)

        # Stock Price per
        index_per = [(index['Close'][i] - index['Open'][i]) / index['Close'][i] * 100 for i in range(len(index['Open']))]

        # make data
        data = pd.DataFrame(data=index['Close'][2:], index=index.index[2:])

        data['mu'] = mu
        data["per"] = index_per[2:]

        open_t = index['Open'][2:]
        close_y = index['Close'][1:-1]
        close_t = index['Close'][2:]

        data['open_y_up'] = [t > y for t,y in zip(open_t, close_y)]
        data["open_t_up"] = index['Open'][2:] < index['Close'][2:]
        data["Close_y_up"] = [t > y for t,y in zip(close_t, close_y)]

        data.columns = ["Price end of day",
                        "Mu_3days",
                        "Price_Per",
                        "Open_Y_UP",
                        "Open_T_UP",
                        "Close_Y_UP"]

        return data

    def get_data(self, data):
        dato = np.zeros((len(data.columns), len(data)))
        for x, title in enumerate(data.columns):
            for y in range(len(dato[x])):
                dato[x][y] = data[title][y]
        return dato


    def make_bool(self, up_down):
        correct, wrong = 0, 0
        for i in up_down:
            if i == True:
                correct +=1
            else:
                wrong +=1
        return [correct, wrong]


    def make_chart_plot(self, date, predict, real, correct_d):

        predict_dato = self.make_bool(predict[:-1])
        real_dato = self.make_bool(real)

        real_dato_0 = real_dato[0]
        predict_dato_0 = predict_dato[0]

        total_up = real_dato_0


        if predict_dato_0 < real_dato_0:

            total_up +=  (real_dato_0 - predict_dato_0)

        else:
            total_up += (predict_dato_0 - real_dato_0)

        #correct_d = correct_d+2



        data = [correct_d, total_up-correct_d] # bool(0) == False

        #plot
        label = f'True: {data[0]}', f'False: {data[1]}'
        explode = (0.1, 0)
        colors = ['#99ff99','#ff9999','#66b3ff','#ffcc99']

        plt.title(f"The Percentage of Up in The Target Stock (4 months): {total_up}")
        plt.pie(data,labels=label,explode=explode, autopct='%1.1f%%', colors= colors, startangle=90)


        if int(predict[-1]) == 0:
            plt.xlabel("When the market in {} will close, Target Stock is Down".format(date))
        else:
            plt.xlabel("When the market in {} will close, Target Stock is Up".format(date))

        plt.legend()

        plt.show()
