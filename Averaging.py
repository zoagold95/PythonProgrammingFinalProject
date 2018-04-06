import pandas as pd



class Averaging():
    def __init__(self, dP):
        self.markets = ['KRAKEN','COINBASE','BITSTAMP','ITBIT']
        self.dP = dP
        self.Weighted = pd.DataFrame()
        self.dummyDfHeads = []
        self.dummyMarket = None



    def Avg(self):
        """
        Setting up 'dummy Data Frame' which is one large dataframe of each market dataframe merged together. self.Weighted dataframe
        will be the large averaged dataframe that gets handled for plotting and Amazon comparison.
        """

        #self.dummyDfHeads = []
        data = self.dP.marketData
        dataminusbit = ['KRAKEN','COINBASE','ITBIT']
        colHeads = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume (BTC)', 'Volume (Currency)', 'Weighted Price']
        colHeadsminDate = ['Open', 'High', 'Low', 'Close', 'Volume (BTC)', 'Volume (Currency)', 'Weighted Price']
        self.Weighted = pd.DataFrame(columns = colHeads)
        self.Weighted['Date'] = data['BITSTAMP']['Date']

        """
        Merging all dataframes
        """
        self.dummyDf = data['BITSTAMP']
        for market in dataminusbit:
            self.dummyDf = pd.merge(self.dummyDf,data[market], how = 'left', on = 'Date')

        """
        Setting uniform column header names for large dataframe
        """
        self.dummyDfHeads = colHeads
        for item in range(len(data)-1):
            self.dummyDfHeads = self.dummyDfHeads + colHeadsminDate
        self.dummyDf.columns = self.dummyDfHeads


        """
        Calculating the average of each column per day, and putting it in the Weighted DataFrame
        """
        #start = time.time()
        print('Processing...')
        for item in colHeadsminDate:
            self.DropCol(item)
            self.Weighted[item] = self.dummyMarket.mean(axis = 1)

        """"
        Making the Date column the index
        """
        self.Weighted.set_index('Date', inplace = True)


    def DropCol(self,col):
        self.dummyMarket = self.dummyDf
        seriesName = self.dummyDfHeads
        for i in range(4):
            seriesName.remove(col)

        """
        :param seriesName:  Type: String / List of strings      Name of series to drop
        :param market:      Type: String                        Name of market to clean
        """

        for item in seriesName:
            self.dummyMarket = self.dummyMarket.drop(item, axis=1)
