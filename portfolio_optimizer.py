import sys
import datetime
import pandas_datareader.data as web

# python ./portfolio_optimizer.py 2017 1 1 2017 6 30 AAPL GLD GOOG XOM
def main(startyear, startmonth, startday, endyear, endmonth, endday, symbol1, symbol2, symbol3, symbol4):
  ''' Main Function '''
  symbols = [symbol1, symbol2, symbol3, symbol4]
  start   = datetime.datetime(int(startyear), int(startmonth), int(startday))
  end     = datetime.datetime(int(endyear), int(endmonth), int(endday))
  print 'symbols', symbols
  print 'start', start
  print 'end', end

  symbol1DF = web.DataReader(symbol1, 'google', start, end)
  print symbol1
  print symbol1DF.ix['2017-06-16']









if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7],sys.argv[8],sys.argv[9],sys.argv[10])