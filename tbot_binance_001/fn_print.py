from colorama import init

init(autoreset=True)
from tbot_binance_001 import input_var
from colorama import init, Fore

init(autoreset=True)
from datetime import datetime


def fn_print_header (simbol, token_1, token_2, balance_start_token1, balance_start_locked_token1, balance_start_token2, balance_start_locked_token2,price_token2_current, interval, rsi_limit, rsi_min, rsi_max, rsi_period, qnty):
    print('Trading BOT: binance-rsi-001 STARTING....\n\n', Fore.RED +'  ПЕРЕД ЗАПУСКОМ ПЕРЕПРОВЕРЬТЕ ПАРАМЕТРЫ:')
    print(Fore.GREEN + \
          '============ ИНФОРМАЦИЯ О БАЛАНСЕ==========\n', \
          'Торговая пара           :', Fore.BLUE + simbol, '\n', \
          'Баланс       ', token_1, '      :', Fore.LIGHTGREEN_EX + str(balance_start_token1), '\n', \
          'Заблокировано', token_1, '      :', Fore.LIGHTRED_EX + str(balance_start_locked_token1), '\n', \
          'Баланс       ', token_2, '      :', Fore.LIGHTGREEN_EX + str(balance_start_token2), '\n', \
          'Заблокировано', token_2, '      :', Fore.LIGHTRED_EX + str(balance_start_locked_token2), '\n', Fore.GREEN +\
          '============ НАСТРОЙКИ ОРДЕРА =============\n', \
          'Ордер на покупку        :', qnty, token_2, '\n', \
          'Текущая цена 1', token_2, '     :', price_token2_current, token_1, '\n', \
          'Текущая стоиомть ордера :', round(price_token2_current * qnty, 2), token_1, '\n', Fore.GREEN +\
          '============ НАСТРОЙКИ ИНДИКАТОРОВ=========\n', \
          'TimeLine раб.облачти    :', interval, '\n', \
          'RSI Limit               :', rsi_limit, '\n', \
          'RSI Period              :', rsi_period, '\n', \
          'RSI Min                 :', rsi_min, '\n',\
          'RSI Max                 :', rsi_max, '\n',\
          'Quantity                :', qnty, '\n',Fore.GREEN +\
          '===========================================','\n',Fore.LIGHTWHITE_EX +\
          'ДЛЯ НАЧАЛА ТОРГОВЫХ ОПЕРАЦИЯ НАЖМИТЕ <ENTER> ....')

def fn_print_current_status (datetime_start, balance_start_token_1_float, balance_current_token_1_float, balance_locked_token_1,
                             balance_start_token_2_float, balance_current_token_2_float, balance_locked_token_2, price_start_token_2, price_current_token_2, rsi_current, msg_status ):
    # Расчет индикаторов, по которым устанавливается цвет вывода RSI_CURRENT
    rsi_zero = 50
    rsi_up_1_3 = rsi_zero + (input_var.RSI_MAX - rsi_zero) / 3
    rsi_up_2_3 = rsi_zero + 2 * (input_var.RSI_MAX - rsi_zero) / 3
    rsi_down_1_3 = rsi_zero - (rsi_zero - input_var.RSI_MIN) / 3
    rsi_down_2_3 = rsi_zero - 2 * (rsi_zero - input_var.RSI_MIN) / 3
    # Расчет прибыли/убытка баланса с момента запуска программы
    balance_diff_token_1 = balance_current_token_1_float - balance_start_token_1_float + balance_locked_token_1
    balance_diff_token_2 = balance_current_token_2_float - balance_start_token_2_float + balance_locked_token_2

    # Устанавливаем цвет вывода значения RSI_CURRENT в зависимости от значения.
    if(rsi_current > input_var.RSI_MAX):
        rsi_current_color = input_var.color_red
    elif(rsi_current < input_var.RSI_MIN):
        rsi_current_color = input_var.color_red
    elif(rsi_current > rsi_up_1_3 and rsi_current < rsi_up_2_3):
        rsi_current_color = input_var.color_yellow
    elif(rsi_current < rsi_down_1_3 and rsi_current > rsi_down_2_3):
        rsi_current_color = input_var.color_yellow
    elif(rsi_current > input_var.RSI_MIN and rsi_current < rsi_down_2_3):
        rsi_current_color = input_var.color_yellow_bold
    elif(rsi_current < input_var.RSI_MAX and rsi_current > rsi_up_1_3):
        rsi_current_color = input_var.color_yellow_bold
    else:
        rsi_current_color = input_var.color_wite


    # ВЫВОД ТЕКУЩЕЙ ИНФОРМАЦИИ ПО РАБОТЕ ПРОГРАММЫ
    print('Дата и время начала работы: ',datetime_start)
    print('Текущие время и дата      : ', datetime.now().strftime('%Y.%m.%d  %H:%M:%S'))

    print(Fore.GREEN + \
          '============ ИНФОРМАЦИЯ О БАЛАНСЕ==========\n', \
          'Торговая пара                 :', input_var.color_blue.format(input_var.SYMBOL), '\n', \
          '-----------------', input_var.TOKEN_1, '--------------------\n', \
          'Стартовый баланс              :', Fore.LIGHTYELLOW_EX + str(balance_start_token_1_float), '\n', \
          'Текущий баланс                :', Fore.LIGHTGREEN_EX + str(balance_current_token_1_float), '\n', \
          'Заблокировано                 :', Fore.LIGHTRED_EX + str(balance_locked_token_1), '\n', \
          'РЕЗУЛЬТАТ:                    :', Fore.LIGHTWHITE_EX + str(balance_diff_token_1), '\n', \
          '-----------------', input_var.TOKEN_2, '--------------------\n', \
          'Стартовый баланс              :', Fore.LIGHTYELLOW_EX + str(balance_start_token_2_float), '\n', \
          'Текущий баланс                :', Fore.LIGHTGREEN_EX + str(balance_current_token_2_float), '\n', \
          'Заблокировано                 :', Fore.LIGHTRED_EX + str(balance_locked_token_2), '\n'\
          ' РЕЗУЛЬТАТ:                    :', Fore.LIGHTWHITE_EX + str(balance_diff_token_2))

    print(Fore.GREEN + \
          '================ ИНДИКАТОРЫ ================\n', \
          'TimeLine раб.области          :', input_var.color_blue.format(input_var.INTERVAL), '\n',\
          'RSI Limit                     :', input_var.color_blue.format(input_var.RSI_LIMIT), '\n',\
          'RSI Period                    :', input_var.color_blue.format(input_var.RSI_PERIOD), '\n',\

          'RSI max                       :', input_var.color_blue.format(input_var.RSI_MAX))
    print(' RSI Текущий                   :', rsi_current_color.format(str(round(rsi_current, input_var.RSI_CURRENT_ROUND))), '\n',\
          'RSI min                       :', input_var.color_blue.format(input_var.RSI_MIN))

    print(Fore.GREEN + \
          '=========== ИНФОРМАЦИЯ ПО ОРДЕРУ ===========\n', \
          'СТАТУС ОРДЕРА                 :', msg_status, '\n', \
          'Покупаем/Продаем              :', input_var.color_blue.format(input_var.QNTY), input_var.color_blue.format(input_var.TOKEN_2), '\n', \
          'Минимальный навар             :', input_var.color_blue.format(input_var.PRICE_DIFF), input_var.color_blue.format('%\n'), \
          'Цена 1', input_var.TOKEN_2, 'на момент старта   :', price_start_token_2, input_var.TOKEN_1, '\n', \
          'Текущая цена 1', input_var.TOKEN_2, '           :', price_current_token_2, input_var.TOKEN_1, '\n', \
          'Текущая стоимость ордера      :', round(price_current_token_2 * input_var.QNTY, input_var.PRICE_ORDER_ROUND), input_var.TOKEN_1)

'''         
          
          , Fore.GREEN +\
          '============ НАСТРОЙКИ ИНДИКАТОРОВ=========\n', \
          'TimeLine раб.облачти    :', interval, '\n', \
          'RSI Limit               :', rsi_limit, '\n', \
          'RSI Period              :', rsi_period, '\n', \
          'RSI Min                 :', rsi_min, '\n',\
          'RSI Max                 :', rsi_max, '\n',\
          'Quantity                :', qnty, '\n',Fore.GREEN +\
          '===========================================','\n',Fore.LIGHTWHITE_EX +\
          'ДЛЯ НАЧАЛА ТОРГОВЫХ ОПЕРАЦИЯ НАЖМИТЕ <ENTER> ....')


           'Interval=', interval, ' Limit=', rsi_limit, ' RSI_MIN=', rsi_min, 'RSI_MAX=', rsi_max, ' RSI_PERIOD=', rsi_period, 'QNTY=', qnty, ' PRICE_DIFF(%)=', price_diff,\
           '\n','=============================================================================================', '\n',\
           'BOT Start at         : ', datetime_start, '\n',\
           'Now                  : ', date_time, '\n', \
           'Balanse T1 Start     : ', balance_start_token_1, '\n', \
           'Balanse T1 Curr      : ', balance_current_token_1, '\n', \
           'Баланс T1. Разница   : ', balance_diff_token1, '\n', \
           'Balance T2 Start     : ', balance_start_token_2, '\n', \
           'Balance T2 Curr      : ', balance_current_token_2, '\n', \
           'Баланс T2. Разница   : ', balance_diff_token2, '\n', \
           'Token                : ', symbol, '\n', \
           'Price start          : ', price_start, '\n', \
           'Price buy            : ', price_buy, '\n', \
           'Price sell min       : ', price_sell_min, '\n', \
           'Price                : ', price_current, '\n', \
           'Price diff(%)        : ', price_diff_current, '\n', \

           'STATUS               : ', current_order, '\n', \
           'buy: ', buy, 'sell: ', sell)
    '''
