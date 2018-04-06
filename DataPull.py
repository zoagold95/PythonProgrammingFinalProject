import quandl
quandl.ApiConfig.api_key = 'yTfiVMeRssPF4sBnwDP7'
import pandas as pd
import os
from quandl.errors.quandl_error import *
from time import sleep


class dataPull:
    def __init__(self):

        #downloading from quandl
        self.markets = ['KRAKEN','COINBASE','BITSTAMP','ITBIT']
        self.marketData = {}
        self.proj_loc = os.getcwd()


    def quandlPull(self):
        try:
            for i in self.markets:
                self.marketData[i] = quandl.get('BCHARTS/{}USD'.format(i), returns = 'pandas')
                self.marketData[i].to_csv(self.proj_loc +'/' + i + '.csv',sep = ',')
        except quandl.errors.quandl_error.LimitExceededError as e:
            print('Exceeded daily pulls from quandl database. Reading from locally saved .csv. All data may not be up to date.')

        for i in self.markets:
            self.marketData[i] = self.readFromCsv(i)
                #self.marketData[i] = pd.read_csv(self.proj_loc +'/' + i + '.csv', sep = ',', usecols = cols)

    def readFromCsv(self, market):
        cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume (BTC)', 'Volume (Currency)', 'Weighted Price']
        return pd.read_csv(self.proj_loc +'/' + market + '.csv', sep = ',', usecols = cols)
        #self.marketData[i] = pd.read_csv(self.proj_loc +'/' + i + '.csv', sep = ',', usecols = cols)

    def sameLength(self):
        """
        This section makes data base the same length. BITSTAMP goes back the
        furthest and has an entry for every date from it's start until now. So if another market
        is missing a value from a given date, this code inserts a new row of zeros for that date.
        This will make it so that there are nothing but zeros until the source started recording,
        and will still allow the next section of code to change zeros to the day-previous value
        for averaging purposes.
        """

        marketsminusbit = ['KRAKEN','COINBASE','ITBIT']
        all_col_lens = self.marketData['BITSTAMP'].count()
        col_len = all_col_lens['Open']
        data = self.marketData
        blank = pd.DataFrame(columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume (BTC)', 'Volume (Currency)', 'Weighted Price'])
        blank['Date'] = data['BITSTAMP']['Date']
        for market in marketsminusbit:
            broke_counter = 0
            for row in range(col_len):
                if blank['Date'][row] == data[market]['Date'][broke_counter]:
                    blank['Open'][row] = data[market]['Open'][broke_counter]
                    blank['High'][row] = data[market]['High'][broke_counter]
                    blank['Low'][row] = data[market]['Low'][broke_counter]
                    blank['Close'][row] = data[market]['Close'][broke_counter]
                    blank['Volume (BTC)'][row] = data[market]['Volume (BTC)'][broke_counter]
                    blank['Volume (Currency)'][row] = data[market]['Volume (Currency)'][broke_counter]
                    blank['Weighted Price'][row] = data[market]['Weighted Price'][broke_counter]
                    broke_counter += 1
            data[market] = blank



    def replaceZeros(self):
        """
        If there is a zero in the data anywhere that means the service was down for that day.
        This section takes the value for the day before and puts it in for that day for averaging
        purposes.
        """

        data = self.marketData
        keys = list(data['BITSTAMP'].keys())
        all_col_lens = data['BITSTAMP'].count()
        col_len = all_col_lens['Open']
        for market in data:
            lastVal = None
            for item in keys:
                for p in range(col_len):
                    x = data[market].at[data[market].index[p], item]
                    if x == 0:
                        data[market].at[p, item] = lastVal
                    else:
                        lastVal = x
