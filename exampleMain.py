from feda import Feda

# Create folder first
datamanager = Feda(fileName='data/ohlcv_bybit_LINKUSDT_30days.json', pair='LINK/USDT', days=30, strExchange='bybit')

ohlcv = datamanager.fetchDatafeed()