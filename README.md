# Тестовое задание

Это бот-напоминалка для телеграм.
Умеет регистрировать пользователя, создавать заметки и напоминать за 10 минут до наступления времени, указанного в заметке.

## Запуск

- Нужно создать файл .env, заполненный по аналогии с .env.example
В нем нужно указать токен для бота, а так же, app_id и app_hash для приложения в телеграм.
- - [Как получить токен](https://core.telegram.org/bots/tutorial#obtain-your-bot-token)
- - [Как получить app_id и app_hash](https://docs.telethon.dev/en/stable/basic/signing-in.html#signing-in)
- - С последним пунктом могут быть сложности. [Решение](https://stackoverflow.com/a/68795328)
- Выполнить `docker compose up bot`


## Локальный запуск бота
- Версия Python: 3.10
- В проекте используется менеджер зависимостей [Poetry](https://python-poetry.org/docs/#installation)
- `poetry install`
- Нужно заполнить в .env файле переменные, касающиеся БД
- Скопировать содержимое файла docker-compose.override.example.yml в docker-compose.override.yml
- `docker compose up liquibase`
- После того, как контейнер liquibase отработает - можно запускать бота:
```shell
TOKEN=BOT_TOKEN \
API_ID=API_ID \
API_HASH=API_HASH\
PG_HOST=localhost \
PG_PORT=5432 \
PG_USER=user \
PG_PASSWORD=password \
PG_DATABASE=bot \
python main.py
```
