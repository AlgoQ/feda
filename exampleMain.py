from histCryptoDatafeed import histCryptoDatafeed

# Create folder first
datamanager = histCryptoDatafeed(fileName='data/ohlcv_bybit_LINKUSDT_170days.json', pair='LINK/USDT', days=170, strExchange='bybit')

ohlcv_binanceF = datamanager.fetchDatafeed()