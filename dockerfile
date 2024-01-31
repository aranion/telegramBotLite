# Указываем Docker использовать образ Python в качестве базового
FROM python:3.7.3
# Устанавливаем необходимые переменные окружения
ENV PYTHONUNBUFFERED 1
# Устанавливаем рабочий каталог контейнера
RUN mkdir /app
WORKDIR /app
# Установка зависимостей
RUN pip install --upgrade pip
COPY ./requirements.txt ./
EXPOSE 5000
RUN pip install -r requirements.txt
# Копируем все файлы из локального проекта в контейнер
COPY ./ /app/
# Копируем файл main.py из src в корень
COPY ./src/main.py /app/