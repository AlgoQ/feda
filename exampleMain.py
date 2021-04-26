from feda import Feda

datamanager = Feda(fileName='data/ohlcv_bybit_LINKUSDT_170days.json', pair='LINK/USDT', days=170z, strExchange='bybit')

ohlcv = datamanager.fetchDatafeed() # Fetch klines and output them into given file