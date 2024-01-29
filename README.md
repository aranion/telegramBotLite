# telegramBot

Telegram Bot "Вокс"

Информационная интеллектуальная система психологической поддержки студентов

@voks_sk_bot

python v. 3.7.3

1) Установить venv:
    - Если python 3.7.3 основной

   ```shell
   python.exe -m venv venv
   ```

    - Если python 3.7.3 в другом месте

   ```shell
   C:\project\python373\python.exe -m venv venv
   ```

    - Если требуется обновить pip

   ```shell
   python -m pip install --upgrade pip
   ```

2) Включаем venv

```shell
cd .\venv\Scripts & .\activate & cd ../../
```

3) Установка пакетов

```shell
pip install -r requirements.txt
```

4) Для настройки чат бота и Firebase необходимо добавить файл "config.py" в "\src" и заполнить согласно "
   \src\config_template.py"
5) Запуск `python .\src\main.py` | `python -m src.main.py`
