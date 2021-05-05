import backtrader as bt
import math

class PandasSMA(bt.feeds.PandasData):
    lines = ('sma30','sma100','buy_signal','sell_signal')
    params = (
        ('datetime', None),
        ('open',1),
        ('high',2),
        ('low',3),
        ('close',4),
        ('volume',6),
        ('openinterest',None),
        ('adj_close',5),
        ('sma30', 7),
        ('sma100', 8),
        ('buy_signal', 9),
        ('sell_signal',10)
    )

class TestSMA(bt.Strategy):
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



