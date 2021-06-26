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

class TradeStat(backtrader.analyzers.TradeAnalyzer):
    '''
    statistics for trade:
    col:
    for all trade:
        index1:
            total - total # of trade
            closed - total # of closed trade
        index2:
            total - total profit/loss of all trade
            return - return rate for investment

    col:
    for won trade:
        index1:
            closed - total # of closed trade
            percent - % of won close trade from all closed trade
        index2:
            total  - total profit from won trade
            max - max profit from won trade

    for lost trade:
        index1:
            closed - total # of closed trade
            percent - % of lost close trade from all closed trade
        index2:
            total  - total profit from lost trade
            max - max profit from lost trade
    '''


    def __init__(self):
        self.start_val = self.strategy.broker.getvalue()
        self.end_val = None
    def stop(self):
        self.end_val = self.strategy.broker.getvalue()
    def get_analysis(self):
        dict1 = super(TradeStat, self).get_analysis()
        ## handling case for no trade happen(no closed trade/no enough cash)
        if len(dict1.keys())==1:
            return 0
        result1 = []
        result2 = []
        total_close = 0
        for key,val in dict1.items():
            if key == 'total':
                temp1 = {'col':'ALL TRADES','id1':'TRADE','id2':'total','val':val['total']}
                temp2 = {'col':'ALL TRADES','id1':'TRADE','id2':'closed','val':val['closed']}
                total_close = val['closed']

            elif key == 'pnl':
                total_profit = val['gross']['total']
                ret_rate = total_profit / self.start_val
                temp1 = {'col': 'ALL TRADES', 'id1':'PROFIT','id2': 'total', 'val': "{:.4f}".format(total_profit)}
                temp2 = {'col': 'ALL TRADES', 'id1':'PROFIT','id2': 'return rate', 'val': "{:.4%}".format(ret_rate)}

            elif key == 'won':
                temp1 = {'col': 'TRADES WON', 'id1':'TRADE','id2': 'total', 'val': val['total']}
                temp2 = {'col': 'TRADES WON', 'id1':'TRADE','id2': '%', 'val': val['total']/total_close }
                temp3 = {'col': 'TRADES WON', 'id1':'PROFIT','id2': 'total', 'val': val['pnl']['total']}
                temp4 = {'col': 'TRADES WON', 'id1':'PROFIT','id2': 'max', 'val': val['pnl']['max']}

            elif key == 'lost':
                temp1 = {'col': 'TRADES LOST', 'id1':'TRADE','id2': 'total', 'val': val['total']}
                temp2 = {'col': 'TRADES LOST', 'id1':'TRADE','id2': '%', 'val': val['total']/total_close }
                temp3 = {'col': 'TRADES LOST', 'id1':'PROFIT','id2': 'total', 'val': val['pnl']['total']}
                temp4 = {'col': 'TRADES LOST', 'id1':'PROFIT','id2': 'max', 'val': val['pnl']['max']}
            else:
                continue

            if key in ['total','pnl']:
                for _dict in [temp1,temp2]:
                    result1.append(_dict)
            if key in ['won','lost']:
                for _dict in [temp1,temp2,temp3,temp4]:
                    result2.append(_dict)

        return {'result1':result1,'result2':result2}




def backtrader_runner(df,strategy_name,stake,cash):
    cerebro = backtrader.Cerebro()
    ## too much stake?
    cerebro.addsizer(backtrader.sizers.FixedSize, stake=stake)

    cerebro.broker.set_cash(cash)
    # Analyzer
    cerebro.addanalyzer(TradeStat, _name='trade_stat')
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
    thestrats = cerebro.run()
    ## for getting the analyzer obj
    thestrat = thestrats[0]

    #print('Final Portfolio Value: %.2  f' % cerebro.broker.getvalue())
    #processPlots(cerebro,width=12, height=6, dpi=300,fmt_x_ticks = '%x',)

    b = Bokeh(plot_mode='single', output_mode='memory',scheme=Tradimo(show_headline = False,plotaspectratio = 2.0))
    model = cerebro.plot(b)
    return model[0],thestrat.analyzers.trade_stat.get_analysis()


