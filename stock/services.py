import finnhub
import os
import datetime


class FinnHub:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.client = finnhub.Client(api_key=self.api_key)

    def get_current_stock_price(self, symb):
        finn_data = self.client.quote(symb)
        return finn_data["c"]

    def get_candle_stock_price(self, symb):
        current_time = datetime.datetime.utcnow()
        end_interval = int(current_time.timestamp())
        start_interval = int((current_time - datetime.timedelta(days=365)).timestamp())
        stock_history = self.client.stock_candles(
            symb, "W", start_interval, end_interval
        )
        stock_history = stock_history["c"]
        return stock_history

    def get_stock_list(self, symb):
        stock_list = self.client.symbol_lookup(symb)
        stock_list = stock_list["result"][:10]
        return [
            {"company": stock["description"], "symb": stock["symbol"]}
            for stock in stock_list
        ]

    def get_company_info(self, symb):
        company = self.client.company_profile2(symbol=symb)
        return {company["country"], company["ipo"], company["name"], company["ticker"]}
