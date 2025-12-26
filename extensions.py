import requests
import json
import cbrapi as cbr
from datetime import date
from config import keys

class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        
        if quote == base:
            raise ConvertionException(f'Не возможно перевести одинаковые валюты {base}!')
        
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}!')
        
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}!')
        
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать колличество {amount}!')
        
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = float(json.loads(r.content)[keys[base]]) * amount

        return total_base
    
    @staticmethod
    def cbr_price(quote: str, base: str, amount: float):    
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать колличество {amount}!')
        
        today = date.today()
        date_now = today.strftime("%Y-%m-%d")
        if base == 'рубль':
            r_cbr = cbr.get_time_series(symbol=keys[quote], first_date=date_now, last_date=date_now)
            total_cbr = float(r_cbr.iloc[0]) * amount
        elif quote == 'рубль':
            r_base = cbr.get_time_series(symbol=keys[base], first_date=date_now, last_date=date_now)
            total_cbr = float(1 / r_base.iloc[0]) * amount
        else:
            r_quote = cbr.get_time_series(symbol=keys[quote], first_date=date_now, last_date=date_now)
            r_base = cbr.get_time_series(symbol=keys[base], first_date=date_now, last_date=date_now)
            total_cbr = float(r_quote.iloc[0] / r_base.iloc[0]) * amount

        return total_cbr