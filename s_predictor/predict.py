import numpy as np

class Model():
    def __init__(self, stock, dow, index, vix, mini_dow):
        self.stock = stock
        self.dow = dow
        self.index = index
        self.vix = vix
        self.mini_dow = mini_dow

        # stock & dow & mini_dow
        # Close	Mu_3_days	Price_Per	Open_Y_UP	Open_T_UP	Close_Y_UP	Vol	Vol_Per	Predict_1	Predict_2

        # index & vix
        # Price end of day	Mu_3days	Price_Per	Open_Y_UP	Open_T_UP	Close_Y_UP

        #if
        self.stock_price = self.stock[0]
        self.mu = self.stock[1]
        self.stock_vol = self.stock[6]
        self.stock_vol_per = self.stock[7]

        self.vix_per= self.vix[2]
        self.index_per= self.index[2]

        # eval data
        self.stock_data = self.stock[5]

        # testing & predict data
        self.index_close_up = self.index[5]

        self.dow_open_y_up = self.dow[3]
        self.dow_pre2 = self.dow[9]

        self.stock_open_y_up = self.stock[3]
        self.stock_close_up = self.stock[5]
        self.stock_pre1 = self.stock[8]
        self.stock_pre2 = self.stock[9]

        self.vix_open_y_up = self.vix[3]
        self.vix_close_up = self.vix[5]

        self.mini_close_up = self.mini_dow[5]

        # predict data
        self.stock_open_t_up = self.stock[4]


        ####
        self.ind_t = np.zeros(len(self.stock_data))
        # index 4 - > 3

        self.index_1_test = [self.stock_data, self.index_close_up, self.stock_open_y_up, self.vix_open_y_up]

        # index 18 -> 10

        self.index_2_test = [self.stock_data, self.stock_open_y_up, self.dow_open_y_up, self.stock_close_up]
        ####


        ####
        self.vol_t = np.zeros(len(self.stock_data))
        # Vol T, F

        self.vol_1_set = [self.stock_data, self.stock_open_y_up,self.dow_open_y_up,
                       self.vix_open_y_up]

        # Vol 2, 11 - > 7
        """
        # 11 -> 7
        self.vol_2_set = [self.dow_open_y_up, self.vix_open_y_up, self.stock_close_up, self.stock_pre1]

        """

        #21 -> 13
        self.vol_2_set = [self.stock_data,  self.stock_open_y_up,self.dow_open_y_up,
                       self.vix_open_y_up,self.stock_close_up, self.stock_pre1]


        # Vix T,F
        self.vix_set = [self.stock_data, self.stock_open_y_up,self.dow_open_y_up,
                       self.vix_open_y_up]


        ####
        self.dum_t = np.zeros(len(self.stock_data))

        # dummy1
        #self.x_test[z-2][i] == self.x_test[z-1][i] == self.x_test[z][i]== self.x_test[n+z][i] == False and (self.mu[i]-self.stock_price[i]) <=10
        self.dum_t = [self.stock_data, self.index_close_up, self.stock_open_y_up,self.dow_open_y_up,
                       self.vix_open_y_up, self.stock_pre1,self.stock_pre2]

        # dummy2
        #self.x_test[z-2][i] == self.x_test[z-1][i] == self.x_test[z][i]== self.x_test[n+z][i] == False and (self.mu[i]-self.stock_price[i]) <=10
        self.dum_tt = [self.stock_data, self.index_close_up, self.stock_open_y_up,self.dow_open_y_up,
                       self.vix_open_y_up, self.stock_pre1,self.stock_pre2]


        # Used data
        self.x_test = [self.stock_data, self.index_close_up, self.stock_open_y_up,self.dow_open_y_up,
                       self.vix_open_y_up, self.stock_pre1,self.stock_pre2,
                       ]
        """
        self.x_test = [self.stock_data, self.index_close_up, self.stock_open_y_up,self.dow_open_y_up,
                       self.vix_open_y_up,self.stock_close_up, self.stock_pre1,self.stock_pre2,
                       self.dow_pre2]
        """

        ###########testing data
        #np.insert(self.stock_data, 0, 9., axis=0)
        self.test = np.zeros(len(self.stock_data)) # dummy

        self.result = np.zeros(len(self.stock_data)) # training data

        self.real = np.zeros(len(self.stock_data))
        self.correct = np.zeros(len(self.stock_data))

        # total
        self.total = np.zeros(len(self.stock_data))

    def predict_4_one(self, data, Max1_array=[], switch = False, mu_big = True, Minus1_array=[], B1_n=0, Max2_array=[], Minus2_array=[], B2_n=0):

        max1 = [Max1_array[i] > B1_n for i in range(len(Max1_array))]
        max2 = [Max2_array[i] > B2_n for i in range(len(Max2_array))]

        minus1 = [Minus1_array[i] < B1_n for i in range(len(Minus1_array))]
        minus2 = [Minus2_array[i] < B2_n for i in range(len(Minus2_array))]


        z = 2
        count = 0
        while len(data) > z:
            for n in reversed(range(len(data[:z-1:-1]))):
                for i in range(len(data)):
                    if mu_big:
                        if switch == False:
                            if self.stock_price[i] < self.mu[i]:
                                if data[z-2][i] == data[z-1][i] == data[z][i]== data[n+z][i] == True and (self.mu[i]-self.stock_price[i]) <=10:

                                    self.result[i] += 1
                        else:

                            if len(max1):
                                if len(max2):
                                    if self.stock_price[i] < self.mu[i] and max1[i] == True and max2[i] == True:
                                            if data[z-2][i] == data[z-1][i] == data[z][i]== data[n+z][i] == True and (self.mu[i]-self.stock_price[i]) <=10:

                                                self.result[i] += 1
                                elif len(minus1):
                                    if self.stock_price[i] < self.mu[i] and max1[i] == True and minus1[i] == True:
                                        if data[z-2][i] == data[z-1][i] == data[z][i]== data[n+z][i] == True and (self.mu[i]-self.stock_price[i]) <=10:

                                                self.result[i] += 1
                                else:
                                    if self.stock_price[i] < self.mu[i] and max1[i] == True:
                                        if data[z-2][i] == data[z-1][i] == data[z][i]== data[n+z][i] == True and (self.mu[i]-self.stock_price[i]) <=10:

                                            self.result[i] += 1


                            elif len(minus1):

                                if len(minus2):
                                    if self.stock_price[i] < self.mu[i] and minus1[i] == True and minus2[i] == True:
                                            if data[z-2][i] == data[z-1][i] == data[z][i]== data[n+z][i] == True and (self.mu[i]-self.stock_price[i]) <=10:

                                                self.result[i] += 1
                                elif len(max1):
                                    if self.stock_price[i] < self.mu[i] and minus1[i] == True and max1[i] == True:
                                            if data[z-2][i] == data[z-1][i] == data[z][i]== data[n+z][i] == True and (self.mu[i]-self.stock_price[i]) <=10:

                                                self.result[i] += 1
                                else:
                                    if self.stock_price[i] < self.mu[i] and minus1[i] == True:
                                        if data[z-2][i] == data[z-1][i] == data[z][i]== data[n+z][i] == True and (self.mu[i]-self.stock_price[i]) <=10:

                                            self.result[i] += 1
                    else:
                        if switch == False:
                            if self.stock_price[i] > self.mu[i]:
                                if data[z-2][i] == data[z-1][i] == data[z][i]== data[n+z][i] == True and (self.mu[i]-self.stock_price[i]) <=10:

                                    self.result[i] += 1
                        else:

                            if len(max1):
                                if len(max2):
                                    if self.stock_price[i] > self.mu[i] and max1[i] == True and max2[i] == True:
                                            if data[z-2][i] == data[z-1][i] == data[z][i]== data[n+z][i] == True and (self.mu[i]-self.stock_price[i]) <=10:

                                                self.result[i] += 1
                                elif len(minus1):
                                    if self.stock_price[i] > self.mu[i] and max1[i] == True and minus1[i] == True:
                                        if data[z-2][i] == data[z-1][i] == data[z][i]== data[n+z][i] == True and (self.mu[i]-self.stock_price[i]) <=10:

                                                self.result[i] += 1
                                else:
                                    if self.stock_price[i] > self.mu[i] and max1[i] == True:
                                        if data[z-2][i] == data[z-1][i] == data[z][i]== data[n+z][i] == True and (self.mu[i]-self.stock_price[i]) <=10:

                                            self.result[i] += 1


                            elif len(minus1):

                                if len(minus2):
                                    if self.stock_price[i] > self.mu[i] and minus1[i] == True and minus2[i] == True:
                                            if data[z-2][i] == data[z-1][i] == data[z][i]== data[n+z][i] == True and (self.mu[i]-self.stock_price[i]) <=10:

                                                self.result[i] += 1
                                elif len(max1):
                                    if self.stock_price[i] > self.mu[i] and minus1[i] == True and max1[i] == True:
                                            if data[z-2][i] == data[z-1][i] == data[z][i]== data[n+z][i] == True and (self.mu[i]-self.stock_price[i]) <=10:

                                                self.result[i] += 1
                                else:
                                    if self.stock_price[i] > self.mu[i] and minus1[i] == True:
                                        if data[z-2][i] == data[z-1][i] == data[z][i]== data[n+z][i] == True and (self.mu[i]-self.stock_price[i]) <=10:

                                            self.result[i] += 1

            z += 1
        return self.result

    def evaluate(self,real_eval_, n):
        #real_eval_ = np.zeros(len(com))
        for i in range(len(real_eval_)):
            if real_eval_[i] != 0:
                if real_eval_[i] >= n-1:
                    self.ind_t[i] = 1
                else:
                    self.ind_t[i] = 0

        return self.ind_t


    def train_predict(self, real_data):
        dummy_t = np.zeros(len(self.stock_data))
        dummy_1 = np.zeros(len(self.stock_data))
        dummy_2 = np.zeros(len(self.stock_data))

        ## from 3 not self
        dummy_3 = np.zeros(len(self.stock_data))
        dummy_4 = np.zeros(len(self.stock_data))

        #predict_4_one(self, data, Max1_array=[],Minus1_array, B1_n=0, B1 = False, Max2_array=[], Minus2_array, B2_n=0, B2 = False)
        #max1 = [Max1_array[i] > B1_n for i in range(len(Max1_array))]
        #max2 = [Max2_array[i] > B2_n for i in range(len(Max2_array))]

        #minus1 = [Minus1_array[i] < B_n for i in range(len(Minus1_array))]
        #minus2 = [Minus2_array[i] < B2_n for i in range(len(Minus2_array))]

        # air index
        dummy_1 += self.predict_4_one(self.index_2_test, switch = True, Minus1_array=self.index_per, B1_n=-4)
        dummy_1 += self.predict_4_one(self.index_1_test, switch = True, Minus1_array=self.stock_vol, B1_n=0, Max2_array=self.index_per, B2_n=0)

        dummy_1 += self.result

        self.ind_t = self.evaluate(dummy_1, 3)
        dummy_t  += self.ind_t


        # vol_1
        dummy_2 += self.predict_4_one(self.vol_1_set, switch = True, Max1_array=self.stock_vol, B1_n=0)
        # vol_2
        #dummy_2 += self.predict_4_one(self.vol_2_set, switch = True, Max1_array=self.stock_vol, B1_n=0)

        # 4 in one
        # vol_1

        """
        z = 2
        while len(self.vol_1_set) > z:
            for n in reversed(range(len(self.vol_1_set[:z-1:-1]))):
                for i in range(len(self.stock_data)):
                    if self.stock_price[i] > self.mu[i] and self.stock_vol[i] < 0:
                        if self.vol_1_set[z-2][i] == self.vol_1_set[z-1][i] == self.vol_1_set[z][i]== self.vol_1_set[n+z][i] == True and (self.mu[i]-self.stock_price[i]) <=10:

                            self.result[i] = 1
            z += 1
        dummy_2 += self.result
        """



         # 4 in one

        z = 2
        while len(self.vol_2_set) > z:
            for n in reversed(range(len(self.vol_2_set[:z-1:-1]))):
                for i in range(len(self.stock_data)):
                    if self.stock_price[i] > self.mu[i] and self.stock_vol[i] > 0:
                        if self.vol_2_set[z-2][i] == self.vol_2_set[z-1][i] == self.vol_2_set[z][i]== self.vol_2_set[n+z][i] == True and (self.mu[i]-self.stock_price[i]) <=10:

                            self.result[i] = 1
            z += 1
        dummy_2 += self.result


        # vix
        z = 2
        while len(self.vix_set) > z:
            for n in reversed(range(len(self.vix_set[:z-1:-1]))):
                for i in range(len(self.stock_data)):
                    if self.stock_price[i] > self.mu[i] and self.vix_per[i] >-4:
                        if self.vix_set[z-2][i] == self.vix_set[z-1][i] == self.vix_set[z][i]== self.vix_set[n+z][i] == True and (self.mu[i]-self.stock_price[i]) <=10:

                            self.result[i] = 1

            z += 1
        dummy_2 += self.result
        self.vol_t = self.evaluate(dummy_2, 3)
        dummy_t  += self.vol_t



        ################################################
        ### dummy


        z = 2
        while len(self.dum_t) > z:
            for n in reversed(range(len(self.dum_t[:z-1:-1]))):
                for i in range(len(self.stock_data)):
                    if self.stock_price[i] < self.mu[i]:
                        if self.dum_t[z-2][i] == self.dum_t[z-1][i] == self.dum_t[z][i]== self.dum_t[n+z][i] == False and (self.mu[i]-self.stock_price[i]) <=10:

                            self.result[i] = 1

            z += 1
        dummy_3 += self.result


        ### dummy2


        z = 2
        while len(self.dum_tt) > z:
            for n in reversed(range(len(self.dum_tt[:z-1:-1]))):
                for i in range(len(self.stock_data)):
                    if self.stock_price[i] > self.mu[i]:
                        if self.dum_tt[z-2][i] == self.dum_tt[z-1][i] == self.dum_tt[z][i]== self.dum_tt[n+z][i] == False and (self.mu[i]-self.stock_price[i]) <=10:

                            self.result[i] = 1

            z += 1

        dummy_3 += self.result

        ### dummy3


        z = 2
        while len(self.x_test) > z:
            for n in reversed(range(len(self.x_test[:z-1:-1]))):
                for i in range(len(self.stock_data)):
                    if self.stock_price[i] < self.mu[i]:
                        if self.x_test[z-2][i] == self.x_test[z-1][i] == self.x_test[z][i]== self.x_test[n+z][i] == False and (self.mu[i]-self.stock_price[i]) <=5:

                            self.result[i] = 1

            z += 1

        dummy_3 += self.result


        ################################################


        #######################################################################
        ### dummy


        z = 2
        while len(self.dum_t) > z:
            for n in reversed(range(len(self.dum_t[:z-1:-1]))):
                for i in range(len(self.stock_data)):
                    if self.stock_price[i] < self.mu[i]:
                        if self.dum_t[z-2][i] == self.dum_t[z-1][i] == self.dum_t[z][i]== self.dum_t[n+z][i] == False:

                            self.result[i] = 1

            z += 1
        dummy_4 += self.result


        ### dummy2


        z = 2
        while len(self.dum_tt) > z:
            for n in reversed(range(len(self.dum_tt[:z-1:-1]))):
                for i in range(len(self.stock_data)):
                    if self.stock_price[i] > self.mu[i]:
                        if self.dum_tt[z-2][i] == self.dum_tt[z-1][i] == self.dum_tt[z][i]== self.dum_tt[n+z][i] == False:

                            self.result[i] = 1
            z += 1

        dummy_4 += self.result

        ### dummy3

        # 4 in one

        z = 2
        while len(self.x_test) > z:
            for n in reversed(range(len(self.x_test[:z-1:-1]))):
                for i in range(len(self.stock_data)):
                    if self.stock_price[i] > self.mu[i]:
                        if self.x_test[z-2][i] == self.x_test[z-1][i] == self.x_test[z][i]== self.x_test[n+z][i] == False:

                            self.result[i] = 1
            z += 1

        dummy_4 += self.result


        ################################################


        for i in range(len(dummy_t)):
            if dummy_t[i] != 0:
                self.total[i] += 1



        ##dummy_3 +
        for i in range(len(dummy_3)):
            if dummy_3[i] == 2 and self.total[i] != dummy_3[i]:
                self.total[i] += 1
            if dummy_3[i] == 0 and self.total[i] != dummy_3[i]:
                self.total[i] = 0

        ##dummy_4 --
        for i in range(len(dummy_4)):

            if dummy_4[i] == 1 and self.total[i] != dummy_4[i]:
                self.total[i] +=1

        #### important!! adding one zero from the begining
        self.result = np.insert(self.result, 0, 0., axis=0)
        self.total = np.insert(self.total, 0, 0., axis=0)
        dummy_3 = np.insert(dummy_3, 0, 0., axis=0)
        dummy_4 = np.insert(dummy_4, 0, 0., axis=0)


        # to get c
        c, w = 0, 0
        for i in range(len(self.total)-1):
            
            if self.total[i] == real_data[i] and self.total[i]==True:
                c += 1

        return self.result, c, self.total
