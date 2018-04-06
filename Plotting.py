import matplotlib.pyplot as plt
import pandas as pd

class plotting():

    def __init__(self, Av):
        self.Av = Av

    def plotter(self,sel):
        Weighted = self.Av.Weighted
        x = pd.to_datetime(Weighted.index)
        y = Weighted[sel]
        plt.grid(True)
        plt.title('Bitcoin Value(USD) by Date')
        plt.xlabel('Date')
        plt.ylabel('USD')
        plt.plot(x,y,'.-', label = sel)
        plt.draw()
        plt.show(block = False)
        plt.pause(.5)
        plt.legend()
