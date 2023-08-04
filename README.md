# Readme файл для Django веб-приложения

## Описание проекта

Это Django веб-приложение, разработанное для отображения списка пользователей и их постов. Основная цель этого приложения - предоставить простой способ управления пользователями и их постами через веб-интерфейс.


## Установка

### Через Docker

1. Убедитесь, что у вас установлен Docker.
2. Склонируйте репозиторий с кодом проекта:

```bash
git clone https://github.com/Shadowmoses1314/Test_BBOOM.git
cd Test_BBOOM
```

3. В файле `django_project/settings.py`, установите параметры подключения к базе данных для PostgreSQL:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",  # set in docker-compose.yml
        "PORT": 5432,  # default postgres port
    }
}
```

4. В файле `django_project/settings.py`, установите параметры для Django Debug Toolbar (опционально):

```python
# django-debug-toolbar
import socket
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + "1" for ip in ips]
```

5. Запустите приложение с помощью Docker Compose:

```bash
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

Приложение будет доступно по адресу http://127.0.0.1:8000.

### Локальный запуск

1. Склонируйте репозиторий с кодом проекта:

```bash
git clone https://github.com/your_username/django_project.git
cd Test_BBOOM
```

2. В файле `django_project/settings.py`, установите параметры подключения к базе данных для SQLite другую базу нужно закоментировать:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

3. В файле `django_project/settings.py`, установите параметры для Django Debug Toolbar (опционально):

```python
INTERNAL_IPS = ["127.0.0.1"]
```

4. Создайте и активируйте виртуальное окружение:

```bash
python -m venv env
source env/Scripts/activate
```

5. Установите зависимости:

```bash
pip install -r requirements.txt
```

6. Примените миграции:

```bash
python manage.py migrate
```

7. Создайте суперпользователя:

```bash
python manage.py createsuperuser
```

8. Запустите сервер:

```bash
python manage.py runserver
```

Приложение будет доступно по адресу http://127.0.0.1:8000.

## Использование

После успешной установки и запуска приложения, вы сможете:
- Зарегистрироваться и войти как обычный пользователь
- Просматривать список всех пользователей на главной странице
- Перейти на страницу пользователя и увидеть список его постов
- Добавлять новые посты (только для аутентифицированных пользователей)
- Удалять свои посты (только для аутентифицированных пользователей)

## Тестирование
В процессе
