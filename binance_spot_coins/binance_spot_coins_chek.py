import keys, requests, websockets, asyncio, time, json, pprint, pandas as pd, unicorn_binance_websocket_api
from binance.client import Client

# Массив. Будет хранить все спотовые монеты.
spot_list = []
# Массив. Будет хранить все фьючерсные монеты.
futures_list = []
is_futures = []

client = Client(keys.BINANCE_API_KEY, keys.BINANCE_API_SECRET)

# . Функция. Возвращает список всех спотовых монет.
def get_spot_list():
    global spot_list
    spot_info = client.get_exchange_info()

    for x in range(0, len(spot_info['symbols'])):
        symbol = spot_info['symbols'][x]['symbol']
        # Выводим эти значения

        try:
            # Пробуем.
            is_spot = spot_info['symbols'][x]['permissions'][0]
        except:
            pass
        if (is_spot == "SPOT"):
            # Добавление в конец списка 'spot_list' значения 'symbol'
            spot_list.append(symbol)

    return spot_list

def get_futures_list():
    global futures_list
    futures_info = client.futures_exchange_info()

    for x in range(0, len(futures_info['symbols'])):
        symbol = futures_info['symbols'][x]['symbol']

        try:
            is_futures = futures_info['symbols'][x]['contractType']

        except:
            pass
        if (is_futures == 'PERPETUAL'):
            futures_list.append(symbol)
    return futures_list


def sort_list(list):
    df = pd.DataFrame(list, columns=['symbol'])

a1 = get_spot_list()
a2 = get_futures_list()

print(a1)
print(a2)

