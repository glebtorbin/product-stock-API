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
cd ..
docker-compose up --build
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

- Создание продукта:
- Поле size указывается в поле data, чтобы была возможность расширить кол-во параметов, при необходимости
- Один продукт может храниться на нескольких складах, на разных складах может быть разное кол-во одного и того же товара

POST http://127.0.0.1:8021/api/products/
```
[
  {
    "title": "string",
    "data": {
        size: "S"
    },
    "code": -9223372036854776000,
    "quantity": 0,
    "stocks": [
      1, 2 ...
    ]
  }
]
```
- Список существующих товаров

GET http://127.0.0.1:8021/api/products/
```
[
    {
        "id": 1,
        "title": "тест",
        "code": 32456654245,
        "date_create": "2023-04-07T06:38:22.925958Z",
        "stocks": [
            1,
            2,
            3,
            4
        ],
        "size": "78"
    }
]
```

- Проверка статуса склада

GET http://127.0.0.1:8021/api/stock_status/{stock_id}

ответ:
```
{
    "status": true
}
```

- Изменение статуса склада

POST http://127.0.0.1:8021/api/stock_status/{stock_id}

ответ:
```
{
    "stock4 availability status": false
}
```

- Баланс склада

GET http://127.0.0.1:8021/api/stock_balance/{stock_id}

ответ:
```
{
    "stock4": {
        "test": {
            "code": 32456654245,
            "quantity": 53
        },
        "t-shirt": {
            "code": 2344567678,
            "quantity": 125
        },
        "total": 178
    }
}
```

- Бронирование товара на складе
- При бронированиии кол-во товара на складах уменьшается

POST http://127.0.0.1:8021/api/reserve/{stock_id}

```
{
    "reserve": [
        123456, 32456654245, 234345
    ]
}
```

```
{
    "reserve": 2,
    "reserved_positions": [
        32456654245
    ],
    "not_available": [
        123456
    ],
    "unknown_items": [
        234345
    ]
}
```

- Отмена бронирования товара на складе
- Сделал отмену бронирования по ID, тк одна и та же бронь может иметь одинаковые позиции
- При отмене бронированиия кол-во товара на складах увеличивается

DELETE http://127.0.0.1:8021/api/deleteres/{reserve_id}

```
"OK"
```
