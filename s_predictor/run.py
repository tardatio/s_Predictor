import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


import yfinance as yf
# https://towardsdatascience.com/free-stock-data-for-python-using-yahoo-finance-api-9dafd96cad2e

# from my work
from predict import Model
from util import stock_util


def geting_data():
    ## from Yahoo Finance
    #Boeing

    stock = yf.Ticker("BA")
    stock = stock.history(period="4mo")

    #Dow
    dow = yf.Ticker("^DJI")
    dow = dow.history(period="4mo")

    #Dow_futures
    mini_dow = yf.Ticker("YM=F")
    mini_dow = mini_dow.history(period="4mo")

    #Crude_oil
    crude = yf.Ticker("CL=F")
    crude = crude.history(period="4mo")

    #Vix
    vix = yf.Ticker("^VIX")
    vix = vix.history(period="4mo")

    #NYSE ARCA AIRLINE INDEX
    ind = yf.Ticker("^XAL")
    index = ind.history(period="4mo")

    ## making data
    #util = stock_util()

    make_stock = util.make_data(stock)
    make_dow = util.make_data(dow)
    make_mini_dow = util.make_data(mini_dow)
    make_crude = util.make_data(crude)
    make_vix = util.make_data_index(vix)
    make_index = util.make_data_index(index)

    stock_ = util.get_data(make_stock)
    dow_ = util.get_data(make_dow)
    mini_dow_ = util.get_data(make_mini_dow)
    crude_ = util.get_data(make_crude)
    vix_ = util.get_data(make_vix)
    index_ = util.get_data(make_index)

    # prepare
    val = [stock['Close'][i] > stock['Open'][i] for i in range(len(stock))]
    real_data = np.zeros(len(val[2:]))
    for i in range(len(real_data[2:])):
        #print(real_data[i])
        if val[i] == True:
            real_data[i] = 1

    return stock_, dow_, index_, vix_, mini_dow_, real_data

def run():

    # data
    stock_, dow_, index_, vix_, mini_dow_, real_data = geting_data()

    # Call model
    model = Model(stock_, dow_, index_, vix_, mini_dow_)

    _, correct_d, predict_data_t  = model.train_predict(real_data)


    #print(correct_d)
    print("Real_data")
    print(real_data) # real_data

    print("")
    print("")

    print("Predict_data")
    print(predict_data_t)



    util.make_chart_plot(predict_data_t, real_data, correct_d)





if __name__ == '__main__':


    util = stock_util()
    run()
