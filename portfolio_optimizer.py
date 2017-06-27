import sys
import datetime
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import numpy as np

def dailyReturns(nds):
  ''' 
  It is very often useful to look at the returns by day for individual stocks. 
  The general equation for daily return on day t is:
  
    ret(t) = (price(t)/price(t-1)) -1 
  
  '''
  s= np.shape(nds)
  if len(s)==1:
      nds=np.expand_dims(nds,1)
  nds[1:, :] = (nds[1:, :] - nds[0:-1]) / abs(nds[0:-1]) # ./portfolio_optimizer.py:19: RuntimeWarning: invalid value encountered in divide
  nds[0, :] = np.zeros(nds.shape[1])

def simulate(na_rets, lf_alloc):
    ''' Simulate Function'''

    # Estimate portfolio returns
    na_portrets = np.sum(na_rets * lf_alloc, axis=1)
    cum_ret = na_portrets[-1]
    # TODO Replace returnize0 with dailyReturns
    # tsu.returnize0(na_portrets)
    dailyReturns(na_portrets)

    # Statistics to calculate
    stddev = np.std(na_portrets)
    daily_ret = np.mean(na_portrets)
    sharpe = (np.sqrt(252) * daily_ret) / stddev

    # Return all the variables
    return stddev, daily_ret, sharpe, cum_ret
  

# python ./portfolio_optimizer.py 2017 1 1 2017 6 30 AAPL GLD GOOG XOM
def main(startyear, startmonth, startday, endyear, endmonth, endday, symbol1, symbol2, symbol3, symbol4):
  ''' Main Function '''
  symbols = [symbol1, symbol2, symbol3, symbol4]
  start   = datetime.datetime(int(startyear), int(startmonth), int(startday))
  end     = datetime.datetime(int(endyear), int(endmonth), int(endday))
  print 'symbols', symbols
  print 'start', start
  print 'end', end

  ls_symbols = [symbol1,symbol2, symbol3, symbol4]
  # pandas.core.panel.Pane
  symbolPandasPane = web.DataReader(ls_symbols, 'google', start, end)
  # testDFConversion(symbolPandasPane)
  
  # Copying close price into separate dataframe to find rets
  df_rets = symbolPandasPane
  # Filling the data.
  df_rets = df_rets.fillna(method='ffill')
  df_rets = df_rets.fillna(method='bfill')
  
  # Normalized Data
  # Numpy matrix of filled data values
  na_rets = df_rets.values
  na_rets = na_rets / na_rets[0, :]
  print "Values:"
  print na_rets[1, :]
  
  
  lf_alloc = [0.0, 0.0, 0.0, 0.0]
  max_sharpe = -1000
  final_stddev = -1000
  final_daily_ret = -1000
  final_cum_ret = -1000
  best_portfolio = lf_alloc
  
  for i in range(0, 101, 10):
      left_after_i = 101 - i
      for j in range(0, left_after_i, 10):
          left_after_j = 101 - i - j
          for k in range(0, left_after_j, 10):
              left_after_k = 100 - i - j - k
              lf_alloc = [i, j, k, left_after_k]
              lf_alloc = [x * 0.01 for x in lf_alloc]
              stddev, daily_ret, sharpe, cum_ret = simulate(na_rets, lf_alloc)
              if sharpe > max_sharpe:
                  max_sharpe = sharpe
                  final_stddev = stddev
                  final_cum_ret = cum_ret
                  final_daily_ret = daily_ret
                  best_portfolio = lf_alloc

  print "Symbols : ", ls_symbols
  print "Best Portfolio : ", best_portfolio
  print "Statistics : Std. Deviation : ", final_stddev
  print "Statistics : Daily Returns  : ", final_daily_ret
  print "Statistics : Cum. Returns   : ", final_cum_ret
  print "Statistics : Sharpe Ratio   : ", max_sharpe
  
  
  
  # symbol2DF = web.DataReader(symbol2, 'google', start, end)
  # symbol3DF = web.DataReader(symbol3, 'google', start, end)
  # symbol4DF = web.DataReader(symbol4, 'google', start, end)
  # Date    Open    High     Low   Close     Volume
  # print symbolPandasPane
  # print symbolPandasPane
  # print symbol1DF #.ix['2017-06-16']

  plt.clf()
  plt.plot(symbolPandasPane.Close, label=symbol1)
  # plt.plot(symbol2DF.Close, label=symbol2)
  # plt.plot(symbol3DF.Close, label=symbol3)
  # plt.plot(symbol4DF.Close, label=symbol4)
  plt.legend()
  plt.ylabel('Cost')
  plt.xlabel('Date')
  plt.savefig('debug.pdf', format='pdf')


  # print type(symbolPandasPane)




if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7],sys.argv[8],sys.argv[9],sys.argv[10])