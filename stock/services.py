from typing import Optional
import finnhub
import os
import datetime


class FinnHub:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.client = finnhub.Client(api_key=self.api_key)

    def get_current_stock_price(self, symb: str) -> Optional[dict[str, float]]:
        finn_data = self.client.quote(symb)
        if finn_data["c"] > 0 and finn_data["dp"]:
            return {"price": finn_data["c"], "change": finn_data["dp"]}
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

    def get_stock_by_search(self, symb: str) -> Optional[list[dict[str, str]]]:
        stock_list = self.client.symbol_lookup(symb)
        if stock_list["count"]:
            stock_companies = stock_list["result"]
            return (
                {
                    "symbol": stock_company["symbol"],
                    "name": stock_company["description"],
                }
                for stock_company in stock_companies
            )
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


def seconds_to_minute_change() -> int:
    now = datetime.datetime.now()
    if now.minute == 59:
        next_minute = datetime.datetime(now.year, now.month, now.day, now.hour + 1, 0)
    else:
        next_minute = datetime.datetime(
            now.year, now.month, now.day, now.hour, now.minute + 1
        )
    return (next_minute - now).seconds


def get_stock(r, finn_client: FinnHub, symbol: str) -> dict[str, float]:
    quote = r.get(f"{symbol}")
    if not quote:
        quote = finn_client.get_current_stock_price(symbol)
        if quote:
            r.set(
                f"{symbol}",
                f"{quote['price']}|{quote['change']}",
                seconds_to_minute_change(),
            )
        else:
            return
    else:
        price, change = str(quote).split("|")
        quote = {"price": price, "change": change}
    return quote
