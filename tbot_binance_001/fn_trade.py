import requests
import numpy as np
import sys
import keys
from datetime import datetime
from func import fn_pause
from binance.client import Client
from tbot_binance_001 import input_var


# Функция возвращает торговую пару, самых торгуемых в данный момент токенов.
def fn_top_coin(pd, client):
    all_tickers = pd.DataFrame(client.get_ticker())
    usdt = all_tickers[all_tickers.symbol.str.contains('USDT')]
    work = usdt[~((usdt.symbol.str.contains('UP')) | (usdt.symbol.str.contains('DOWN')))]
    top_coin = work[work.priceChangePercent == work.priceChangePercent.max()]
    top_coin = top_coin.symbol.values[0]
    return top_coin


# Функция возвращает пул значений - цен закрытия свечей. Кол-во- это лимит, для указанного таймфрейма
def fn_get_data(url_candles_interval_limit, symbol, time_frame_interval, rsi_limit):
    url = url_candles_interval_limit.format(symbol, time_frame_interval, rsi_limit)
    res = requests.get(url)
    return_data = []
    for each in res.json():
        # Берем 4-й столбец. Это цена закрытия
        return_data.append(float(each[4]))
    return np.array(return_data)


# Функция возвращает свободный баланс и заблокированный баланс (в открытых ордерах) токена
def fn_get_balance(client, token):
    balance = client.get_asset_balance(asset=token)
    balance_free = float((f"{balance['free']}"))
    balance_locked = float((f"{balance['locked']}"))
    return balance_free, balance_locked

# Возвращает текущую цену токена
def fn_get_price(symbol, url):
    key = url.format(symbol)
    data = requests.get(key)
    data = data.json()
    price = float((f"{data['price']}"))
    return price

# Функция контроля корректности входных параметров.
def fn_control_start_param(client, symbol,token1, balance_start_token_1, token2, price_token2_current, qnty):
    # Запрос информации по токену (формат- dict, вложенный список )
    symbol_info = client.get_symbol_info(symbol)

    # Вытаскиваем из вложенного списка, второй список с индексом 'filters'
    symbol_info_filters = dict(symbol_info['filters'][2])
    # Вытаскиваем значение под индексом 'minNotional' - это МИНИМАЛЬНАЯ СУММА СДЕЛКИ допустимая биржей
    symbol_info_filters_minNotional = symbol_info_filters.get('minNotional')
    order_min_cost = float(symbol_info_filters_minNotional)

#    print (price_token2_current)
#    print (price_token2_current*qnty)
#    print (balance_start_token_1)

    if (balance_start_token_1 == 0):          # Если нет средств на TOKEN1 - это то, за что мы покупаем ТОКЕН2
        control_index = 0                     # control_index = 0 -при ОШИБКАХ control_index = 1 -все ОК
        msg_control_status = ' <ERROR> Торги не возможны. Начальный баланс '+ token1 + ' = 0'
    elif (price_token2_current*qnty > balance_start_token_1): # Если не хватает ТОКЕН1 для покупки указанного кол-ва ТОКЕН2
        control_index = 0
        msg_control_status = ' <ERROR> ОШИБКА ВХОДНЫХ ПАРАМЕТРОВ. Начального баланса ' + token1 +' = ' +str(balance_start_token_1) + ' не хватает для покупки ' + str(qnty) + ' токенов '+ token2 + ' За имеющийся баланс можно купить только ' + str(round(balance_start_token_1/price_token2_current,2)) + ' ' +token2
    elif (price_token2_current*qnty < order_min_cost ):   # Если сумма сделки меньше допустимого биржей значения
        control_index = 0
        #                                                      приводим к строке(округляет до 2 знака
        msg_control_status = ' <ERROR> Сумма сделки составляет - '+ str(round(price_token2_current*qnty,2))+ ' '+ token1+ ', что меньше допустимого значения, равного - ' + str(order_min_cost) + ' '+ token1+'. Измените входные параметры !!!'

    else:
        control_index = 1
        msg_control_status = ' <OK> Проверка входных параметров выполнена успешно. Расчетная сумма сделки составляет - ' + str(round(price_token2_current*qnty,2)) + ' '+token1
    return control_index, msg_control_status

def fn_place_order(order_type, client, api_key, api_secret):
    CLIENT = Client(api_key, api_secret, testnet=True)
    print('Функция формирования ордера ЗАПУЩЕНА')
    fn_pause()
    if(order_type == 'BUY'):
        # Попытка размещения ордера на покупку
        try:
            print('Попытка размещения ордера на ПОКУПКУ')
            order = CLIENT.create_order(symbol=input_var.SYMBOL, side=order_type, type='MARKET', quantity=input_var.QNTY)
        except:
            print('ОШИБКА размещения ордера на ПОКУПКУ')
            sys.exit("ОШИБКА размещения ордера на ПОКУПКУ")
        else:
            print(order, 'Размещение ордера на ПОКУПКУ прошло УСПЕШНО')

    if(order_type == 'SELL'):
        print('Размещаем ордер на ПРОДАЖУ')
            # Попытка размещения  ордера на ПРОДАЖУ
        try:
            print('Попытка размещения ордера на ПРОДАЖУ')
            order = CLIENT.create_order(symbol=input_var.SYMBOL, side=order_type, type='MARKET', quantity=input_var.QNTY)
        except:
            print('ОШИБКА размещения ордера на ПРОДАЖУ')
            sys.exit("ОШИБКА размещения ордера на ПРОДАЖУ")
        else:
            print(order, 'Размещение ордера на ПРОДАЖУ прошло УСПЕШНО')

    print('Функция формирования ордера ОТРАБОТАЛА')




