# FEDA
A user-friendly library to fetch kline/ohlcv data from several crypto exchanges, using CCXT & pandas.

## Install
```shell
$ git clone https://github.com/AlgoQ/feda
$ pip install -r requirements.txt
```

## Some examples
1. Fetch last 5000 daily candles for BTC/USDT:USDT (USDT settled perpetuals) & ETH/USDT:USDT on Binance & print these OHLCV dataframes
```python
from asyncio import run
from feda import Feda

feda = Feda(symbols=['BTC/USDT:USDT', 'ETH/USDT:USDT'], timeframe='1d', limit=5000, exchangeId='binance')
data = run(feda.main())

for symbol, ohlcv in data.items():
    print(symbol)
    print(ohlcv)
```

2. Fetch all weekly candle for all spot symbols on Bybit since 1 Jan 2023 (1672527600000 - https://currentmillis.com/) & export them to csv's
```python
feda = Feda(timeframe='1h', startTime=1672527600000, marketType='spot', exchangeId='bybit')
data = run(feda.main())

for symbol, ohlcv in data.items():
    path = f'{symbol}_{feda.timeframe}_{ohlcv["timeframe"].min() // 1000}_{ohlcv["timeframe"].max() // 1000}.csv'
    ohlcv.to_csv(path, index=False)
    print(f'{symbol} OHLCV csv data saved at `{path}`')
```


## Supported Exchanges
All exchanges that support `fetchOHLCV` on ccxt (most of them), [supported CCXT exchanges](https://github.com/ccxt/ccxt/wiki/Exchange-Markets)

## Feda Parameters
| Parameter     | Type             | Default Value | Description                                                                                               |
|---------------|------------------|---------------|-----------------------------------------------------------------------------------------------------------|
| symbols       | str or list      | None          | The trading pair symbol(s) or list of symbols.                                                            |
| timeframe     | str              | '1d'          | The timeframe for the OHLCV data.                                                                         |
| startTime     | str              | None          | The start time in milliseconds for fetching historical data.                                              |
| limit         | int              | None          | The maximum number of data points to retrieve.                                                            |
| marketType    | str              | 'spot'        | The market type. Options: spot, future, swap, option.                                                     |
| quote         | str              | None          | The quote currency for the trading pair (e.g., 'USDT').                                                   |
| settle        | str              | 'USDT'        | The settlement currency for the trading pair whenever the market type is swap. Options: USDT, USDC, COIN. |
| callType      | str              | 'ohlcv'       | The type of API call. Options: ohlcv (more options coming soon).                                          |
| exchangeId    | str              | 'binance'     | The ID of the exchange to fetch data from. Options: All [supported exchanges](https://github.com/ccxt/ccxt/wiki/Exchange-Markets) on CCXT.                      |

## TODO
* Add more call types (like fundingRateHistories, tickers, ...)