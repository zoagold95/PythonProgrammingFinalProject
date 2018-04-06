from DataPull import dataPull
from Averaging import Averaging
from Plotting import plotting
from AmazonPull import AmazonPull
from WhatIf import WhatIf
import time


class cryptoCurrencyTracker:
    def __init__(self):
        #pulling Bitcoin data
        print('Pulling Bitcoin data... ')
        dP = dataPull()
        dataPull.quandlPull(dP)
        dataPull.sameLength(dP)
        dataPull.replaceZeros(dP)

        print('Compiling... ')
        Av = Averaging(dP)
        Averaging.Avg(Av)
        print('Complete!')

        #pulling amazon Data
        print('Pulling info from Amazon. This may take a minute depending on your internet connection...')
        Az = AmazonPull()
        AmazonPull.ReadAsin(Az)
        print('Complete!')


        Pl = plotting(Av)
        #begin selection of plot or 'What if'

        menuSelAccept = ['A', 'B', 'C', 'a', 'b', 'c']

        while True:
            print('\n', 'What would you like to do?')
            print('A.) Plot Bitcoin Data')
            print('B.) Run a \'what-if\' scenario')
            print('C.) Exit')
            menuSel = input()
            PlotAccept = ['Open', 'High', 'Low', 'Close', 'Volume (BTC)', 'Volume (Currency)', 'Weighted Price']
            if menuSel not in menuSelAccept:
                menuSel = self.handleInput(menuSel,menuSelAccept)

            #Plotting Selection
            if menuSel == 'a' or menuSel == 'A':
                print('Select which value you would like to plot: \n', 'Open, High, Low, Close, Volume (BTC), Volume (Currency), Weighted Price')
                PlotSel = input()
                if PlotSel not in PlotAccept:
                    PlotSel = self.handleInput(PlotSel, PlotAccept)
                Pl.plotter(PlotSel)
            elif menuSel == 'B' or menuSel == 'b':
                Wi = WhatIf(dP, Av, Az, cryptoCurrencyTracker)
                WhatIf.readAmazonData(Wi)
                WhatIf.whatIf(Wi)
                WhatIf.valueComparison(Wi)

            elif menuSel == 'C' or menuSel == 'c':
                exit()



        #handling input
    def handleInput(self, sel, acceptable):
        while sel not in acceptable:
            print('That is not a valid input, please try again.\n')
            sel = input()
        return sel








if __name__ == '__main__':
    cryptoCurrencyTracker()