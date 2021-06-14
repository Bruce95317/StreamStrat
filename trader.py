import backtrader
#import datetime
#from strategies.strategy import TestStrategy
from strategies.SMA import TestSMA,PandasSMA
from strategies.OBV import TestOBV,PandasOBV
from strategies.DEMA import TestDEMA,PandasDEMA
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Tradimo

"""
def processPlots(cerebro, numfigs=1, iplot=True, start=None, end=None,
         width=16, height=9, dpi=300, use=None, **kwargs):

    # if self._exactbars > 0:
    #     return
    from backtrader import plot
    import matplotlib
    matplotlib.use('agg')

    if cerebro.p.oldsync:
        plotter = plot.Plot_OldSync(**kwargs)
    else:
        plotter = plot.Plot(**kwargs)

    plotter = plot.Plot(**kwargs)

    figs = []
    for stratlist in cerebro.runstrats:
        for si, strat in enumerate(stratlist):
            rfig = plotter.plot(strat, figid=si * 100,
                                numfigs=numfigs, iplot=iplot,
                                start=start, end=end, use=use,)
            figs.append(rfig)

        # this blocks code execution
        # plotter.show()

    for fig in figs:
        for f in fig:
            f.set_size_inches(width, height)
            f.set_dpi(dpi)
            f.savefig('broker_fig.png', bbox_inches='tight')
    return figs
"""

def backtrader_runner(df,strategy_name):
    cerebro = backtrader.Cerebro()
    ## too much stake?
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
    cerebro.run()
    #print('Final Portfolio Value: %.2  f' % cerebro.broker.getvalue())
    #processPlots(cerebro,width=12, height=6, dpi=300,fmt_x_ticks = '%x',)

    b = Bokeh(plot_mode='single', output_mode='memory',scheme=Tradimo(show_headline = False,plotaspectratio = 2.0))
    model = cerebro.plot(b)
    return model[0]


