<a name="Начало"></a>

## BookInn

API сервис для бронирования номеров

[![BookInn workflow](https://github.com/dmsnback/bookinn/actions/workflows/main.yml/badge.svg)](https://github.com/dmsnback/bookinn/actions/workflows/main.yml)


- [Описание](#Описание)
- [Технологии](#Технологии)
- [Основные ресурсы](#Ресурсы)
- [Шаблон заполнения .env-файла](#Шаблон)
- [Запуск проекта на локальной машине](#Запуск)
- [Автор](#Автор)

<a name="Описание"></a>

### Описание

Сервис — REST API для бронирования номеров в отеле.  
Реализован на Django + Django REST Framework, используется Djoser для аутентификации (JWT), drf-spectacular для документации.

```python
Проект адаптирован для использования PostgreSQL и развёртывания в контейнерах Docker.
```

> [Вернуться в начало](#Начало)
<a name="Технологии"></a>

### Технологии

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
[![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org/ru/)
[![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)](https://gunicorn.org)

> [Вернуться в начало](#Начало)

<a name="Ресурсы"></a>

### Основные ресурсы

- `/api/v1/rooms/` — CRUD и список номеров
- `/api/v1/room_type/` — типы номеров
- `/api/v1/bookings/` — бронирования (создание/обновление/просмотр)
- `/api/v1/room_images/` — загрузка фото номера
- `/api/v1/auth/` — djoser (регистрация, логин, токены)

> [Вернуться в начало](#Начало)

<a name="Шаблон"></a>

### Шаблон заполнения .env-файла, расположен по пути infra/.env

> в settings.py указаны дефолтные значения для переменных из env-файла

```python
SECRET_KEY = 'Ваш секретный ключ'

DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 
```

> [Вернуться в начало](#Начало)

<a name="Запуск"></a>

### Запуск проекта на локальной машине

- Склонируйте репозиторий

```python
git clone git@github.com:dmsnback/bookinn.git
```

- Переходим в папку с файлом ```docker-compose.yaml```

```python
cd infra
```

- Запускаем Docker контейнеры

```python
docker-compose up -d --build
```

- Выполняем миграции

```python
docker-compose exec backend python manage.py migrate 
```

- Создаём суперюзера

```python
docker-compose exec backend python manage.py createsuperuser
```

- Собираем статику

```python
docker-compose exec backend python manage.py collectstatic --no-input
```

- Наполняем базу данных содержимым из файла ```rooms_fixture.json```:

> В базу добавится 10 номеров.

```python
docker-compose exec backend python manage.py loaddata data/rooms_fixture.json
```

> __Проект станет доступен по адресу:__

[http://localhost/api/v1/](http://localhost/api/v1/)

> __Админка станет доступна по адресу:__

[http://localhost/admin/](http://localhost/admin/)

> __Документация к API будет доступна по адресу:__

[http://localhost/api/docs/](http://localhost/api/docs/)

> [Вернуться в начало](#Начало)

<a name="Авторы"></a>

### Автор

- [Титенков Дмитрий](https://github.com/dmsnback)

> [Вернуться в начало](#Начало)
