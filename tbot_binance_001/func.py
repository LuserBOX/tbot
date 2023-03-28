import  requests

def fn_print_header (simbol, balance_start_token1, balance_start_token2, price, interval, limit, rsi_min, rsi_max, rsi_period, qnty):
    print('Trading BOT: binance-rsi-001 STARTING....\n\n', 'BOT parameters:\n', '---------------------\n', \
          'Token         :', simbol, '\n', \
          'Balance T1    :', balance_start_token1, '\n', \
          'Balance T2    :', balance_start_token2, '\n', \
          'Current price :', price, '\n', 'Interval      :', interval, '\n', 'RSI Limit     :', limit, '\n', \
          'RSI Period    :', rsi_period, '\n', \
          'RSI Min       :', rsi_min, '\n',
          'RSI Max       :', rsi_max, '\n',
          'Quantity      :', qnty, '\n')

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

def fn_create_logfile (logfile_name, datetime_now, botname, symbol, token_1, balance_start_token1, token_2, balance_start_token2 ,interval, limit, rsi_min, rsi_max, rsi_period, qnty ):
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
def fn_get_price(symbol, url)
    key = url.format(symbol)
    data = requests.get(key)
    data = data.json()
    price = float((f"{data['price']}"))
    return price