import time
from pythonnet import load

# Укажите 'coreclr' для .NET Core / .NET 5+

load("coreclr")
import clr

clr.AddReference("System")
from System import *
import os

# Путь к вашей DLL
dll_path = r"C:\Users\stanislav.ivanov\Desktop\city_graph_analyze\Algos\Algos\bin\Debug\net9.0\Algos.dll"
assembly = clr.AddReference(dll_path)

# Получаем тип и метод
fib_type = assembly.GetType("Algos.AlgorithmFibonacci")
method = fib_type.GetMethod("Fibonacci")


def fib_fast(n):
    # Явно упаковываем число в .NET Int32
    dot_net_int = Int64(n)

    # В Invoke параметры передаются как массив объектов (Object[])
    # Создаем список параметров
    params = [dot_net_int]

    # Вызываем метод
    return method.Invoke(None, params)

def fib_python(n):
    if n <= 1:
        return n

    a = 0
    b = 1
    for i in range(2, n + 1, 1):
        temp = (a + b) % 100000000
        a = b
        b = temp
    return b

# Проверяем
try:
    a = 10000000
    s = time.time()
    fib_fast(a)
    print(time.time() - s)
    s = time.time()
    fib_python(a)
    print(time.time() - s)

    obj = Activator.CreateInstance(fib_type)

    # 2. Работа с полем (Dictionary aboba)
    # Получаем информацию о поле
    field_info = fib_type.GetField("aboba")
    # Получаем само значение словаря из объекта
    aboba_dict = field_info.GetValue(obj)
    print(aboba_dict)
    print(dict(aboba_dict))

    # 3. Вызов динамического метода Set
    set_method = fib_type.GetMethod("Set")
    set_method.Invoke(obj, ["myKey", "myValue"])
    print(dict(aboba_dict))

    # 4. Вызов динамического метода Get
    get_method = fib_type.GetMethod("Get")
    print(get_method.Invoke(obj, ["myKey"]))
except Exception as e:
    print(f"Ошибка: {e}")