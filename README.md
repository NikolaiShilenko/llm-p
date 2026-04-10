# llm-p

## FastAPI сервис с JWT аутентификацией, SQLite и интеграцией с LLM через OpenRouter

## Технологии

- FastAPI
- SQLAlchemy (async)
- SQLite (aiosqlite)
- JWT (python-jose)
- OpenRouter API (httpx)
- uv (управление зависимостями)

## Установка и запуск

### 1. Установить uv

```bash
pip install uv
```
### 2. Клонировать репозиторий
```bash
git clone https://github.com/NikolaiShilenko/llm-p.git
cd llm-p
```
### 3. Создать виртуальное окружение
```bash
uv venv
```
### 4. Активировать виртуальное окружение
#### Windows:

```bash
.venv\Scripts\activate
```
#### MacOS/Linux:

```bash
source .venv/bin/activate
```

### 5. Установить зависимости
```bash
uv pip compile pyproject.toml -o requirements.txt
uv pip install -r requirements.txt
```

### 6. Настроить переменные окружения
#### Создать .env, скопировать .env.example в .env и добавить ваш OpenRouter API Key:
#### OPENROUTER_API_KEY=sk-or-v1-ваш_ключ

### 7. Запустить сервер
```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 8. Открыть Swagger документацию
#### Перейти по адресу: http://localhost:8000/docs

### Проверка работоспособности
#### Регистрация пользователя
####  /auth/register с email формата student_фамилия@email.com

#### Логин
#### POST /auth/login — получить JWT токен

#### Авторизация в Swagger
#### Нажать кнопку Authorize, вставить Bearer <токен>

#### Запрос к LLM
#### POST /chat с полем prompt

#### История диалога
#### GET /chat/history — просмотр истории
#### DELETE /chat/history — очистка истории

### Проверка качества кода
```bash
ruff check
```

### Структура проекта

    llm-p/
    ├── app/
    │   ├── api/           # HTTP эндпоинты
    │   ├── core/          # Конфиг, security, ошибки
    │   ├── db/            # База данных (модели, сессия)
    │   ├── schemas/       # Pydantic схемы
    │   ├── repositories/  # Доступ к данным
    │   ├── services/      # Внешние сервисы (OpenRouter)
    │   └── usecases/      # Бизнес-логика
    ├── pyproject.toml
    ├── .env.example
    └── README.md

### Скриншоты
#### Регистрация


#### Логин и получение токена


#### Авторизация в Swagger


#### Запрос к LLM (POST /chat)


#### Получение истории (GET /chat/history)


#### Удаление истории (DELETE /chat/history)

