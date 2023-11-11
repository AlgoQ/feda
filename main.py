from asyncio import run
from feda import Feda


## EXAMPLES
# 1. Fetch last 5000 hourly candles for BTC/USDT:USDT (USDT settled perpetuals) & ETH/USDT:USDT on Bybit & print these OHLCV dataframes
feda = Feda(symbols=['BTC/USDT:USDT', 'ETH/USDT:USDT'], timeframe='1h', limit=5000, exchangeId='bybit')
data = run(feda.main())

for symbol, ohlcv in data.items():
    print(symbol)
    print(ohlcv)


# 2. Fetch daily candles for all USDT spot symbols on Binance since 1 Jan 2023 (1672527600000 - https://currentmillis.com/) & export them to csv's
from pathlib import Path 
feda = Feda(timeframe='1d', startTime=1672527600000, marketType='spot', quote='USDT', exchangeId='binance')
data = run(feda.main())

currentDirectory = str(Path.cwd())
for symbol, ohlcv in data.items():
    symbolWithoutSlashes = symbol.replace('/', '').replace(':', '')
    fileName = fr'\{symbolWithoutSlashes}_{feda.timeframe}_{ohlcv["timestamp"].min() // 1000}_{ohlcv["timestamp"].max() // 1000}.csv'
    path = currentDirectory + fileName
    ohlcv.to_csv(path, index=False)

print(f'All OHLCV data has been saved')