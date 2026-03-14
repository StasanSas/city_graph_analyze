from my_code.code.utilite import get_slow_query


#({"name":".+?})|(\[[\d, .]+])
s = get_slow_query('https://kudikina.ru/kostr/bus/21k/A', 1)
scripts_without_attrs = [str(script) for script in s.find_all('script') if len(script.attrs) == 1]
a = filter(lambda c: 'drawMap(' in c, scripts_without_attrs)
print(list(a)[0])