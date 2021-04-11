# FEDA
A user-friendly library to fetch kline (ohlcv) data from several crypto exchanges.

## Install
```shell
git clone https://github.com/JanssensKobe/feda
```

## Getting Started
```python
from feda import feda

# Create folder first
datamanager = feda(fileName='data/ohlcv_bybit_LINKUSDT_170days.json', pair='LINK/USDT', days=170, strExchange='bybit')

ohlcv = datamanager.fetchDatafeed() # Fetches klines and export them into file
```

## Supported Exchanges
| Logo        | Exchange        | strExchange    |
| ----------- | --------------- | -------------- |
| [![binance](https://user-images.githubusercontent.com/1294454/29604020-d5483cdc-87ee-11e7-94c7-d1a8d9169293.jpg)](https://www.binance.com/?ref=10205187) | Binance         | binance        |
| [![binance futures](https://user-images.githubusercontent.com/1294454/29604020-d5483cdc-87ee-11e7-94c7-d1a8d9169293.jpg)](https://www.binance.com/?ref=10205187) | Binance Futures | binanceFutures |
| [![ftx](https://user-images.githubusercontent.com/1294454/67149189-df896480-f2b0-11e9-8816-41593e17f9ec.jpg)](https://ftx.com/#a=1623029) | FTX | ftx |
| [![bybit](https://user-images.githubusercontent.com/51840849/76547799-daff5b80-649e-11ea-87fb-3be9bac08954.jpg)](https://www.bybit.com/app/register?ref=X7Prm) | Bybit | bybit |

## TODO
* Add more exchanges
* Add support for csv
