from histCryptoDatafeed import histCryptoDatafeed

# Create folder first
datamanager = histCryptoDatafeed(fileName='data/ohlcv_bybit_LINKUSDT_126days.json', pair='LINK/USDT', days=126, strExchange='bybit', interval='1m')

ohlcv_binanceF = datamanager.fetchDatafeed()