#!/usr/bin/env python3
"""
Простое тестирование CRUD API
"""

import requests

BASE_URL = "http://localhost:8000"

def test_api():
    print("Тестирование API")
    print("-" * 30)
    
    # Создать запись
    print("1. Создание записи...")
    response = requests.post(f"{BASE_URL}/items", json={
        "title": "Тестовая запись",
        "description": "Описание"
    })
    print(f"Статус: {response.status_code}")
    item = response.json()
    print(f"Создана: {item}")
    item_id = item["id"]
    
    # Получить все записи
    print("\n2. Получение всех записей...")
    response = requests.get(f"{BASE_URL}/items")
    print(f"Статус: {response.status_code}")
    print(f"Записи: {response.json()}")
    
    # Получить запись по ID
    print(f"\n3. Получение записи {item_id}...")
    response = requests.get(f"{BASE_URL}/items/{item_id}")
    print(f"Статус: {response.status_code}")
    print(f"Запись: {response.json()}")
    
    # Обновить запись
    print(f"\n4. Обновление записи {item_id}...")
    response = requests.put(f"{BASE_URL}/items/{item_id}", json={
        "title": "Обновленная запись",
        "description": "Новое описание"
    })
    print(f"Статус: {response.status_code}")
    print(f"Обновлена: {response.json()}")
    
    # Удалить запись
    print(f"\n5. Удаление записи {item_id}...")
    response = requests.delete(f"{BASE_URL}/items/{item_id}")
    print(f"Статус: {response.status_code}")
    
    print("\nТестирование завершено!")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("Ошибка: Сервер не запущен. Запустите: python -m uvicorn app.main:app --reload")
    except Exception as e:
        print(f"Ошибка: {e}")
