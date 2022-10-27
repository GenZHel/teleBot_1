import requests
import json
from config import keys


class ConvertionException(Exception):
    pass


class ValueConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: float):

        if quote == base:
            raise ConvertionException(f'Невозможно перевести "{quote}" в "{base}"!')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту "{quote}"')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту "{base}"')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать валюту "{amount}"')

        r = requests.get(f'https://api.tinkoff.ru/v1/currency_rates?from={quote_ticker}&to={base_ticker}')
        text = json.loads(r.content)['payload']['rates']
        dict_1 = text[0]
        price = round(dict_1['buy'] * amount, 5)
        return price
