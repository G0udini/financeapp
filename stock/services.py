from typing import Optional
import finnhub
import os
import datetime


class FinnHub:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.client = finnhub.Client(api_key=self.api_key)

    def get_current_stock_price(self, symb: str) -> Optional[float]:
        finn_data = self.client.quote(symb)
        if finn_data["c"]:
            return finn_data["c"]
        return

    def get_candle_stock_price(self, symb: str) -> Optional[list[float]]:
        current_time = datetime.datetime.utcnow()
        end_interval = int(current_time.timestamp())
        start_interval = int((current_time - datetime.timedelta(days=365)).timestamp())
        stock_history = self.client.stock_candles(
            symb, "W", start_interval, end_interval
        )
        if stock_history["s"] == "no_data":
            return
        stock_history = stock_history["c"]
        return stock_history

    def get_stock_by_search(
        self, symb: str, cnt: int = 5
    ) -> Optional[list[dict[str, str]]]:
        stock_list = self.client.symbol_lookup(symb)
        if stock_list["count"]:
            if cnt:
                stock_companies = stock_list["result"]
                return (
                    {
                        "symbol": stock_company["symbol"],
                        "name": stock_company["description"],
                    }
                    for stock_company in stock_companies
                )
            else:
                stock_company = stock_list["result"][cnt]
                return {
                    "symbol": stock_company["symbol"],
                    "name": stock_company["description"],
                }
        return

    def get_company_info(self, symb: str) -> Optional[dict[str, str]]:
        company = self.client.company_profile2(symbol=symb)
        if company:
            return {
                "country": company["country"],
                "ipo": company["ipo"],
                "name": company["name"],
                "symbol": company["ticker"],
            }
        return

    def search_for_company_info(self, symb: str) -> Optional[dict[str, str]]:
        try:
            intermediate_result = self.get_stock_by_search(symb, 0)["symbol"]
        except TypeError:
            return
        else:
            return self.get_company_info(intermediate_result)
