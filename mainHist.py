from histCryptoDatafeed import histCryptoDatafeed

# Create folder first
datamanager = histCryptoDatafeed(fileName='data_binanceF3/ohlcv_binance_LINKUSDT_75days.json', pair='LINK/USDT', days=75, strExchange='binanceFutures', interval='15m')

ohlcv_binanceF = datamanager.fetchDatafeed()
