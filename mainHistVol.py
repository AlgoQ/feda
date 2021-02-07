from histCryptoDatafeed import histCryptoDatafeed
import ccxt

exchange = ccxt.binance({
    'enableRateLimit': True
})

allPairs = exchange.fetch_markets()

btcPairs = []
for pair in allPairs:
    if pair['quote'] == 'BTC':
        btcPairs.append(pair['symbol'])

tickers = exchange.fetch_tickers(btcPairs)
btcPairs2 = []

for symbol, value in tickers.items():
    if float(value['quoteVolume']) > 200:
        btcPairs2.append(symbol)

btcPairs2.remove('SXP/BTC')
btcPairs2.remove('IRIS/BTC')
btcPairs2.remove('FIO/BTC')
btcPairs2.remove('SOL/BTC')
btcPairs2.remove('SNX/BTC')
btcPairs2.remove('CHR/BTC')
btcPairs2.remove('FTT/BTC')
btcPairs2.remove('CTSI/BTC')
btcPairs2.remove('KAVA/BTC')

for pair in btcPairs2:
    datamanager = histCryptoDatafeed(fileName=f'data_binance/ohlcv_binance_{pair}_365days.json', pair=pair, days=365, strExchange='binance')

ohlcv_binance_BTCUSDT = datamanager.fetchDatafeed()