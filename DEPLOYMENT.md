# 🚀 Развертывание проекта

## 📦 Локальное развертывание

### Требования
- Python 3.7+
- pip

### Установка
```bash
# Клонировать репозиторий
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY

# Установить зависимости
pip install -r requirements.txt

# Запустить сервер
python -m uvicorn app.main:app --reload
```

## ☁️ Облачное развертывание

### Heroku

1. **Создайте Procfile:**
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

2. **Установите Heroku CLI** и выполните:
```bash
heroku create your-app-name
git push heroku main
heroku open
```

### Railway

1. Подключите GitHub репозиторий к Railway
2. Railway автоматически определит Python проект
3. Приложение будет доступно по сгенерированному URL

### PythonAnywhere

1. Загрузите файлы проекта
2. Установите зависимости через консоль
3. Настройте веб-приложение с WSGI файлом

## 🐳 Docker (опционально)

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Запуск с Docker
```bash
docker build -t crud-api .
docker run -p 8000:8000 crud-api
```

## 🔧 Переменные окружения

Создайте файл `.env` для настройки:
```env
DATABASE_URL=sqlite:///./app/app.db
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

## 📝 Примечания

- База данных SQLite создается автоматически при первом запуске
- Для продакшена рекомендуется использовать PostgreSQL
- Настройте CORS для доступа с внешних доменов
