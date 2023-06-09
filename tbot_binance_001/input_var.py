# ================ НАСТРАИВАЕМЫЕ ПАРАМЕТРЫ. Указать необходимые =================
# УКАЗАТЬ Торговая пара
SYMBOL = 'BTCUSDT'
# Указать индексные названия торгуемых токены. Должны быть согласованы с параметром SYMBOL
# Этим токеном мы оплачиваем покупки
TOKEN_1 = 'USDT'
# Этот токен мы продаем и на его курсе пытаемся заработать.
TOKEN_2 = 'BTC'
# Параметр TimeFrame. Set this timeframe on Binance TradingView Window for correct inspectors bot work
INTERVAL = '1m'
# Параметр отвечает за расчет индекса RSI
RSI_LIMIT = '200'
# Параметр указывает, какое кол-во ТОКЕНА_2 мы покупаем, для дальнейшей продажи.
QNTY = 0.01
# Индикатор RSI. Среднее значение RSI=50. Можно сказать- это нулевая линия на графике.
# Минимальное пороговое значение индикатора RSI, при котором срабатает тригер на покупку. (По умолчанию = 30)
RSI_MIN = 20
# Максимальное  пороговое значение индикатора RSI, при котором срабатает тригер на продажу. (По умолчанию = 70)
RSI_MAX = 80
# Период расчета параметра RSI. По умолчанию = 14. Но для болееоперативного реагирования значения ставят от 8 - 11
RSI_PERIOD = 7
# Минимальная разница между ценой закупки и ценой продажи в %. Это второй индикатор, разрешающий продажу. Чтобы не продать дешевле, чем купили.
PRICE_DIFF = 0.5
#
# ====================================================
# ЭТО Служебный параметры. НЕ МЕНЯТЬ !!!
# ====================================================
BOTNAME = 'tbot_binance(v.001)'

# ======= ПАРАМЕТРЫ
# Комиссия (%) биржи c каждой сделки в BNB. Указана в качестве информации.В коде не используется.
EXCHANGE_COMISSION = 0.075
# До какого знака округлять стоимость ордера при выводе информации на экран
PRICE_ORDER_ROUND = 3
# До какого знака округлять значение RSI_CURRENT при выводе информации на экран
RSI_CURRENT_ROUND = 2

# ======= ФАЙЛОВАЯ СИСТЕМА =====
# Директория для LOG файлов
DIR_LOG = 'log/'
LOG_FILENAME = 'tbot_binance(v.001)'

# URL для подключения
# URL для запроса пула свечей для расчета RSI индекса
# Тестовая сеть BINANCE - ПОКАЗАНИЯ НЕ СОГЛАСУЮТСЯ С ГРАФИКОМ!!! ДЛЯ ТЕСТОВ ИСПОЛЬЗУЮ РАБОЧУЮ URL
#URL_BINANCE_GET_CANDLES_INTERVAL_LIMIT = 'https://testnet.binance.vision/api/v3/klines?symbol={}&interval={}&limit={}'
# Рабочая сеть BINANCE
URL_BINANCE_GET_CANDLES_INTERVAL_LIMIT = 'https://api.binance.com/api/v3/klines?symbol={}&interval={}&limit={}'
# URL for WINSOCS connect to BINANCE
# Тестовая сеть Binance
URL = 'https://testnet.binance.vision/api/v3/ticker/price?symbol={}'
# Рабочая сеть BINANCE
#URL = 'https://api.binance.com/api/v3/ticker/price?symbol={}'
# Уведомление, отправляемое в телеграмм бот при старте скрипта.
MSG_INFO_TELEGRAM_START_BOT ='INFO: '+ BOTNAME+' STATUS:  запущен'

# Сообщения
# Сообщение в Телеграм об успешном подключении к бирже
msg_telegram_success_exchange_connect = '<OK> Подключение к бирже прошло успешно'
# Сообщение в Телеграм об ошибке подключения к бирже
msg_telegram_error_exchange_connect = '<ERROR> Ошибка подключения к бирже. Завершение работы программы.'

# Установка переменных для печати разнвм цветов через ASCII
color_wite = "\033[1m\033[39m{}"
color_yellow = "\033[0m\033[33m{}"
color_yellow_bold = "\033[1m\033[33m{}"
color_red = "\033[1m\033[31m{}"
color_blue = "\033[1m\033[34m{}"