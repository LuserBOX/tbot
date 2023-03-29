import input_var
import config_var
import keys
from binance.client import Client
#from input_var import SYMBOL, INTERVAL, LIMIT, QNTY, URL, RSI_MIN, RSI_MAX, RSI_PERIOD, BOTNAME, EXCHANGE_COMISSION, PRICE_DIFF, TOKEN_1, TOKEN_2
from func import fn_print_header, fn_print_current_status, fn_create_logfile, fn_write_logfile_order_buy,fn_write_logfile_order_sell, fn_top_coin
from func import fn_telegram_send_msg, fn_pause, fn_get_price, fn_get_balance, fn_get_balance_locked, fn_write_logfile_msg, fn_control_start_param
from datetime import datetime
import sys
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
# BALANCE_START_TOKEN_1 = 0     # Баланс ТОКЕНА_1 на момент запуска скрипта
# BALANCE_START_TOKEN_2 = 0     # Баланс ТОКЕНА_2 на момент запуска скрипта
# BALANCE_LOCKED_START_TOKEN_1  # Баланс заблокированных ТОКЕНОВ_1 на момент запуска скрипта
# BALANCE_LOCKED_START_TOKEN_2  # Баланс заблокированных ТОКЕНОВ_2 на момент запуска скрипт
BALANCE_CURRENT_TOKEN_1 = 0   # Актуальный (текущий) баланс ТОКЕНА_1
BALANCE_CURRENT_TOKEN_2 = 0   # Актуальный (текущий) баланс ТОКЕНА_2
PRICE_SELL = 0                #
PRICE_SELL_MIN = 0  # Минимально допустимая цена продажи, раасчитвается как PRICE_BUY + PRICE_DIFF (%)
PRICE_BUY = 0
PRICE_DIFF_CURRENT = 0
# PRICE_TOKEN2_CURRENT - Текущая цена токена
PRICE_START = 0
CURRENT_ORDER = 'Ордеров не было'
# До первого ордера = 0, Купил, дждет продажу = 1, Продал, ждет покупку = -1
CURRENT_STATUS = 0
# DATETIME_START - строковая переменная. Содержит дату и время старта скрипта. Нужна для фиксации события и информировании с какого момента скрипт работает
# LOGFILE_NAME - в переменной формируется имя лог файла.

# ======================= СТАРТ СКРИПТА =====================
DATETIME_START = datetime.now().strftime('<%Y.%m.%d  %H:%M:%S>') # Переменная сохраняет знаяение даты и времени в виде строки.
# Формирование имени ЛОГ файла.
LOGFILE_NAME = (input_var.BOTNAME + "_" + datetime.now().strftime('<%Y.%m.%d  %H:%M:%S>') + ".log")
# Создание LOG файла
try:
    fn_create_logfile(LOGFILE_NAME, datetime.now(), input_var.BOTNAME, input_var.SYMBOL, input_var.INTERVAL, input_var.LIMIT, input_var.RSI_MIN, input_var.RSI_MAX, input_var.RSI_PERIOD, input_var.QNTY)
    print('Лог файл создан: '+ LOGFILE_NAME)
except:
    print ('Ошибка создания LOF файла')
# Отправка уваедомления в ТЕЛЕГРАМ БОТа о старте скрипта.
fn_telegram_send_msg(keys.TELEGRAM_TOKEN, keys.TELEGRAM_CHAT_ID, datetime.now().strftime('<%Y.%m.%d  %H:%M:%S>')+ '   ' +input_var.MSG_INFO_TELEGRAM_START_BOT)

# ============ Подключение к Binance ==========
try:
    CLIENT = Client(keys.BINANCE_API_KEY, keys.BINANCE_API_SECRET)
except:
    fn_telegram_send_msg(keys.TELEGRAM_TOKEN, keys.TELEGRAM_CHAT_ID, datetime.now().strftime('<%Y.%m.%d  %H:%M:%S>') + '   ' + config_var.msg_telegram_error_exchange_connect)
    sys.exit("Ошибка подключения к бирже. Завершение работы программы.")
else:
    fn_telegram_send_msg(keys.TELEGRAM_TOKEN, keys.TELEGRAM_CHAT_ID, datetime.now().strftime('<%Y.%m.%d  %H:%M:%S>') + '   ' + config_var.msg_telegram_success_exchange_connect)
    fn_write_logfile_msg(LOGFILE_NAME, datetime.now(), ' <OK> Подключение к бирже прошло успешно')

# Запрос информации по нашей торговой паре: балансы, в том числе заблокированные, минимальный размер ордера
try:
    BALANCE_START_TOKEN_1 = fn_get_balance(CLIENT, input_var.TOKEN_1)
    BALANCE_START_TOKEN_2 = fn_get_balance(CLIENT, input_var.TOKEN_2)
    BALANCE_LOCKED_START_TOKEN_1 = fn_get_balance_locked(CLIENT, input_var.TOKEN_1)
    BALANCE_LOCKED_START_TOKEN_2 = fn_get_balance_locked(CLIENT, input_var.TOKEN_2)
    # Запрос текущей цены ТОКЕНА2
    PRICE_TOKEN2_CURRENT=fn_get_price(input_var.SYMBOL,input_var.URL)
except:
    fn_write_logfile_msg(LOGFILE_NAME, datetime.now(), ' <ERROR> Ошибка при запросе Баланса токенов и цены')
    print ('<ERROR> Ошибка запроса баланса и стоимости ТОКЕН2 ')
    sys.exit("Ошибка при запросе Баланса токенов и цены . Завершение работы программы.")
else:
    fn_write_logfile_msg(LOGFILE_NAME, datetime.now(), ' <OK> Балансы токенов и цена с биржи получены успешно')
    print ('Запрос баланса и стоимости ТОКЕН2 проши успешно ')

# Проверка согласованности входных параметров. index_control=0 (ERROR) или 1 (OK) , msg_control - инфо строка, сообщение о результатах проверки
index_control, msg_control = fn_control_start_param(CLIENT, input_var.SYMBOL,input_var.TOKEN_1,BALANCE_START_TOKEN_1, input_var.TOKEN_2, PRICE_TOKEN2_CURRENT, input_var.QNTY)
# Если при проверке есть ошибки, выполнение прекращается с уведомлением о причине.
if (index_control == 0):
    fn_write_logfile_msg(LOGFILE_NAME, datetime.now(), msg_control)
    sys.exit(msg_control)
else:
    fn_write_logfile_msg(LOGFILE_NAME, datetime.now(), msg_control)
#    print(msg_control)
# Вывод на экран стартовых параметров для подтверждения
print('Подключение к бирже прошло успешно. Входные параметры согласованы. Проверьте входные данные. Для начала торговых операций нажмите ENTER ')
fn_print_header (input_var.SYMBOL, input_var.TOKEN_1, input_var.TOKEN_2, BALANCE_START_TOKEN_1, BALANCE_START_TOKEN_2, PRICE_TOKEN2_CURRENT, input_var.INTERVAL, input_var.LIMIT, input_var.RSI_MIN, input_var.RSI_MAX, input_var.RSI_PERIOD,input_var.QNTY)

fn_write_logfile_msg (LOGFILE_NAME, datetime.now(), ' <INFO> Ожидание подтверждения пользователя (Press the <ENTER> key to continue...) на начало торговых операций')


fn_pause()
# ====== ОШИБОК НЕТ. Продолжаем выполнение =========








