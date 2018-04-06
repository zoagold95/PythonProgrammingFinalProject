import pandas as pd
import numpy as np
import random

class WhatIf:

    def __init__(self, Dp, Av, Az, Cont):
        self.Dp = Dp
        self.Av = Av
        self.Az = Az
        self.cryptoCurrencyTracker = Cont
        self.WData = self.Av.Weighted
        self.WData.index = pd.to_datetime(self.WData.index)

    def readAmazonData(self):
        Proj = self.Dp.proj_loc
        self.Data = pd.read_csv(Proj +'/scraped_data.csv', sep = ',')

    def whatIf(self):
        last = len(self.WData) - 1
        dummy = self.WData.index
        dates = dummy.astype('str')
        marketvals = ['Open', 'Close', 'High', 'Low', 'open', 'close', 'high', 'low']
        print('Fill in the blanks:')
        print('What if I bought on <Date1> at <market value1> and sold on <Date2> at <market value2>?')

        print('Date1 (YYYY-MM-DD) between {} and {}'.format(self.WData.index[0].date(),self.WData.index[last].date()))
        self.date1 = self.handleDateInput(input(), dates)


        print('Select a market value: Open, Close, High or Low.')
        self.marketval1 = input()
        if self.marketval1 not in marketvals:
            self.handleInput(self.marketval1, marketvals)

        print('Date2 (YYYY-MM-DD) between your first date and {}'.format(self.WData.index[last].date()))
        self.date2 = self.handleDateInput(input(), dates)

        print('Select a market value: Open, Close, High or Low.')
        self.marketval2 = input()
        if self.marketval2 not in marketvals:
            self.handleInput(self.marketval2, marketvals)

    def valueComparison(self):
        earned = round(self.WData.loc[self.date2,self.marketval2] - self.WData.loc[self.date1, self.marketval1], 2)
        if earned <= 0:
            print('Sorry you\'ve lost ${}'.format(abs(earned)))
            return
        randomitem = random.randint(0,len(self.Data)-1)
        itemprice = float(self.PriceToInt(self.Data.loc[randomitem, 'SALE_PRICE']))

        counter = 0
        while itemprice > earned:
            counter += 1
            randomitem = random.randint(0,len(self.Data)-1)
            itemprice = float(self.PriceToInt(self.Data.loc[randomitem, 'SALE_PRICE']))
            if counter >= 20:
                itemprice = -999999999
                break

        countprice = itemprice
        #determining number of items
        count = 1
        if itemprice == -999999999:
            print('Congrats! You earned ${}, however this is not enough to have purchased any of the items we have price info for.'.format(earned))
        else:
            while countprice <= earned - (earned * .05):
                count += 1
                countprice = countprice + itemprice

            if countprice >= earned:
                count -= 1
                countprice = countprice - itemprice

            moneyleft = round(earned - countprice, 2)
            print('If you had bought at {} on {} and sold at {} on {}, you would have made ${}'.format(self.marketval1, self.date1.date(), self.marketval2, self.date2.date(), earned))
            print('That\'s the same as {} {}, with ${} leftover'.format(count, self.Data.loc[randomitem, 'NAME'], moneyleft))


    def handleInput(self, sel, acceptable):
        while sel not in acceptable:
            print('That is not a valid input, please try again.')
            sel = input()
        return sel

    def handleDateInput(self, sel, acceptable):
        try:
            sel = str(sel)
        except ValueError:
            self.handleDateInputType(sel)

        while sel not in acceptable:
            print('That is not a valid input, please try again.')
            sel = input()

        return pd.to_datetime(sel)

    def handleDateInputType(self, sel):
        while not isinstance(sel, pd.datetime):
            print('That is not a valid input, please try again.')
            try:
                sel = pd.to_datetime(input())
            except ValueError:
                pass

        return pd.to_datetime(sel)


    def PriceToInt(self, Price):
        return np.float(Price.replace('$','').replace(',',''))