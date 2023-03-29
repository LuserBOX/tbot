
import  requests
import input_var
import config_var
from colorama import init, Fore
from colorama import Back
from colorama import Style
init(autoreset=True)


def fn_print_header (simbol, token_1, token_2, balance_start_token1, balance_start_locked_token1, balance_start_token2, balance_start_locked_token2,price_token2_current, interval, limit, rsi_min, rsi_max, rsi_period, qnty):
    print('Trading BOT: binance-rsi-001 STARTING....\n\n', Fore.RED +'  ПЕРЕД ЗАПУСКОМ ПЕРЕПРОВЕРЬТЕ ПАРАМЕТРЫ:')
    print(Fore.GREEN + \
          '============ ИНФОРМАЦИЯ О БАЛАНСЕ==========\n', \
          'Торговая пара           :', simbol, '\n', \
          'Баланс       ', token_1, '      :', Fore.LIGHTYELLOW_EX + str(balance_start_token1), '\n', \
          'Заблокировано', token_1, '      :', Fore.MAGENTA + str(balance_start_locked_token1), '\n', \
          'Баланс       ', token_2, '      :', Fore.LIGHTYELLOW_EX + str(balance_start_token2), '\n', \
          'Заблокировано', token_2, '      :', Fore.MAGENTA + str(balance_start_locked_token2), '\n', Fore.GREEN +\
          '============ НАСТРОЙКИ ОРДЕРА =============\n', \
          'Ордер на покупку        :', qnty, token_2, '\n', \
          'Текущая цена 1', token_2, '     :', price_token2_current, token_1, '\n', \
          'Текущая стоиомть ордера :', round(price_token2_current * qnty, 2), token_1, '\n', Fore.GREEN +\
          '============ НАСТРОЙКИ ИНДИКАТОРОВ=========\n', \
          'TimeLine раб.облачти    :', interval, '\n', \
          'RSI Limit               :', limit, '\n', \
          'RSI Period              :', rsi_period, '\n', \
          'RSI Min                 :', rsi_min, '\n',\
          'RSI Max                 :', rsi_max, '\n',\
          'Quantity                :', qnty, '\n',Fore.GREEN +\
          '===========================================','\n',Fore.LIGHTWHITE_EX +\
          'ДЛЯ НАЧАЛА ТОРГОВЫХ ОПЕРАЦИЯ НАЖМИТЕ <ENTER> ....')

def fn_print_current_status (bot_status, interval, limit, rsi_min, rsi_max, rsi_period, qnty, price_diff, datetime_start, date_time, \
                          balance_start_token_1, balance_start_token_2, balance_current_token_1, balance_current_token_2, symbol, price_start, price_buy, \
                          price_sell_min, price_current,price_diff_current ,current_order, current_rsi, buy, sell):

    balance_start_token_1_float = float(balance_start_token_1['free'])
    balance_current_token_1_float = float(balance_current_token_1['free'])
    balance_start_token_2_float = float(balance_start_token_2['free'])
    balance_current_token_2_float = float(balance_current_token_2['free'])
    balance_diff_token1 = balance_current_token_1_float - balance_start_token_1_float
    balance_diff_token2 = balance_current_token_2_float - balance_start_token_2_float

    print (bot_status, '\n', \
           'Interval=', interval, ' Limit=', limit, ' RSI_MIN=', rsi_min, 'RSI_MAX=', rsi_max, ' RSI_PERIOD=', rsi_period,'QNTY=', qnty ,' PRICE_DIFF(%)=', price_diff,\
           '\n','=============================================================================================', '\n',\
           'BOT Start at         : ',datetime_start , '\n' ,\
           'Now                  : ',date_time, '\n', \
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
           'Price                : ', price_current,'\n', \
           'Price diff(%)        : ', price_diff_current, '\n', \
           'RSI (Текущий)        : ', current_rsi, '\n', \
           'STATUS               : ', current_order, '\n', \
           'buy: ', buy, 'sell: ', sell)

def fn_create_logfile (logfile_name, datetime_now, botname, symbol, interval, limit, rsi_min, rsi_max, rsi_period, qnty ):
    file = open(logfile_name,"w")
    file.write(datetime_now.strftime("%m.%d.%Y, %H:%M:%S"))
    file.write(' <START> '+botname+' ; '+symbol+ ' ; QNTY='+str(qnty)+' ; INTERVAL='+str(interval)+' ; LIMIT='+str(limit))
    file.write(' ; RSI_MIN='+str(rsi_min)+' ; '+'RSI_MAX='+str(rsi_max)+' ; '+'RSI_PERIOD='+str(rsi_period) )
    file.write('\n')
    file.close()

def fn_write_logfile_status (logfile_name, datetime_now, botname, symbol, token_1, balance_start_token1, token_2, balance_start_token2 ,interval, limit, rsi_min, rsi_max, rsi_period, qnty ):
    balance_start_token_1_float = float(balance_start_token1['free'])
    balance_start_token_2_float = float(balance_start_token2['free'])
    file = open(logfile_name,"w")
    file.write(datetime_now.strftime("%m.%d.%Y, %H:%M:%S"))
    file.write(' <START> '+botname+' ; '+symbol+' ; '+token_1+'='+str(balance_start_token_1_float)+' ; '+token_2+'=')
    file.write(str(balance_start_token_2_float) + ' ; QNTY='+str(qnty)+' ; INTERVAL='+str(interval)+' ; LIMIT='+str(limit)+' ; RSI_MIN=')
    file.write(str(rsi_min)+' ; '+'RSI_MAX='+str(rsi_max)+' ; '+'RSI_PERIOD='+str(rsi_period)+' ; ' )
    file.write('\n')
    file.close()

def fn_write_logfile_order_buy (logfile_name, datetime_now, botname, rsi, symbol, qnty, price):
    file = open(logfile_name,"a")
    file.write(datetime_now.strftime("%m.%d.%Y, %H:%M:%S"))
    file.write(' <BUY ORDER ADD> ')
    file.write(str(botname))
    file.write(' RSI=')
    file.write(str(rsi))
    file.write(' TOKEN=')
    file.write(str(symbol))
    file.write(' QNTY=')
    file.write(str(qnty))
    file.write(' PRICE=')
    file.write(str(price))
    file.write('\n')
    file.close()

def fn_write_logfile_order_sell (logfile_name, datetime_now, botname, rsi, symbol, qnty, price):
    file = open(logfile_name,"a")
    file.write(datetime_now.strftime("%m.%d.%Y, %H:%M:%S"))
    file.write(' <SELL ORDER ADD> ')
    file.write(str(botname))
    file.write(' RSI=')
    file.write(str(rsi))
    file.write(' TOKEN=')
    file.write(str(symbol))
    file.write(' QNTY=')
    file.write(str(qnty))
    file.write(' PRICE=')
    file.write(str(price))
    file.write('\n')
    file.close()

# Функция записи сообщения в LOG файл
def fn_write_logfile_msg (logfile_name, datetime_now, msg):
    file = open(logfile_name, "a")
    file.write(datetime_now.strftime("%m.%d.%Y, %H:%M:%S"))
    file.write(msg)
    file.write('\n')
    file.close()


def fn_top_coin(pd, client):
        all_tickers = pd.DataFrame(client.get_ticker())
        usdt = all_tickers[all_tickers.symbol.str.contains('USDT')]
        work = usdt[~((usdt.symbol.str.contains('UP')) | (usdt.symbol.str.contains('DOWN')))]
        top_coin = work[work.priceChangePercent == work.priceChangePercent.max()]
        top_coin = top_coin.symbol.values[0]
        return top_coin

def fn_telegram_send_msg(telegram_token, chat_id,text):
    url_req = "https://api.telegram.org/bot" + telegram_token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
    results = requests.get(url_req)
    print(results.json())

def fn_pause():
    programPause = input("Press the <ENTER> key to continue...")

# Функция возвращает текущую цену токена в индексной паре 'symbol'. Например symbol=BNBUSDT
def fn_get_price(symbol, url):
    key = url.format(symbol)
    data = requests.get(key)
    data = data.json()
    price = float((f"{data['price']}"))
    return price

# Функция возвращает свободный баланс и заблокированный баланс (в открытых ордерах) токена
def fn_get_balance(client, token):
    balance = client.get_asset_balance(asset=token)
    balance_free = float((f"{balance['free']}"))
    balance_locked = float((f"{balance['locked']}"))
    return balance_free, balance_locked
# Функция возвращает кол-во заблокированных (находящиеся в открытых ордерах) токенов.
def fn_get_balance_locked(client, token):
    balance_locked = client.get_asset_balance(asset=token)
    balance_locked = float((f"{balance_locked['locked']}"))
    return balance_locked

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


