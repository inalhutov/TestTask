# Структура проекта

```
test12/
├── app/                          # Основное приложение
│   ├── routes/                   # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py              # Аутентификация (register, login, logout)
│   │   ├── user.py              # Управление профилем
│   │   ├── admin.py             # Административные функции
│   │   └── resources.py         # Mock-ресурсы (articles, documents, reports)
│   ├── __init__.py              # Фабрика приложения
│   ├── models.py                # Модели БД (User, Role, Permission, UserSession)
│   └── auth.py                  # Функции аутентификации и декораторы
│
├── DB/                           # База данных SQLite (создается автоматически)
│   └── auth_system.db
│
├── .env                          # Переменные окружения
├── .gitignore                    # Игнорируемые файлы для Git
├── config.py                     # Конфигурация приложения
├── requirements.txt              # Зависимости Python
├── run.py                        # Точка входа + команда init-db
├── test_api.py                   # Автоматические тесты
│
├── README.md                     # Полная документация
├── QUICK_START.md               # Быстрый старт
├── API_EXAMPLES.md              # Примеры использования API
├── CHANGELOG.md                 # История изменений
└── PROJECT_STRUCTURE.md         # Этот файл
```

## Основные файлы

### Конфигурация
- **config.py** - настройки приложения, подключение к БД
- **.env** - секретные ключи и переменные окружения

### Модели данных (app/models.py)
- **User** - пользователи системы
- **Role** - роли (admin, user, editor, manager)
- **Permission** - разрешения (resource_type:action)
- **UserSession** - сессии пользователей

### API Routes
- **auth.py** - регистрация, вход, выход (3 endpoint)
- **user.py** - управление профилем (3 endpoint)
- **admin.py** - администрирование (13 endpoint)
- **resources.py** - mock-ресурсы (11 endpoint)

### Тестирование
- **test_api.py** - автоматические тесты всех функций

## Запуск

```bash
# Установка зависимостей
pip install -r requirements.txt

# Инициализация БД
flask --app run init-db

# Запуск приложения
python run.py

# Тестирование
python test_api.py
```

## Ключевые возможности

✅ Собственная система аутентификации (без Flask-Login)
✅ RBAC (Role-Based Access Control)
✅ Детальные разрешения (resource:action)
✅ Session-based аутентификация
✅ Мягкое удаление пользователей
✅ Хеширование паролей (bcrypt)
✅ API для администрирования
✅ Mock-ресурсы для демонстрации
✅ Полная документация
✅ Автоматические тесты
