import finnhub
import os
import datetime


def get_finnhub_client():
    api_key = os.getenv("API_KEY")
    return finnhub.Client(api_key=api_key)


def get_current_stock_price(symb):
    finnhub_client = get_finnhub_client()
    finn_data = finnhub_client.quote(symb)
    return finn_data["c"]


def get_candle_stock_price(symb):
    finnhub_client = get_finnhub_client()
    current_time = datetime.datetime.utcnow()
    end_interval = int(current_time.timestamp())
    start_interval = int((current_time - datetime.timedelta(days=365)).timestamp())
    stock_history = finnhub_client.stock_candles(
        symb, "W", start_interval, end_interval
    )
    stock_history = stock_history["c"]
    return stock_history


def get_stock_list(symb):
    finnhub_client = get_finnhub_client()
    stock_list = finnhub_client.symbol_lookup(symb)
    stock_list = stock_list["result"][:10]
    return [
        {"company": stock["description"], "symb": stock["symbol"]}
        for stock in stock_list
    ]


def get_company_info(symb):
    finnhub_client = get_finnhub_client()
    company = finnhub_client.company_profile2(symbol=symb)
    return {company["country"], company["ipo"], company["name"], company["ticker"]}
