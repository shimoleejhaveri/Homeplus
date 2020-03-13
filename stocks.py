import requests

def get_stocks_by_symbols(symbols, api_key):
    """Get a closing price lists of all stocks in symbols list."""

    closing_price_list = {}

    for symbol in symbols:

        payload={'function': 'TIME_SERIES_INTRADAY',
                'symbol': symbol,
                'interval': '5min',
                'apikey': api_key}

        url = requests.get("https://www.alphavantage.co/query", params=payload)
        open_page = url.json()

        time_series = open_page.get('Time Series (5min)')

        if time_series:
            time_stamp = list(time_series.keys())[0]
            stocks = time_series[time_stamp]
            stock_info = list(stocks.keys())[3]
            closing_price = str(round(float(stocks[stock_info]), 2))
            closing_price_list[symbol] = closing_price

    return closing_price_list