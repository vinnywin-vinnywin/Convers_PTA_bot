import json
import requests
from config import keys

#класс "отлова" исключений неправильного ввода пользователем
class ConvertionException(Exception):
    pass
#
class APIException:
    @staticmethod
    def get_price(quote: str, base: str, amount: str): #статический метод
        if quote == base:  # обработка невозможности конвертации одинаковых валют
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}.')
        # присваиваем валюты в переменные и проверяем их наличие в списке Key
        try:
            quote_ticket = keys[quote]
        except KeyError:
            raise ConvertionException(f'Нет информации по валюте {quote}.')
        # присваиваем валюты в переменные и проверяем их наличие в списке Key
        try:
            base_ticket = keys[base]
        except KeyError:
            raise ConvertionException(f'Нет информации по валюте {base}.')
        # проверяем, что кол-во переводимой валюты явяется числом
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать указанное количество {amount}.')

        # отправляем запрос стороннему API на конвертацию
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticket}&tsyms={base_ticket}')
        #total_base = json.loads(r.content)[base_ticket]
        total_base = json.loads(r.content)[keys[base]]
        total_base = total_base * amount

        return total_base