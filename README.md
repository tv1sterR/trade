1. Клонирование репозитория
https://github.com/tv1sterR/trade.git
cd barter
2. Создание виртуального окружения
python -m venv venv
source venv/bin/activate - Для macOS и Linux
venv\Scripts\activate - Для Windows
3. Установка зависимостей
pip install -r requirements.txt
4. Миграция БД
python manage.py makemigrations
python manage.py migrate
5. Запуск сервера
python manage.py runserver (перед этим cd barter)
Доступ к серверу по адресу: 127.0.0.1:8000
6. Запуск тестов
python manage.py test app

P.S. 
Создание суперпользователя - python manage.py createsuperuser
