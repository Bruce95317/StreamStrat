import backtrader
#import datetime
#from strategies.strategy import TestStrategy
from strategies.SMA import TestSMA,PandasSMA
from strategies.OBV import TestOBV,PandasOBV
from strategies.DEMA import TestDEMA,PandasDEMA
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Tradimo

def backtrader_runner(df,strategy_name):
    cerebro = backtrader.Cerebro()
    cerebro.addobserver(backtrader.observers.Broker)
    cerebro.addsizer(backtrader.sizers.FixedSize, stake=1000)

    cerebro.broker.set_cash(1000000)
    #data = backtrader.feeds.YahooFinanceCSVData(
    #    dataname='data/GOOG.csv',plot=False)
        # Do not pass values before this date
        #fromdate=datetime.datetime(2001, 10, 1),
        # Do not pass values after this date
        #todate=datetime.datetime(2001, 12, 1),
        #reverse=False)
    if strategy_name == 'SMA':
        data = PandasSMA(dataname = df,plot = False)
        cerebro.addstrategy(TestSMA)
    elif strategy_name == 'OBV':
        data = PandasOBV(dataname = df,plot = False)
        cerebro.addstrategy(TestOBV)
    elif strategy_name == 'DEMA':
        data = PandasDEMA(dataname = df,plot = False)
        cerebro.addstrategy(TestDEMA)

    cerebro.adddata(data)

    #print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run(stdstats = False)
    #print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    b = Bokeh(scheme=Tradimo(show_headline = False),output_mode='save',filename = 'broker_fig.html')
    cerebro.plot(b,volume = False)