# Built-in modules
from datetime import datetime 
import math
# Extern modules
import ccxt
class histCryptoDatafeed:
    def __init__(self, fileName:str, pair:str, days:int, strExchange:str='binanceFutures'):
        self.fileName = fileName
        self.pair = pair
        self.days = days
        self.strExchange = strExchange
        self._checkExchange()

    def _checkExchange(self):
        if self.strExchange == 'binance':
            self.exchange = ccxt.binance({
                'enableRateLimit': True
            })

            self.limit = 1000
        elif self.strExchange == 'binanceFutures':
            self.exchange = ccxt.binance({
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'future',
                }
            })

            self.limit = 1000

        elif self.strExchange == 'bybit':
            self.exchange = ccxt.bybit({
                'enableRateLimit': True
            })

            self.limit = 200
        elif self.strExchange == 'okexFutures':
            self.exchange = ccxt.okex({
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'future',
                }
            })

            self.limit = 300
        elif self.strExchange == 'bitstamp':
            self.exchange = ccxt.bitstamp({
                'enableRateLimit': True
            })

            self.limit = 1000
        elif self.strExchange == 'ftx':
            self.exchange = ccxt.ftx({
                'enableRateLimit': True
            })

            self.limit = 5000
        else:
            raise Exception('Exchange is not supported')

    def fetchDatafeed(self):
        until = self.exchange.milliseconds()
        startSince = until - 86400000 * self.days

        diffBtwnUntilSince = round(int(until - startSince)/(1000*60))
        loopCount = math.floor(diffBtwnUntilSince / self.limit)

        fullOhlcv = self.exchange.fetch_ohlcv(symbol=self.pair, limit=self.limit, timeframe='1m', since=startSince)
        since = fullOhlcv[-1][0] + 60000

        fullOhlcvFull = [fullOhlcv]

        for i in range(loopCount):
            fullOhlcv = self.exchange.fetch_ohlcv(symbol=self.pair, limit=self.limit, timeframe='1m', since=since)
            fullOhlcvFull = fullOhlcvFull + fullOhlcv
            since = fullOhlcv[-1][0] + 60000

        f = open(self.fileName, "w")

        f.write(str(fullOhlcvFull))
        f.close()

        return fullOhlcv