import sys
import os
import GLOBAL
sys.path.append("/dll")
import talib
import func
from pynput.keyboard import Key, Listener
from tbot_binance_001 import input_var
#import keys
import keys_test as keys
from binance.client import Client
from tbot_binance_001.func import  fn_create_logfile, on_release, on_press
from tbot_binance_001.func import fn_pause, fn_write_logfile_msg
from tbot_binance_001.fn_print import fn_print_header, fn_print_current_status
from tbot_binance_001.fn_trade import fn_get_balance, fn_get_price, fn_control_start_param, fn_get_data, fn_place_order
from datetime import datetime
import time

from pynput import keyboard



PRICE_SELL = 0                #
PRICE_SELL_MIN = 0  # Минимально допустимая цена продажи, раасчитвается как PRICE_BUY + PRICE_DIFF (%)
PRICE_DIFF_CURRENT = 0
# PRICE_TOKEN2_CURRENT - Текущая цена токена
# PRICE_START_TOKEN_2  - Цена ТОКЕН2 на момент старта
CURRENT_ORDER = 'Ордеров не было'
# До первого ордера = 0, Купил, дждет продажу = 1, Продал, ждет покупку = -1
CURRENT_STATUS = 0

# ======================= СТАРТ СКРИПТА =====================

DATETIME_START = datetime.now().strftime('%Y.%m.%d  %H:%M:%S') # Переменная сохраняет знаяение даты и времени в виде строки.
# Формирование имени ЛОГ файла.
LOGFILE_NAME = (input_var.DIR_LOG + input_var.BOTNAME + "_" + datetime.now().strftime('<%Y.%m.%d  %H:%M:%S>') + ".log")
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
    # Подключение к ТЕСТОВОЙ СРЕДЕ!!!
    CLIENT = Client(keys.BINANCE_API_KEY, keys.BINANCE_API_SECRET, testnet=True)
    #CLIENT = Client(keys.BINANCE_API_KEY, keys.BINANCE_API_SECRET)
except:
#    fn_telegram_send_msg(keys.TELEGRAM_TOKEN, keys.TELEGRAM_CHAT_ID, datetime.now().strftime('<%Y.%m.%d  %H:%M:%S>') + '   ' + config_var.msg_telegram_error_exchange_connect)
    sys.exit("Ошибка подключения к бирже. Завершение работы программы.")
else:
#    fn_telegram_send_msg(keys.TELEGRAM_TOKEN, keys.TELEGRAM_CHAT_ID, datetime.now().strftime('<%Y.%m.%d  %H:%M:%S>') + '   ' + config_var.msg_telegram_success_exchange_connect)
    fn_write_logfile_msg(LOGFILE_NAME, datetime.now(), ' <OK> Подключение к бирже прошло успешно')


try:

    BALANCE_START_TOKEN_1, BALANCE_LOCKED_START_TOKEN_1 = fn_get_balance(CLIENT, input_var.TOKEN_1)
    BALANCE_START_TOKEN_2, BALANCE_LOCKED_START_TOKEN_2 = fn_get_balance(CLIENT, input_var.TOKEN_2)

    # Запрос текущей цены ТОКЕНА2
    PRICE_TOKEN2_CURRENT=fn_get_price(input_var.SYMBOL, input_var.URL)
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
index_control, msg_control = fn_control_start_param(CLIENT, input_var.SYMBOL, input_var.TOKEN_1, BALANCE_START_TOKEN_1, input_var.TOKEN_2, PRICE_TOKEN2_CURRENT, input_var.QNTY)
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


def main():
    global BALANCE_CURRENT_TOKEN_1, BALANCE_LOCKED_CURRENT_TOKEN_1, BALANCE_CURRENT_TOKEN_2, BALANCE_LOCKED_CURRENT_TOKEN_2
    global PRICE_TOKEN_2_CURRENT, RSI_CURRENT, PRICE_START_TOKEN_2, KEY




    KEY = ''

    PRICE_START_TOKEN_2 = fn_get_price(input_var.SYMBOL, input_var.URL)
    GLOBAL.PRICE_BUY_TOKEN_2 = 0        # При запуске = 0, потом туда поместится цена купленного токена.

    # Пара индексов. Определяют статус ордера ПОКУПКА - ПРОДАЖА .(buy=False и sell=True)-Ожидание покупки.(buy=True и sell=False)-Ожидание продажи.
    buy = False     #  buy = False - значит, что мы еще ничего не купили. buy = True - значит, мы что то купили и нужно продать
    sell = True     #  sell = True - значи, что мы все продали и продавать НЕЧЕГО! . Если sell = False - значит, мы еще не продали и нужно продавать.

    while True:


        # ======= РАСЧЕТ ПАРАМЕТРОВ ДЛЯ ТОРГОВ =====
        BALANCE_CURRENT_TOKEN_1, BALANCE_LOCKED_CURRENT_TOKEN_1 = fn_get_balance(CLIENT, input_var.TOKEN_1)
        BALANCE_CURRENT_TOKEN_2, BALANCE_LOCKED_CURRENT_TOKEN_2 = fn_get_balance(CLIENT, input_var.TOKEN_2)
        # Расчет текущего значения индикатора RSI_CURRENT
        closing_data = fn_get_data(input_var.URL_BINANCE_GET_CANDLES_INTERVAL_LIMIT, input_var.SYMBOL, input_var.INTERVAL, input_var.RSI_LIMIT)
        RSI_CURRENT = talib.RSI(closing_data, input_var.RSI_PERIOD)[-1]
        # Получение текущей цены ТОКЕНА_2
        PRICE_TOKEN_2_CURRENT = fn_get_price(input_var.SYMBOL, input_var.URL)

        # ========= ТЕСТ Ручной ввод RSI_CURRENT
        #RSI_TEST_INPUT = input('Введите значение RSI_CURRENT: ')
        #RSI_CURRENT = int(RSI_TEST_INPUT)

        # Если ордеры на покупку уже былы, то PRICE_BUY содержит цену покупки и <> 0. Расчет текущей разницы в % и Допустимой минимальной цены продажи.
        if (GLOBAL.PRICE_BUY_TOKEN_2 != 0):
            GLOBAL.PRICE_DIFF_CURRENT = (PRICE_TOKEN_2_CURRENT - GLOBAL.PRICE_BUY_TOKEN_2) / GLOBAL.PRICE_BUY_TOKEN_2 * 100
            PRICE_SELL_MIN = GLOBAL.PRICE_BUY_TOKEN_2 + GLOBAL.PRICE_BUY_TOKEN_2 / 100 * input_var.PRICE_DIFF

        # Условие для покупки токена: Только по текущему значению RSI
        if ((RSI_CURRENT <= input_var.RSI_MIN and not buy) or GLOBAL.ORDER_MANUAL_SET == 'BUY'):
            # ВЫзов функции создания ордеоа с параметром на покупку
            # Фиксируем цену закупки в глобальную переменную PRICE_BUY_TOKEN_2
            # Сбрасываем глобальную переменную, если мы создали ордер по ней, ее нужно обнулить.

            GLOBAL.PRICE_BUY_TOKEN_2 = PRICE_TOKEN_2_CURRENT

            fn_place_order('BUY', RSI_CURRENT, keys.BINANCE_API_KEY, keys.BINANCE_API_SECRET)
            print('buy=', buy,' sell=', sell )
            # Переворачиваем индексы.
            buy = not buy
            sell = not sell

            if (GLOBAL.ORDER_MANUAL_SET == 'BUY'):
                GLOBAL.ORDERS_NUMBER_BUY_MANUAL = GLOBAL.ORDERS_NUMBER_BUY_MANUAL + 1
                buy = not buy
                sell = not sell
            print('buy=', buy,' sell=', sell )
            GLOBAL.ORDER_MANUAL_SET = ''
            # Увеличиваем счетчик ордеров на покупку на 1

            GLOBAL.ORDERS_NUMBER_BUY = GLOBAL.ORDERS_NUMBER_BUY + 1
            GLOBAL.ORDERS_NUMBER_BUY_AUTO = GLOBAL.ORDERS_NUMBER_BUY - GLOBAL.ORDERS_NUMBER_BUY_MANUAL

            #  ===========ТЕСТ=========== Условия на продажу. По текущему значению RSI
        if ((RSI_CURRENT >= input_var.RSI_MAX and not sell) or GLOBAL.ORDER_MANUAL_SET == 'SELL'):
            buy = not buy
            sell = not sell
            # Если продажа была РУЧНАЯ (ар установке переменной GLOBAL.ORDER_MANUAL_SET), то переменную ОБНУДИТЬ и ЛОГИКУ исправить
            if (GLOBAL.ORDER_MANUAL_SET == 'SELL'):
                GLOBAL.ORDERS_NUMBER_SELL_MANUAL = GLOBAL.ORDERS_NUMBER_SELL_MANUAL + 1
                GLOBAL.ORDER_MANUAL_SET = ''
                fn_pause()
                buy = not buy
                sell = not sell
        # ========= РОБОЧИЙ ======Условия на продажу. По текущему значению RSI и чтобы навар был не меньше фиксированного
        #if (RSI_CURRENT >= input_var.RSI_MAX and GLOBAL.PRICE_DIFF_CURRENT >= input_var.PRICE_DIFF and not sell):
            # ВЫзов функции создания ордеоа с параметром на продажу

            fn_place_order('SELL', RSI_CURRENT, keys.BINANCE_API_KEY, keys.BINANCE_API_SECRET)

            # Сбрасываем глобальную переменную, если мы создали ордер по ней, ее нужно обнулить.

            print('buy=', buy, ' sell=', sell)

            # Увеличиваем счетчик ордеров на покупку на 1
            GLOBAL.ORDERS_NUMBER_SELL = GLOBAL.ORDERS_NUMBER_SELL + 1
            # Расчет общего колва автоматических ордеров на продажу
            GLOBAL.ORDERS_NUMBER_SELL_AUTO = GLOBAL.ORDERS_NUMBER_SELL - GLOBAL.ORDERS_NUMBER_SELL_MANUAL
            print('buy=', buy, ' sell=', sell)

        if (buy == False and sell == True):
            MSG_ORDER_STATUS = 'ОЖИДАНИЕ УСЛОВИЙ ДЛЯ ПОКУПКИ'
        else:
            MSG_ORDER_STATUS = 'ОЖИДАНИЕ УСЛОВИЙ ДЛЯ ПРОДАЖИ'

        os.system('clear')
        # ======= Печать в реминал ТЕКУЩЕГО СТАТУСА РАБОТЫ =====
        fn_print_current_status(DATETIME_START, BALANCE_START_TOKEN_1, BALANCE_CURRENT_TOKEN_1, BALANCE_LOCKED_CURRENT_TOKEN_1,\
                                BALANCE_START_TOKEN_2, BALANCE_CURRENT_TOKEN_2, BALANCE_LOCKED_CURRENT_TOKEN_2, PRICE_START_TOKEN_2,PRICE_TOKEN_2_CURRENT, RSI_CURRENT, MSG_ORDER_STATUS)
        print('buy=', buy, ' sell=', sell)

        # Прослушивание и перехват нажатия кнопок
        listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release)
        listener.start()
        # Обработка нажатых клавиш
        if (GLOBAL.PRESS_KEY == 'b'):
            print('GLOBAL.ORDER_MANUAL_SET => BUY')
            GLOBAL.ORDER_MANUAL_SET = 'BUY'
            #input_buy_char = input('СФОРМИРОВАТЬ ОРДЕР НА ПОКУПКУ? Y/n:')
            #if (input_buy_char == 'Y'):
            #    print('GLOBAL.ORDER_MANUAL_SET => BUY')
            #    GLOBAL.ORDER_MANUAL_SET = 'BUY'
            #    fn_pause()
        if (GLOBAL.PRESS_KEY == 's'):
            print('GLOBAL.ORDER_MANUAL_SET => SELL')
            GLOBAL.ORDER_MANUAL_SET = 'SELL'
            #input_buy_char = input('СФОРМИРОВАТЬ ОРДЕР НА ПРОДАЖУ? Y/n:')
            #if (input_buy_char == 'Y'):
            #    print('GLOBAL.ORDER_MANUAL_SET => SELL')
            #    GLOBAL.ORDER_MANUAL_SET = 'SELL'
            #    fn_pause()
        if (GLOBAL.PRESS_KEY == 'q'):
            input_buy_char = input('ЗАКОНЧИТЬ ВЫПОЛНЕНИЕ ПРОГРАММЫ? y/n:')
#            sys.exit('ЗАВЕРШЕНИЕ ПРОГРАММЫ ПО ТРЕБОВАНИЮ ПОЛЬЗОВАТЕЛЯ.....')
            if (input_buy_char == 'y'):
                sys.exit('ЗАВЕРШЕНИЕ ПРОГРАММЫ ПО ТРЕБОВАНИЮ ПОЛЬЗОВАТЕЛЯ.....')

if __name__ == '__main__':

    main()

