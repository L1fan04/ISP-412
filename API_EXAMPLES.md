# 📚 Примеры использования API

## 🌐 Веб-интерфейс (рекомендуется)

Откройте http://localhost:8000 в браузере для удобного интерфейса с формами.

## 🔧 Программное использование

### Python (requests)

```python
import requests

BASE_URL = "http://localhost:8000"

# Создать запись
response = requests.post(f"{BASE_URL}/items", json={
    "title": "Новая задача",
    "description": "Описание задачи"
})
print(response.json())

# Получить все записи
response = requests.get(f"{BASE_URL}/items")
print(response.json())

# Получить запись по ID
response = requests.get(f"{BASE_URL}/items/1")
print(response.json())

# Обновить запись
response = requests.put(f"{BASE_URL}/items/1", json={
    "title": "Обновленная задача",
    "description": "Новое описание"
})
print(response.json())

# Удалить запись
response = requests.delete(f"{BASE_URL}/items/1")
print(response.status_code)  # 204 - успешно удалено
```

### JavaScript (fetch)

```javascript
const BASE_URL = "http://localhost:8000";

// Создать запись
async function createItem(title, description) {
    const response = await fetch(`${BASE_URL}/items`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description })
    });
    return response.json();
}

// Получить все записи
async function getItems() {
    const response = await fetch(`${BASE_URL}/items`);
    return response.json();
}

// Обновить запись
async function updateItem(id, title, description) {
    const response = await fetch(`${BASE_URL}/items/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description })
    });
    return response.json();
}

// Удалить запись
async function deleteItem(id) {
    const response = await fetch(`${BASE_URL}/items/${id}`, {
        method: 'DELETE'
    });
    return response.status === 204;
}
```

### cURL команды

```bash
# Создать запись
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"title":"Новая запись","description":"Описание"}'

# Получить все записи
curl http://localhost:8000/items

# Получить запись по ID
curl http://localhost:8000/items/1

# Обновить запись
curl -X PUT http://localhost:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Обновленная запись","description":"Новое описание"}'

# Удалить запись
curl -X DELETE http://localhost:8000/items/1
```

## 📋 Структура данных

### Запрос (POST/PUT)
```json
{
  "title": "string",
  "description": "string"
}
```

### Ответ (GET)
```json
{
  "id": 1,
  "title": "string",
  "description": "string"
}
```

## 🔗 Полезные ссылки

- **Веб-интерфейс**: http://localhost:8000
- **API документация**: http://localhost:8000/docs
- **ReDoc документация**: http://localhost:8000/redoc
