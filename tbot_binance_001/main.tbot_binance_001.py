import input_var
import keys
from binance.client import Client
#from input_var import SYMBOL, INTERVAL, LIMIT, QNTY, URL, RSI_MIN, RSI_MAX, RSI_PERIOD, BOTNAME, EXCHANGE_COMISSION, PRICE_DIFF, TOKEN_1, TOKEN_2
from func import fn_print_header, fn_print_current_status, fn_create_logfile, fn_write_logfile_order_buy,fn_write_logfile_order_sell, fn_top_coin, fn_telegram_send_msg, fn_pause
from datetime import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
import pandas as pd
import asyncio
import talib
import time

import requests
import json
import numpy as np
import os

# Определение глобальных переменных:
BALANCE_START_TOKEN_1 = 0     # Баланс ТОКЕНА_1 на момент запуска скрипта
BALANCE_START_TOKEN_2 = 0     # Баланс ТОКЕНА_2 на момент запуска скрипта
BALANCE_CURRENT_TOKEN_1 = 0   # Актуальный (текущий) баланс ТОКЕНА_1
BALANCE_CURRENT_TOKEN_2 = 0   # Актуальный (текущий) баланс ТОКЕНА_2
PRICE_SELL = 0                #
PRICE_SELL_MIN = 0  # Минимально допустимая цена продажи, раасчитвается как PRICE_BUY + PRICE_DIFF (%)
PRICE_BUY = 0
PRICE_DIFF_CURRENT = 0
PRICE_CURRENT = 0
PRICE_START = 0
CURRENT_ORDER = 'Ордеров не было'
# До первого ордера = 0, Купил, дждет продажу = 1, Продал, ждет покупку = -1
CURRENT_STATUS = 0
# DATETIME_START - строковая переменная. Сожержит дату и время старта скрипта.
# LOGFILE_NAME - в переменной формируется имя лог файла.

# =========== СТАРТ СКРИПТА ==============
DATETIME_START = datetime.now().strftime('<%Y.%m.%d  %H:%M:%S>') # Переменная сохраняет знаяение даты и времени в виде строки.
# Отправка уваедомления в ТЕЛЕГРАМ БОТа о старте скрипта.
fn_telegram_send_msg(keys.TELEGRAM_TOKEN, keys.TELEGRAM_CHAT_ID, DATETIME_START+ '   ' +input_var.MSG_INFO_TELEGRAM_START_BOT)

# Подключение к Binance
try:
    CLIENT = Client(keys.BINANCE_API_KEY, keys.BINANCE_API_SECRET)

    print('ОК. Успешное подключение.')
except:
    print('ОШИБКА ПОДКЛЮЧЕНИЯ.')
fn_pause()

# Запрос баланса токенов, которыми будем торговать.
BALANCE_START_TOKEN_1 = CLIENT.get_asset_balance(asset=input_var.TOKEN_1)
BALANCE_START_TOKEN_2 = CLIENT.get_asset_balance(asset=input_var.TOKEN_2)
print(BALANCE_START_TOKEN_1)
print(BALANCE_START_TOKEN_2)

key = input_var.URL.format(input_var.SYMBOL)
data = requests.get(key)
data = data.json()
print(data)
price = float((f"{data['price']}"))
print (price)

# Формирование имени ЛОГ файла.
LOGFILE_NAME = (input_var.BOTNAME + "_" + DATETIME_START + ".log")
# Создание лог файла
#(logfile_name, datetime_now, botname, symbol, token_1, balance_start_token1, token_2, balance_start_token2 ,interval, limit, rsi_min, rsi_max, rsi_period, qnty ):
#fn_create_logfile(LOGFILE_NAME, DATETIME_START, input_var.BOTNAME, input_var.SYMBOL, input_var.TOKEN_1, input_var.TOKEN_2, )

fn_pause()
print(LOGFILE_NAME)




