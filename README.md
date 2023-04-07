# product-stock-API


## Tecnhologies:
- Python 3.9
- Django 4.0
- Django REST framework 3.14
- Docker
- Postgres

```
git clone https://github.com/glebtorbin/product-stock-API.git
```
- Go to project directory
```
cd product-stock-API/
```
- Create env-file:
```
touch .env
```
- Fill in the env-file like it:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=stock_db
POSTGRES_USER=admin
POSTGRES_PASSWORD=qwerty
DB_HOST=db
DB_PORT=5432
POSTGRES_DB=stock_db
```
- Run tests
```
cd stock_app/
python manage.py tests
```
- Run docker-compose
```
sudo docker-compose up --build
```

# Описание методов

- Документация доступна после запуска проекта тут:
```
http://127.0.0.1:8021/redoc/
```

- Создание склада:

POST http://127.0.0.1:8021/api/stocks/
```
{
    "title": "string"
}
```

```
[
  {
    "id": 0,
    "title": "string",
    "avail_sign": true,
    "date_create": "2019-08-24T14:15:22Z"
  }
]
```

- Список складов:

GET http://127.0.0.1:8021/api/stocks/

```
[
  {
    "id": 0,
    "title": "string",
    "avail_sign": true,
    "date_create": "2019-08-24T14:15:22Z"
  }
]
```


