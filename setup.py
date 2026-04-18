import os
import subprocess
import sys
from pathlib import Path

from pybind11.setup_helpers import build_ext
from setuptools import setup, Extension
import pybind11


class BuildExtWithOutput(build_ext):
    def run(self):
        # Создаём папку для выходных файлов
        output_dir = "./c_plus_plus_code"
        os.makedirs(output_dir, exist_ok=True)

        # Меняем путь вывода
        self.build_lib = output_dir
        super().run()


# Определение расширения
ext_modules = [
    Extension(
        "graph_solver", # Имя модуля, который будем импортировать
        ["C:\\Users\\stanislav.ivanov\\source\\repos\\TestSolushion\\TestSolushion\\TestSolushion.cpp"], # Имя вашего файла C++
        include_dirs=[
            pybind11.get_include(),
            # Добавляем путь к vcpkg, если pybind11 брался оттуда
        ],
        language='c++',
        extra_compile_args=['/std:c++20', '/utf-8'], # Важно для .contains()
    ),
]

setup(
    name="graph_solver",
    ext_modules=ext_modules,
    cmdclass={'build_ext': BuildExtWithOutput},
)

current_dir = Path(__file__).parent
stub_dir = current_dir / "c_plus_plus_code"
stub_dir.mkdir(exist_ok=True)

subprocess.check_call([
    sys.executable, "-m", "pybind11_stubgen",
    "graph_solver",
    "-o", str(stub_dir)
])

print("Очистка от дубликатов...")
for pyd_file in Path(".").glob("*.pyd"):
    if pyd_file.parent != stub_dir:  # Если файл не в целевой папке
        pyd_file.unlink()
# из родительской дирректории
#python setup.py build_ext --inplace
