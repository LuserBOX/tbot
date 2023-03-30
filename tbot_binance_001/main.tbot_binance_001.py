import input_var
import keys
from binance.client import Client
import talib
#from input_var import SYMBOL, INTERVAL, RSI_LIMIT, QNTY, URL, RSI_MIN, RSI_MAX, RSI_PERIOD, BOTNAME, EXCHANGE_COMISSION, PRICE_DIFF, TOKEN_1, TOKEN_2

from func import  fn_create_logfile
from func import fn_pause, fn_write_logfile_msg
from fn_print import fn_print_header, fn_print_current_status
from fn_trade import fn_get_balance, fn_get_price, fn_control_start_param, fn_get_data
from datetime import datetime
import sys

import os

# Определение глобальных переменных:

# BALANCE_START_TOKEN_1         # Баланс ТОКЕНА_1 на момент запуска скрипта
# BALANCE_START_TOKEN_2         # Баланс ТОКЕНА_2 на момент запуска скрипта
# BALANCE_LOCKED_START_TOKEN_1  # Баланс заблокированных ТОКЕНОВ_1 на момент запуска скрипта
# BALANCE_LOCKED_START_TOKEN_2  # Баланс заблокированных ТОКЕНОВ_2 на момент запуска скрипт
# BALANCE_CURRENT_TOKEN_1         # Актуальный (текущий) баланс ТОКЕНА_1
# BALANCE_LOCKED_CURRENT_TOKEN_1  # Актуальный баланс заблокированных в ордерах ТОКЕНОВ1
# BALANCE_CURRENT_TOKEN_2         # Актуальный (текущий) баланс ТОКЕНА_2
# BALANCE_LOCKED_CURRENT_TOKEN_2  # Актуальный баланс заблокированных в ордерах ТОКЕНОВ2
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
DATETIME_START = datetime.now().strftime('%Y.%m.%d  %H:%M:%S') # Переменная сохраняет знаяение даты и времени в виде строки.
# Формирование имени ЛОГ файла.
LOGFILE_NAME = (input_var.DIR_LOG+input_var.BOTNAME + "_" + datetime.now().strftime('<%Y.%m.%d  %H:%M:%S>') + ".log")
# Создание LOG файла
try:
    fn_create_logfile(LOGFILE_NAME, datetime.now(), input_var.BOTNAME, input_var.SYMBOL, input_var.INTERVAL, input_var.RSI_LIMIT, input_var.RSI_MIN, input_var.RSI_MAX, input_var.RSI_PERIOD, input_var.QNTY)
    print('Лог файл создан: '+ LOGFILE_NAME)
except:
    print ('Ошибка создания LOF файла')
# Отправка уваедомления в ТЕЛЕГРАМ БОТа о старте скрипта.
#fn_telegram_send_msg(keys.TELEGRAM_TOKEN, keys.TELEGRAM_CHAT_ID, datetime.now().strftime('<%Y.%m.%d  %H:%M:%S>')+ '   ' +input_var.MSG_INFO_TELEGRAM_START_BOT)

# ============ Подключение к Binance ==========
try:
    CLIENT = Client(keys.BINANCE_API_KEY, keys.BINANCE_API_SECRET)
except:
#    fn_telegram_send_msg(keys.TELEGRAM_TOKEN, keys.TELEGRAM_CHAT_ID, datetime.now().strftime('<%Y.%m.%d  %H:%M:%S>') + '   ' + config_var.msg_telegram_error_exchange_connect)
    sys.exit("Ошибка подключения к бирже. Завершение работы программы.")
else:
#    fn_telegram_send_msg(keys.TELEGRAM_TOKEN, keys.TELEGRAM_CHAT_ID, datetime.now().strftime('<%Y.%m.%d  %H:%M:%S>') + '   ' + config_var.msg_telegram_success_exchange_connect)
    fn_write_logfile_msg(LOGFILE_NAME, datetime.now(), ' <OK> Подключение к бирже прошло успешно')

# Запрос информации по нашей торговой паре: балансы, в том числе заблокированные, минимальный размер ордера
try:
    BALANCE_START_TOKEN_1, BALANCE_LOCKED_START_TOKEN_1 = fn_get_balance(CLIENT, input_var.TOKEN_1)
    BALANCE_START_TOKEN_2, BALANCE_LOCKED_START_TOKEN_2 = fn_get_balance(CLIENT, input_var.TOKEN_2)

    # Запрос текущей цены ТОКЕНА2
    PRICE_TOKEN2_CURRENT=fn_get_price(input_var.SYMBOL,input_var.URL)
#    print('Баланс токена 1 free', BALANCE_START_TOKEN_1)
#    print('Баланс токена 1 locked', BALANCE_LOCKED_START_TOKEN_1)
#    print('Баланс токена 2 free', BALANCE_START_TOKEN_2)
#    print('Баланс токена 2 locked', BALANCE_LOCKED_START_TOKEN_2)
#    print('Цена Токена 2',PRICE_TOKEN2_CURRENT )

except:
    fn_write_logfile_msg(LOGFILE_NAME, datetime.now(), ' <ERROR> Ошибка при запросе Баланса токенов и цены')
    print ('<ERROR> Ошибка запроса баланса и стоимости ТОКЕН2 ')
    sys.exit("Ошибка при запросе Баланса токенов и цены . Завершение работы программы.")
else:
    fn_write_logfile_msg(LOGFILE_NAME, datetime.now(), ' <OK> Балансы токенов и цена с биржи получены успешно')
    print ('Запрос баланса и стоимости ТОКЕН2 проши успешно ')

# Проверка согласованности входных параметров. index_control=0 (ERROR) или 1 (OK) , msg_control - инфо строка, сообщение о результатах проверки
index_control, msg_control = fn_control_start_param(CLIENT, input_var.SYMBOL,input_var.TOKEN_1,BALANCE_START_TOKEN_1, input_var.TOKEN_2, PRICE_TOKEN2_CURRENT, input_var.QNTY)
# =============== Временное отключение проверки, для написания дальнейшего кода
#index_control = 1
#msg_control = ' <OK> Проверка входных параметров выполнена успешно. = ПРОВЕРКА ОТКЛЮЧЕНА!!!'
#================================================================================
# Если при проверке есть ошибки, выполнение прекращается с уведомлением о причине.
if (index_control == 0):
    fn_write_logfile_msg(LOGFILE_NAME, datetime.now(), msg_control)
    sys.exit(msg_control)
else:
    fn_write_logfile_msg(LOGFILE_NAME, datetime.now(), msg_control)
#    print(msg_control)
# Вывод на экран стартовых параметров для подтверждения
print('Подключение к бирже прошло успешно. Входные параметры согласованы. Проверьте входные данные. Для начала торговых операций нажмите ENTER ')
fn_print_header (input_var.SYMBOL, input_var.TOKEN_1, input_var.TOKEN_2, BALANCE_START_TOKEN_1, BALANCE_LOCKED_START_TOKEN_1, \
                 BALANCE_START_TOKEN_2, BALANCE_LOCKED_START_TOKEN_2, PRICE_TOKEN2_CURRENT, input_var.INTERVAL, input_var.RSI_LIMIT, \
                 input_var.RSI_MIN, input_var.RSI_MAX, input_var.RSI_PERIOD, input_var.QNTY)

fn_write_logfile_msg (LOGFILE_NAME, datetime.now(), ' <INFO> Ожидание подтверждения пользователя (Press the <ENTER> key to continue...) на начало торговых операций')

# ====== ЕСЛИ ОШИБОК НЕТ. Продолжаем выполнение =========
fn_pause()

def main():
    global BALANCE_CURRENT_TOKEN_1, BALANCE_LOCKED_CURRENT_TOKEN_1, BALANCE_CURRENT_TOKEN_2, BALANCE_LOCKED_CURRENT_TOKEN_2
    global PRICE_TOKEN_2_CURRENT, RSI_CURRENT

    # Пара индексов. Показывают состояние крипта.(buy=False и sell=True)-Ожидание покупки.(buy=True и sell=False)-Ожидание продажи.
    buy = False
    sell = True

    while True:
        os.system('clear')

        style = "\033[7m\033[33m{}"
        style = "\033[7m\033[33m{}"
        print("\033[33m{}".format('ПРИВЕТ!!!'))
        print("\033[1m\033[33m{}".format('ПРИВЕТ!!!'))
        print(style.format("ПРИВЕТ!!!'"))

        # ======= РАСЧЕТ ПАРАМЕТРОВ ДЛЯ ТОРГОВ =====
        BALANCE_CURRENT_TOKEN_1, BALANCE_LOCKED_CURRENT_TOKEN_1 = fn_get_balance(CLIENT, input_var.TOKEN_1)
        BALANCE_CURRENT_TOKEN_2, BALANCE_LOCKED_CURRENT_TOKEN_2 = fn_get_balance(CLIENT, input_var.TOKEN_2)
        PRICE_TOKEN_2_CURRENT = fn_get_price(input_var.SYMBOL, input_var.URL)


        closing_data = fn_get_data(input_var.URL_BINANCE_GET_CANDLES_INTERVAL_LIMIT, input_var.SYMBOL, input_var.INTERVAL, input_var.RSI_LIMIT)
        RSI_CURRENT = talib.RSI(closing_data, input_var.RSI_PERIOD)[-1]



        fn_print_current_status(DATETIME_START, BALANCE_START_TOKEN_1, BALANCE_CURRENT_TOKEN_1, BALANCE_LOCKED_CURRENT_TOKEN_1,\
                                BALANCE_START_TOKEN_2, BALANCE_CURRENT_TOKEN_2, BALANCE_LOCKED_CURRENT_TOKEN_2, PRICE_TOKEN_2_CURRENT, 85)



        fn_pause()



if __name__ == '__main__':

    main()

