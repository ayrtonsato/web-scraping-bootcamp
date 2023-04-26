import requests as r
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class Stock:
    ticker: str
    exchange: str
    price: float = 0
    currency: str = "USD"
    usd_price: float = 0

    def __post_init__(self):
        price_info = get_price_information(self.ticker, self.exchange)
        if price_info["ticker"] == self.ticker:
            self.price = price_info["price"]
            self.usd_price = price_info["usd_price"]
            self.currency = price_info["currency"]


@dataclass
class Position:
    stock: Stock
    quantity: int


@dataclass
class Portifolio:
    positions: list[Position]

    def get_total_value(self):
        total_value = 0
        for position in self.positions:
            total_value += position.quantity * position.stock.usd_price
        return total_value


BASE_REQUEST = "www.google.com/finance/quote/MSFT:NASDAQ"


def get_fx_to_usd(currency):
    fx_url = f"https://www.google.com/finance/quote/{currency}-USD"
    resp = r.get(fx_url)
    soup = BeautifulSoup(resp.content, features="html.parser")
    fx_rate = soup.find("div", {"data-last-price": True})
    fx = float(fx_rate["data-last-price"])
    return fx


def get_price_information(ticker, exchange):
    url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"
    resp = r.get(url)
    soup = BeautifulSoup(resp.content, features="html.parser")

    price_div = soup.find("div", attrs={"data-last-price": True})
    price = float(price_div["data-last-price"])
    currency = price_div["data-currency-code"]

    usd_price = price
    if currency != "USD":
        fx = get_fx_to_usd(currency)
        usd_price = round(price * fx, 2)

    return {
        "ticker": ticker,
        "exchange": exchange,
        "price": price,
        "currency": currency,
        "usd_price": usd_price
    }


if __name__ == "__main__":
    # print(get_price_information("MSFT", "NASDAQ"))
    # print(get_price_information("SHOP", "TSE"))
    shop = Stock("SHOP", "TSE")
    msft = Stock("MSFT", "NASDAQ")
    googl = Stock("GOOGL", "NASDAQ")

    portifolio = Portifolio([Position(shop, 10), Position(msft, 2), Position(googl, 30)])

    print(portifolio.get_total_value())
