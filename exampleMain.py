from feda import Feda

datamanager = Feda(
    fileName='ohlcv_ftx_LINKUSD_30days.json',
    pair='LINK/USD',
    days=30,
    exchange='ftx'
)

data = datamanager.fetchDatafeed() # Fetch klines and output them into given file

# You can also just fetch the klines 
# data = datamanager.fetchDatafeed(writeToFile=False)

# Convert klines to 1h
import pandas as pd

ohlcv = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])

interval = '1h'

ohlcv = ohlcv.set_index('date')
ohlcv.index = pd.to_datetime(ohlcv.index, unit='ms')

ohlcv = ohlcv.groupby(pd.Grouper(freq=interval)).agg({'open': 'first', 'high': max, 'low': min, 'close': 'last', 'volume': sum})

print(ohlcv)