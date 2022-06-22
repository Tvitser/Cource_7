#       TodoList

С помощью этого приложения вы сможете сохранять напоминания о своих делах.

##    Как установить

1. Установить зависимости с помощью команды
pip install -r requirements.txt
2. Установить Базу Данных с помощью docker: docker run --name postgresql -e POSTGRES_PASSWORD=postgres -d postgres
3. Накатить миграции с помощью команды py manage.py migrate
4. Запустить приложение: py manage.py runserver 8000