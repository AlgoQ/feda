# Built-in modules
from datetime import datetime
import calendar
# Extern modules
import ccxt
class histCryptoDatafeed:
    def __init__(self, pair:str, days:int, strExchange:str='binanceFutures', interval:str='1m'):
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
        else:
            raise Exception('Exchange is not supported')

    def _calcMillis(self, interval, limit):
        minute = 60000
        if interval == '1m':
            return minute * limit
        elif interval == '3m':
            return minute * 3 * limit
        elif interval == '5m':
            return minute * 5 * limit
        elif interval == '15m':
            return minute * 15 * limit
        elif interval == '30m':
            return minute * 30 * limit
        elif interval == '45m':
            return minute * 45 * limit
        elif interval == '1h':
            return minute * 60 * limit
        elif interval == '2h':
            return minute * 60 * 2 * limit
        elif interval == '4h':
            return minute * 60 * 4 * limit
        elif interval == '1d':
            return minute * 60 * 24 * limit
        elif interval == '1w':
            return minute * 60 * 24 * 7 * limit
        elif interval == '1w':
            return minute * 60 * 24 * 30 * limit
        else:
            raise Exception('Unsupported interval')


    def histCryptoDatafeed(self, pair:str, days:int, exchange='binanceFutures', interval='1m'):
        startSince = exchange.milliseconds() - 86400000 * days
        until = datetime.now().strftime("%d/%m/%Y %H:%M:%S").timestamp() * 1000

        diffBtwnUntilSince = int((until - startSince).total_seconds() / 60)
        loopCount = diffBtwnUntilSince / self.limit

        fullOhlcv = []

        fullOhlcv.append(exchange.fetch_ohlcv(symbol=pair, limit=self.limit, timeframe=interval, since=startSince))
        millisCycle = self._calcMillis(interval, self.limit)

        since = startSince + millisCycle
        for i in range(loopCount - 1):
            fullOhlcv.append(exchange.fetch_ohlcv(symbol=pair, limit=self.limit, timeframe=interval, since=since))
            since += millisCycle

        # TODO: If item is already in the list don't add it
        # TODO: Check release of a specific market pair
        

    # histCryptoDatafeed(pair='BTC/USDT', days=60, exchange='binanceFutures', interval='1m')