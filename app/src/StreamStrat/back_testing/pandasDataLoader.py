import backtrader as bt

class PandasDEMA(bt.feeds.PandasData):
    lines = ('dema_short','dema_long','buy_signal','sell_signal')
    params = (
        ('datetime', None),
        ('open',1),
        ('high',2),
        ('low',3),
        ('close',4),
        ('volume',6),
        ('openinterest',None),
        ('adj_close',5),
        ('dema_short', 7),
        ('dema_long', 8),
        ('buy_signal', 9),
        ('sell_signal',10)
    )


class PandasOBV(bt.feeds.PandasData):
    lines = ('obv','obv_ema','buy_signal','sell_signal')
    params = (
        ('datetime', None),
        ('open',1),
        ('high',2),
        ('low',3),
        ('close',4),
        ('volume',6),
        ('openinterest',None),
        ('adj_close',5),
        ('obv', 7),
        ('obv_ema', 8),
        ('buy_signal', 9),
        ('sell_signal',10)
    )

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
