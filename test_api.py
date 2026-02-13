#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Скрипт для тестирования API"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def print_response(title, response):
    """Печать форматированного ответа"""
    print(f"\n{'='*60}")
    print(f">> {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")
    print()


def test_auth():
    """Тестирование аутентификации"""
    print("\n" + "="*60)
    print("TEST: AUTHENTICATION AND AUTHORIZATION")
    print("="*60)
    
    # 1. Вход как администратор
    admin_session = requests.Session()
    response = admin_session.post(f"{BASE_URL}/auth/login", json={
        "email": "admin@example.com",
        "password": "admin123"
    })
    print_response("1. Вход как администратор", response)
    
    # 2. Проверка текущего пользователя
    response = admin_session.get(f"{BASE_URL}/auth/me")
    print_response("2. Получение информации о текущем пользователе", response)
    
    # 3. Попытка доступа к статьям (должна быть успешной)
    response = admin_session.get(f"{BASE_URL}/resources/articles")
    print_response("3. Получение статей (admin имеет доступ)", response)
    
    # 4. Создание статьи
    response = admin_session.post(f"{BASE_URL}/resources/articles", json={
        "title": "Тестовая статья от администратора",
        "content": "Содержимое тестовой статьи"
    })
    print_response("4. Создание статьи (admin имеет права)", response)
    
    # 5. Выход
    response = admin_session.post(f"{BASE_URL}/auth/logout")
    print_response("5. Выход администратора", response)


def test_user_permissions():
    """Тестирование прав пользователя"""
    print("\n" + "="*60)
    print("TEST: USER PERMISSIONS")
    print("="*60)
    
    # 1. Вход как обычный пользователь
    user_session = requests.Session()
    response = user_session.post(f"{BASE_URL}/auth/login", json={
        "email": "user@example.com",
        "password": "user123"
    })
    print_response("1. Вход как обычный пользователь", response)
    
    # 2. Попытка чтения статей (должна быть успешной - есть права)
    response = user_session.get(f"{BASE_URL}/resources/articles")
    print_response("2. Получение статей (user имеет articles:read)", response)
    
    # 3. Попытка создания статьи (должна вернуть 403)
    response = user_session.post(f"{BASE_URL}/resources/articles", json={
        "title": "Попытка создать статью",
        "content": "Не должно сработать"
    })
    print_response("3. Попытка создать статью (403 - нет прав)", response)
    
    # 4. Попытка доступа к отчетам (должна вернуть 403)
    response = user_session.get(f"{BASE_URL}/resources/reports")
    print_response("4. Попытка получить отчеты (403 - нет прав)", response)


def test_editor_permissions():
    """Тестирование прав редактора"""
    print("\n" + "="*60)
    print("TEST: EDITOR PERMISSIONS")
    print("="*60)
    
    # 1. Вход как редактор
    editor_session = requests.Session()
    response = editor_session.post(f"{BASE_URL}/auth/login", json={
        "email": "editor@example.com",
        "password": "editor123"
    })
    print_response("1. Вход как редактор", response)
    
    # 2. Создание статьи (должна быть успешной)
    response = editor_session.post(f"{BASE_URL}/resources/articles", json={
        "title": "Статья от редактора",
        "content": "Редактор может создавать статьи"
    })
    print_response("2. Создание статьи (editor имеет права)", response)
    
    # 3. Попытка удалить статью (должна вернуть 403 - нет прав)
    response = editor_session.delete(f"{BASE_URL}/resources/articles/1")
    print_response("3. Попытка удалить статью (403 - нет прав)", response)
    
    # 4. Попытка получить отчеты (должна вернуть 403)
    response = editor_session.get(f"{BASE_URL}/resources/reports")
    print_response("4. Попытка получить отчеты (403 - нет прав)", response)


def test_manager_permissions():
    """Тестирование прав менеджера"""
    print("\n" + "="*60)
    print("TEST: MANAGER PERMISSIONS")
    print("="*60)
    
    # 1. Вход как менеджер
    manager_session = requests.Session()
    response = manager_session.post(f"{BASE_URL}/auth/login", json={
        "email": "manager@example.com",
        "password": "manager123"
    })
    print_response("1. Вход как менеджер", response)
    
    # 2. Получение отчетов (должна быть успешной)
    response = manager_session.get(f"{BASE_URL}/resources/reports")
    print_response("2. Получение отчетов (manager имеет доступ)", response)
    
    # 3. Создание отчета
    response = manager_session.post(f"{BASE_URL}/resources/reports", json={
        "title": "Отчет от менеджера",
        "date": "2026-02-13"
    })
    print_response("3. Создание отчета (manager имеет права)", response)
    
    # 4. Попытка создать статью (должна вернуть 403)
    response = manager_session.post(f"{BASE_URL}/resources/articles", json={
        "title": "Попытка",
        "content": "Не должно сработать"
    })
    print_response("4. Попытка создать статью (403 - нет прав)", response)


def test_admin_management():
    """Тестирование функций администрирования"""
    print("\n" + "="*60)
    print("TEST: ADMIN MANAGEMENT FUNCTIONS")
    print("="*60)
    
    # Вход как администратор
    admin_session = requests.Session()
    admin_session.post(f"{BASE_URL}/auth/login", json={
        "email": "admin@example.com",
        "password": "admin123"
    })
    
    # 1. Получение всех ролей
    response = admin_session.get(f"{BASE_URL}/admin/roles")
    print_response("1. Получение всех ролей", response)
    
    # 2. Получение всех разрешений
    response = admin_session.get(f"{BASE_URL}/admin/permissions")
    print_response("2. Получение всех разрешений", response)
    
    # 3. Получение всех пользователей
    response = admin_session.get(f"{BASE_URL}/admin/users")
    print_response("3. Получение всех пользователей", response)
    
    # 4. Создание новой роли
    response = admin_session.post(f"{BASE_URL}/admin/roles", json={
        "name": "tester",
        "description": "Роль для тестирования"
    })
    print_response("4. Создание новой роли 'tester'", response)
    
    # 5. Попытка создать роль с существующим именем (409)
    response = admin_session.post(f"{BASE_URL}/admin/roles", json={
        "name": "admin",
        "description": "Дубликат"
    })
    print_response("5. Попытка создать дубликат роли (409)", response)


def test_unauthorized_access():
    """Тестирование доступа без авторизации"""
    print("\n" + "="*60)
    print("TEST: UNAUTHORIZED ACCESS")
    print("="*60)
    
    # Попытка доступа без входа
    response = requests.get(f"{BASE_URL}/resources/articles")
    print_response("Попытка получить статьи без авторизации (401)", response)


def test_profile_management():
    """Тестирование управления профилем"""
    print("\n" + "="*60)
    print("TEST: PROFILE MANAGEMENT")
    print("="*60)
    
    # Регистрация нового пользователя
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "email": "newuser@test.com",
        "password": "test123456",
        "password_confirm": "test123456",
        "first_name": "Тестовый",
        "last_name": "Пользователь",
        "middle_name": "Тестович"
    })
    print_response("1. Регистрация нового пользователя", response)
    
    # Вход
    user_session = requests.Session()
    response = user_session.post(f"{BASE_URL}/auth/login", json={
        "email": "newuser@test.com",
        "password": "test123456"
    })
    print_response("2. Вход нового пользователя", response)
    
    # Обновление профиля
    response = user_session.put(f"{BASE_URL}/user/profile", json={
        "first_name": "Обновленное Имя",
        "last_name": "Обновленная Фамилия"
    })
    print_response("3. Обновление профиля", response)
    
    # Получение обновленного профиля
    response = user_session.get(f"{BASE_URL}/user/profile")
    print_response("4. Получение обновленного профиля", response)
    
    # Мягкое удаление аккаунта
    response = user_session.delete(f"{BASE_URL}/user/profile")
    print_response("5. Мягкое удаление аккаунта", response)
    
    # Попытка войти с удаленным аккаунтом (403)
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "newuser@test.com",
        "password": "test123456"
    })
    print_response("6. Попытка входа с удаленным аккаунтом (403)", response)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("STARTING API TESTS")
    print("="*60)
    
    try:
        test_unauthorized_access()
        test_auth()
        test_user_permissions()
        test_editor_permissions()
        test_manager_permissions()
        test_admin_management()
        test_profile_management()
        
        print("\n" + "="*60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\nERROR: Cannot connect to server.")
        print("Make sure Flask app is running: python run.py")
    except Exception as e:
        print(f"\nERROR: {e}")
