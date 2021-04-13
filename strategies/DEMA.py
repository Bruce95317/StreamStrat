import backtrader as bt
import math

class PandasDEMA(bt.feeds.PandasData):
    lines = ('close','dema_short','dema_long','buy_signal','sell_signal')
    params = (
        ('datetime', None),
        ('open',1),
        ('high',None),
        ('low',None),
        ('close',4),
        ('volume',None),
        ('openinterest',None),
        ('adj_close',None),
        ('dema_short', 7),
        ('dema_long', 8),
        ('buy_signal', 9),
        ('sell_signal',10)
    )

class TestDEMA(bt.Strategy):
    def __init__(self):
        self.sell_signal = self.datas[0].sell_signal
        self.buy_signal = self.datas[0].buy_signal

    def next(self):
        if not(math.isnan(self.buy_signal[0])):
            self.buy()
            print('buy at',self.buy_signal[0])
        elif not(math.isnan(self.sell_signal[0])):
            self.sell()
            print('sell at',self.sell_signal[0])


