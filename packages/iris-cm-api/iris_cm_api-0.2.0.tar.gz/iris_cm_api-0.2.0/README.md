# Эмулятор сигналов Iris CM Callback API

![PyPI](https://img.shields.io/pypi/v/iris-cm-api)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/iris-cm-api)
![GitHub](https://img.shields.io/github/license/lordralinc/iris_cm_api_emulator)

# Установка 

## Windows
```shell
# Создаем папку, открываем в этой папке командную строку (shift + ПКМ)
py -m venv env
env\Scripts\activate.bat
pip install -U https://github.com/timoniq/vkbottle/archive/master.zip
pip install iris_cm_api
```

# Настройка
Создайте файл `config.ini` (скопируйте его из файла [config.ini.example](https://github.com/lordralinc/iris_cm_api_emulator/blob/master/config.ini.example)), укажите токен группы в поле `token`

# Запуск
```shell
# Открываем в созданной папке командную строку (shift + ПКМ)
env\Scripts\activate.bat
py -m iris_cm_api
```

# Обновление 
```shell
# Открываем в созданной папке командную строку (shift + ПКМ)
env\Scripts\activate.bat
pip install -U https://github.com/timoniq/vkbottle/archive/master.zip
pip install -U iris_cm_api
```

