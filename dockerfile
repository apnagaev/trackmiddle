# установка базового образа (host OS)
FROM python:alpine

# установка рабочей директории в контейнере
WORKDIR /httpserver

# копирование файла зависимостей в рабочую директорию
COPY requirements.txt .

# установка зависимостей
RUN pip install -r requirements.txt

# копирование содержимого локальной директории src в рабочую директорию
COPY . .

# команда, выполняемая при запуске контейнера
CMD [ "python3", "/httpserver/server.py" ]
