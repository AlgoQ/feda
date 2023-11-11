# Built-in modules
from datetime import datetime 
from time import time
from asyncio import sleep
# Extern modules
import pandas as pd
import ccxt.pro

class Feda:
    def __init__(self, symbols:str|list=None, timeframe:str='1d', startTime:str=None, limit:int=None, marketType:str='spot', quote:str=None, settle:str='USDT', callType:str='ohlcv', exchangeId:str='binance'):
        self.symbols = symbols
        self.timeframe = timeframe
        self.startTime = startTime
        self.limit = limit
        self.marketType = marketType # options: spot, future, swap, option
        if quote != None:
            self.quote = quote.upper() # example: USDT
        else:
            self.quote = quote
        if settle != None:
            self.settle = settle.upper() # options: USDT, USDC, COIN
        else:
            self.settle = settle
        self.callType = callType # options: ohlcv - more coming soon
        self.exchangeId = exchangeId # options: all supported exchanges on ccxt (https://github.com/ccxt/ccxt/wiki/Exchange-Markets#supported-exchanges)
        self.exchange = self._createExchange()

        if self.startTime == None and self.limit == None:
            raise Exception('Either `startTime` or `limit` should be defined')
        
    async def main(self):
        self.markets = await self.exchange.loadMarkets()
        self.symbols = self._checkOrFetchSymbols(self.symbols)
        result = await self._handleCallType()
        await self.exchange.close()
        return result
    
    async def fetchOHLCV(self):
        if 'fetch_ohlcv' not in dir(self.exchange):
            raise ccxt.NotSupported(f'{self.exchange} does not has the `fetchOHLCV` endpoint')
        
        if self.startTime is not None:
            startSince = self.startTime
        elif self.limit is not None:
            currentMs = int(time() * 1000)
            startSince = currentMs - self._timeframeToMs(self.timeframe) * self.limit

        result = {}
        try:
            for symbol in self.symbols:
                since = startSince
                result[symbol] = []
                try:
                    while True:
                        data = await self.exchange.fetch_ohlcv(symbol, self.timeframe, since)
                        if data[-1][0] == since:
                            result[symbol].extend([data[-1]])
                            df = pd.DataFrame(result[symbol], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                            result[symbol] = df
                            break
                        
                        result[symbol].extend(data[:-1])
                        since = data[-1][0]

                    self._printLog(f'{symbol} data has been fetched')
                except (IndexError, KeyError):
                    if result[symbol] != []:
                        df = pd.DataFrame(result[symbol], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                        result[symbol] = df
                        self._printLog(f'{symbol} data has been fetched')
                    else:
                        self._printLog(f'Failed to fetch {symbol} data')
                        del result[symbol]
                    continue
        
        except ccxt.NetworkError:
            await sleep(5)

        return result
    
    async def _handleCallType(self):
        if self.callType == 'ohlcv':
            result = await self.fetchOHLCV()
        return result
    
    def _createExchange(self):
        exchange = getattr(ccxt.pro, self.exchangeId)()
        return exchange

    def _printLog(self, msg:str):
        print(f'{datetime.now()} - {msg}')

    def _timeframeToMs(self, timeframe):
        timeframes = {
            's': 1000,
            'm': 60000,
            'h': 3600000,
            'd': 86400000,
            'w': 604800000,
            'M': 2592000000,
        }

        unit = timeframe[-1]
        if unit in timeframes:
            try:
                multiplier = int(timeframe[:-1])
            except ValueError:
                return None  # Invalid format
            return multiplier * timeframes[unit]
        else:
            return None  # Unsupported unit

    def _checkOrFetchSymbols(self, symbols:list|str):
        if symbols == None:
            result = []
            # Check marketType and settle
            for symbol, market in self.markets.items():
                if self.marketType == 'swap' and market['type'] == 'swap':
                    if self.settle == None:
                        raise ccxt.ArgumentsRequired('When `marketType` is swap, settle can not be undefined')
                    if self.settle == 'COIN':
                        if market['settle'] == market['base']:
                            result.append(symbol)
                    else:
                        if market['settle'] == self.settle:
                            result.append(symbol)
                else:
                    if market['type'] == self.marketType:
                        result.append(symbol)

            # Check quote
            if self.quote != None:
                for symbol in result.copy():
                    market = self.markets[symbol]
                    if market['quote'] != self.quote:
                        result.remove(symbol)
            
            return result
        else:
            if isinstance(symbols, list):
                for symbol in symbols:
                    if symbol not in self.markets:
                        raise ccxt.BadSymbol(f'{symbol} is not available on {self.exchangeId}, also make sure you are using the right symbol naming convention -> https://docs.ccxt.com/#/?id=contract-naming-conventions')

        if isinstance(symbols, list):
            return symbols
        else:
            return [symbols]