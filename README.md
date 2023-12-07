# Habr parser

## Описание
Парсер собирает статьи из указанных хабов и сохраняет в базу данных информацию об авторе и статье.

- Можно указать частоту обхода для каждого хаба
- Использование `aiohttp` для параллельного обхода страниц
- Использование асинхронных возможностей `SQLAlchemy` для работы с базой данных
- `docker-compose` для быстрого развертывания
- `Django Admin` для просмотра и редактирования данных


## Запуск проекта

### Запуск с `docker-compose`
```bash
docker-compose up -d --build
docker-compose logs -f parser
```
При использовании docker-compose дополнительных действий не требуется.

### Запуск без `docker-compose`
- Cоздать базу данных
- Bзменить параметры базы данных в `.env`
>Cоздать и запустить виртуальное окружение
>```bash
>python3 -m venv venv
>venv\Scripts\activate
>```

>Установить зависимости
>```bash
>pip install -r requirements.txt
>```

>Стандартные миграции `Django`
>```bash
>python3 django_admin/manage.py migrate
>```

>Создать суперпользователя `Django`
>```bash
>python3 django_admin/manage.py createsuperuser --noinput 
>```

>Запустить парсер
>```bash
> python3 src/main.py
>```

>Запустить `Django Admin`
>```bash
>  python3 django_admin/manage.py runserver
>  ```
  

## Использование
После запуска база данных наполнится тестовыми данными о хабах. 

Данные о собранных статьях будут выводиться в консоль.

>После выполненных действий `Django Admin` будет доступен по адресу http://localhost:8000/admin/.
> 
>Стандартные пользователь и пароль для `Django Admin`:
> * admin
> * 1234

