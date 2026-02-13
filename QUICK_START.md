# Быстрый старт

## 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

## 2. Инициализация базы данных

```bash
flask --app run init-db
```

Будут созданы тестовые пользователи:
- **admin@example.com** / admin123 (полный доступ)
- **user@example.com** / user123 (только чтение)
- **editor@example.com** / editor123 (создание и редактирование контента)
- **manager@example.com** / manager123 (работа с отчетами)
- **multirole@example.com** / multi123 (редактор + менеджер)

## 3. Запуск приложения

```bash
python run.py
```

Приложение будет доступно по адресу: http://localhost:5000

## 4. Тестирование API

Запустите автоматические тесты:

```bash
python test_api.py
```

Тесты проверяют:
- ✅ Аутентификацию (регистрация, вход, выход)
- ✅ Авторизацию (проверка прав доступа)
- ✅ Коды ответов (401 Unauthorized, 403 Forbidden)
- ✅ RBAC систему (роли и разрешения)
- ✅ Административные функции
- ✅ Управление профилем
- ✅ Мягкое удаление пользователей

## Основные API endpoints

### Аутентификация
- `POST /api/auth/register` - регистрация
- `POST /api/auth/login` - вход
- `POST /api/auth/logout` - выход
- `GET /api/auth/me` - текущий пользователь

### Профиль
- `GET /api/user/profile` - получение профиля
- `PUT /api/user/profile` - обновление профиля
- `PUT /api/user/profile/password` - изменение пароля
- `DELETE /api/user/profile` - удаление аккаунта

### Ресурсы (требуют соответствующих прав)
- `GET /api/resources/articles` - список статей
- `POST /api/resources/articles` - создание статьи
- `GET /api/resources/documents` - список документов
- `GET /api/resources/reports` - список отчетов

### Администрирование (только admin)
- `GET /api/admin/roles` - список ролей
- `POST /api/admin/roles` - создание роли
- `GET /api/admin/permissions` - список разрешений
- `POST /api/admin/permissions` - создание разрешения
- `GET /api/admin/users` - список пользователей
- `POST /api/admin/users/{id}/roles` - назначение роли
- `POST /api/admin/roles/{id}/permissions` - добавление разрешения к роли

## Примеры использования

См. подробные примеры в файле `API_EXAMPLES.md`

## Документация

Полная документация в файле `README.md`
