Полезные ссылки на теорию и примеры работы функций
https://www.codecamp.ru/blog/pandas-column-to-list/
https://www.codecamp.ru/blog/pandas-check-if-column-contains-string/
https://khashtamov.com/ru/pandas-introduction/
https://pythonru.com/biblioteki/struktury-dannyh-v-pandas
https://skillbox.ru/media/code/metody-append-i-extend-v-python-dobavlyaem-elementy-v-spisok/




Программа получает от Бинанса перечень монет, торгующихся только спотом.
т.е. нет фьючерсной тоговли

https://www.youtube.com/watch?v=ETLKgFRXdCo

spot_info - многомерный список.

print(spot_info['symbols'][1]['symbol']) - выводит что:
- В верхнем списке 'spot_info' нам нужен подсписок с индексом 'symbols'
- В этом подсписке, мы заходим в подсписок с индексом '1' ("это второй, так как считаем от 0 ")
- В этом подсписке уже ищем значение с индексом 'symbol'
=> LTCBTC


Series.str.contains() используется для проверки наличия шаблона или регулярного выражения в строке серии или индекса.
Функция возвращает логический ряд или индекс в зависимости от того, содержится ли заданный шаблон или регулярное
выражение в строке ряда или индекса.

