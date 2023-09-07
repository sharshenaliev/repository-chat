# Использование

Здесь приведены основные инструкции по использованию приложения `repository-chat`.

## Настройка переменных окружения

Для корректной работы приложения вам нужно настроить следующие переменные окружения в файле `.env`:

Заполните соответствующими значениями, которые вы хотите использовать для каждой переменной.

```shell
POSTGRES_DB=test
POSTGRES_USER=test
POSTGRES_PASSWORD=test
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
SECRET_KEY=testkey
```

## Запуск приложения

1. Запустите Docker Compose:

    ```
    docker-compose up -d --build
    ```
2. Выполните миграции:

    ```
    docker-compose exec web alembic upgrade head
    ```

   Это запустит все необходимые сервисы, указанные в вашем `docker-compose.yml`, включая ваше Django приложение, базу
   данных Postgres.

## Работа с приложением

1. Для входа в приложение откройте браузер и перейдите по адресу `http://localhost:8000/docs`.

2. Здесь вы найдете свагер приложения и сможете начать работу.


## Запуск unit тестов

1. Запустить команду:

    ```
    docker compose exec web pytest -v -s tests/
    ```
