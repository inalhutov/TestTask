# Система аутентификации и авторизации

Проект демонстрирует RBAC (Role-Based Access Control) - систему, где права доступа раздаются через роли. У каждого пользователя есть роли (например, "редактор" или "менеджер"), а у ролей - конкретные разрешения (например, "может создавать статьи").

## Как устроена база данных

В проекте 6 таблиц:

**Основные:**
- `users` - пользователи с email, паролем (захешированным) и ФИО
- `roles` - роли типа admin, user, editor
- `permissions` - разрешения вида "articles:read" или "documents:create"

**Связующие:**
- `user_roles` - связывает пользователей и их роли (один пользователь может иметь несколько ролей)
- `role_permissions` - связывает роли с разрешениями (одна роль может иметь много разрешений)

**Для сессий:**
- `user_sessions` - хранит токены сессий для залогиненных пользователей

## Как это работает

1. Пользователь регистрируется и получает роль "user" (базовая)
2. Когда он логинится, создается сессия на 1 час
3. При попытке что-то сделать (например, создать статью) система проверяет:
   - Залогинен ли пользователь? (проверяет сессию)
   - Есть ли у него нужное разрешение? (проходится по всем его ролям)
4. Если все ОК - запрос выполняется, если нет - 401 или 403

## Быстрый старт

```bash
# зависимости
pip install -r requirements.txt

# Создаем базу с тестовыми данными
flask --app run init-db

# Запуск
python run.py
```

## Тестовые аккаунты

Уже есть готовые пользователи для теста:

| Email | Пароль | Что может делать |
|-------|--------|------------------|
| admin@example.com | admin123 | Все, включая управление пользователями |
| user@example.com | user123 | Только читать статьи и документы |
| editor@example.com | editor123 | Создавать и редактировать статьи/документы |
| manager@example.com | manager123 | Работать с отчетами |
| multirole@example.com | multi123 | Права редактора + менеджера одновременно |

## Какие есть роли

**admin** - полный доступ ко всему + может управлять пользователями и правами

**user** - базовая роль, может только смотреть контент (статьи и документы)

**editor** - может создавать и редактировать статьи и документы, но не удалять

**manager** - работает с отчетами (создание, чтение, обновление) + может читать статьи и документы

## API

### Регистрация и вход

**Регистрация**
```
POST /api/auth/register
```
Отправляешь JSON с email, паролем (дважды), именем и фамилией.

**Вход**
```
POST /api/auth/login
```
Email + пароль. Получаешь токен сессии.

**Выход**
```
POST /api/auth/logout
```
Убивает текущую сессию.

**Кто я?**
```
GET /api/auth/me
```
Показывает инфу о залогиненном пользователе.

### Профиль

```
GET /api/user/profile          # Посмотреть свой профиль
PUT /api/user/profile          # Изменить имя/фамилию
PUT /api/user/profile/password # Сменить пароль
DELETE /api/user/profile       # Удалить аккаунт (мягкое удаление)
```

### Админка (только для admin)

```
GET /api/admin/roles           # Все роли
POST /api/admin/roles          # Создать роль
PUT /api/admin/roles/<id>      # Изменить роль
DELETE /api/admin/roles/<id>   # Удалить роль

GET /api/admin/permissions     # Все разрешения
POST /api/admin/permissions    # Создать разрешение
DELETE /api/admin/permissions/<id> # Удалить разрешение

GET /api/admin/users           # Все пользователи
POST /api/admin/users/<id>/roles # Добавить роль пользователю
DELETE /api/admin/users/<id>/roles/<role_id> # Убрать роль

POST /api/admin/roles/<id>/permissions # Добавить разрешение к роли
DELETE /api/admin/roles/<id>/permissions/<perm_id> # Убрать разрешение
```

### Ресурсы (Mock)

Для демонстрации прав сделаны три типа mock-ресурсов:

**Статьи:**
```
GET /api/resources/articles        # Список (нужно articles:read)
GET /api/resources/articles/<id>   # Одна статья
POST /api/resources/articles       # Создать (нужно articles:create)
PUT /api/resources/articles/<id>   # Изменить (нужно articles:update)
DELETE /api/resources/articles/<id> # Удалить (нужно articles:delete)
```

**Документы:**
```
GET /api/resources/documents       # Список
POST /api/resources/documents      # Создать
DELETE /api/resources/documents/<id> # Удалить
```

**Отчеты:**
```
GET /api/resources/reports         # Список
POST /api/resources/reports        # Создать
PUT /api/resources/reports/<id>    # Изменить
```

## Примеры на PowerShell

Зарегистрировать пользователя:
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/auth/register" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"email":"test@test.com","password":"123456","password_confirm":"123456","first_name":"Иван","last_name":"Тестов"}'
```

Войти (сохраняем сессию):
```powershell
$response = Invoke-WebRequest -Uri "http://localhost:5000/api/auth/login" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"email":"admin@example.com","password":"admin123"}' `
  -SessionVariable session
```

## Коды ответов

- `200` - все хорошо
- `201` - создано
- `400` - неправильный запрос (что-то не заполнил или неверный формат)
- `401` - не залогинен (нужна авторизация)
- `403` - недостаточно прав (залогинен, но прав нет)
- `404` - не найдено
- `409` - конфликт (например, email уже занят)

## Технические детали

**Безопасность:**
- Пароли хешируются через bcrypt (не хранятся в открытом виде)
- Сессии истекают через час
- HttpOnly cookies (нельзя украсть через JavaScript)
- Мягкое удаление - данные не удаляются из базы, просто ставится флаг is_active=False

**Что используется:**
- Flask - веб-фреймворк
- SQLAlchemy - работа с базой данных
- SQLite - сама база (файл DB/auth_system.db)
- Flask-Bcrypt - хеширование паролей


