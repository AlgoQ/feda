# Built-in modules
from datetime import datetime
import calendar
# Extern modules
import ccxt
class histCryptoDatafeed:
    def __init__(self, fileName:str, pair:str, days:int, strExchange:str='binanceFutures', interval:str='1m'):
        self.fileName = fileName
        self.pair = pair
        self.days = days
        self.strExchange = strExchange
        self.interval = interval
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
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'future',
                }
            })

            self.limit = 5000
        else:
            raise Exception('Exchange is not supported')

    def _calcMillis(self):
        minute = 60000

        if self.interval == '1m':
            return minute * self.limit
        elif self.interval == '3m':
            return minute * 3 * self.limit
        elif self.interval == '5m':
            return minute * 5 * self.limit
        elif self.interval == '15m':
            return minute * 15 * self.limit
        elif self.interval == '30m':
            return minute * 30 * self.limit
        elif self.interval == '45m':
            return minute * 45 * self.limit
        elif self.interval == '1h':
            return minute * 60 * self.limit
        elif self.interval == '2h':
            return minute * 60 * 2 * self.limit
        elif self.interval == '4h':
            return minute * 60 * 4 * self.limit
        elif self.interval == '1d':
            return minute * 60 * 24 * self.limit
        elif self.interval == '1w':
            return minute * 60 * 24 * 7 * self.limit
        elif self.interval == '1M':
            return minute * 60 * 24 * 30 * self.limit
        else:
            raise Exception('Unsupported interval')


    def fetchDatafeed(self):
        startSince = self.exchange.milliseconds() - 86400000 * self.days
        until = round(datetime.now().timestamp() * 1000)
        diffBtwnUntilSince = round(int(until - startSince)/(1000*60))
        loopCount = int(diffBtwnUntilSince / self.limit)

        fullOhlcv = []
        
        fullOhlcv = self.exchange.fetch_ohlcv(symbol=self.pair, limit=self.limit, timeframe=self.interval, since=startSince)
        millisCycle = self._calcMillis()
        
        since = startSince + millisCycle
        for i in range(loopCount - 1):
            fullOhlcv = fullOhlcv + self.exchange.fetch_ohlcv(symbol=self.pair, limit=self.limit, timeframe=self.interval, since=since)
            since += millisCycle

        # # TODO: If item is already in the list don't add it

        f = open(self.fileName, "w")

        f.write(str(fullOhlcv))
        f.close()

        return fullOhlcv