import keys, requests, websockets, asyncio, time, json, pprint, pandas as pd, unicorn_binance_websocket_api
from binance.client import Client

# Массив. Будет хранить все спотовые монеты.
spot_list = []
# Массив. Будет хранить все фьючерсные монеты.
futures_list = []
volume_dict = {}
extremem_dict = {}
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


# Функция сортировки, фильтрации и отсеивания ненужные
def sort_list(list):
    df = pd.DataFrame(list, columns=['symbol'])
    df = df[~(df.symbol.str.contains("BULL|BEAR"))]
    df = df[~(df.symbol.str.contains("BUSD|USDC"))]
    df = df[df.symbol.str.contains("USDT")]
    getted_list = df['symbol'].to_list()
#    print(getted_list)
    return getted_list


# Функция получает свечи. НЕ РАБОТАЕТ!!!
def get_klines(symbol_list):
    global extremem_dict
    global volume_dict
    df = pd.DataFrame(columns=[symbol_list], index=['high', 'low'])
    for symbol in symbol_list:
        kline = client.get_klines(symbol=symbol, interval=client.KLINE_INTERVAL_1DAY, limit=1)
        df.loc['high', symbol] = float(kline[0][2])  # Хаи интересующей монеты
        df.loc['low', symbol] = float(kline[0][3])  # Лои (низы) интересующей монеты
        volume_dict[symbol] = None
    # Отсмортируем Дата фреймы
    df = df.T
    data_dict = df.to_dict()
    for symbol, value_dict in data_dict.items():
        for key in value_dict.keys():
            extremem_dict[key[0]] = {'high': data_dict['high'][key], 'low': data_dict['low'][key]}
    #print(extremum_dict)


a1 = get_spot_list()
a2 = get_futures_list()

b1 = sort_list(a1)

#print(b1)

