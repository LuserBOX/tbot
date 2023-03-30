
from colorama import init, Fore
from colorama import Back
from colorama import Style
init(autoreset=True)
import input_var
import requests
from colorama import init, Fore
from colorama import Back
from colorama import Style
init(autoreset=True)
b = input_var.QNTY

def fn_create_logfile (logfile_name, datetime_now, botname, symbol, interval, rsi_limit, rsi_min, rsi_max, rsi_period, qnty):

    file = open(logfile_name,"w")
    file.write(datetime_now.strftime("%m.%d.%Y, %H:%M:%S"))
    file.write(' <START> ' + botname +' ; ' + symbol + ' ; QNTY=' + str(qnty) +' ; INTERVAL=' + str(interval) +' ; RSI_LIMIT=' + str(rsi_limit))
    file.write(' ; RSI_MIN='+str(rsi_min)+' ; '+'RSI_MAX='+str(rsi_max)+' ; '+'RSI_PERIOD='+str(rsi_period) )
    file.write('\n')
    file.close()

def fn_write_logfile_status (logfile_name, datetime_now, botname, symbol, token_1, balance_start_token1, token_2, balance_start_token2, interval, rsi_limit, rsi_min, rsi_max, rsi_period, qnty):

    balance_start_token_1_float = float(balance_start_token1['free'])
    balance_start_token_2_float = float(balance_start_token2['free'])
    file = open(logfile_name,"w")
    file.write(datetime_now.strftime("%m.%d.%Y, %H:%M:%S"))
    file.write(' <START> '+botname+' ; '+symbol+' ; '+token_1+'='+str(balance_start_token_1_float)+' ; '+token_2+'=')
    file.write(str(balance_start_token_2_float) + ' ; QNTY=' + str(qnty) +' ; INTERVAL=' + str(interval) +' ; RSI_LIMIT=' + str(rsi_limit) + ' ; RSI_MIN=')
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




def fn_telegram_send_msg(telegram_token, chat_id,text):
    url_req = "https://api.telegram.org/bot" + telegram_token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
    results = requests.get(url_req)
    print(results.json())

def fn_pause():
    programPause = input("Press the <ENTER> key to continue...")

# Функция возвращает текущую цену токена в индексной паре 'symbol'. Например symbol=BNBUSDT









