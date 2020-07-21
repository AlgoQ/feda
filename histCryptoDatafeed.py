# Built-in modules
from datetime import datetime
import calendar
# Extern modules
import ccxt

def _calcMillis(interval, limit):
    if interval == '1m':
        return 60000 * limit
    elif interval == '3m':
        return 60000 * 3 * limit


def histCryptoDatafeed(pair:str, days:int, exchange='binanceFutures', interval='1m'):
    # Check exchange
    if exchange == 'binanceFutures':
        exchange = ccxt.binance({
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future',
            }
        })

        limit = 1000
    
    elif exchange == 'binance':
        exchange = ccxt.binance({
            'enableRateLimit': True
        })

        limit = 1000
    else:
        raise Exception('Exchange is not supported')
    
    startSince = exchange.milliseconds() - 86400000 * days
    until = datetime.now().strftime("%d/%m/%Y %H:%M:%S").timestamp() * 1000

    diffBtwnUntilSince = int((until - startSince).total_seconds() / 60)
    loopCount = diffBtwnUntilSince / limit

    fullOhlcv = []

    fullOhlcv.append(exchange.fetch_ohlcv(symbol=pair, limit=limit, timeframe=interval, since=startSince))
    millisCycle = _calcMillis(interval, limit)

    since = startSince + millisCycle
    for i in range(loopCount - 1):
        fullOhlcv.append(exchange.fetch_ohlcv(symbol=pair, limit=limit, timeframe=interval, since=since))
        since += millisCycle

    # TODO: If item is already in the list don't add it
    

histCryptoDatafeed(pair='BTC/USDT', days=60, exchange='binanceFutures', interval='1m')