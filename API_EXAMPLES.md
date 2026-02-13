# Примеры использования API

## Подготовка

Все примеры используют `curl`. Для Windows PowerShell замените `\` на `` ` `` (обратный апостроф).

Сохраняйте cookies в файл для поддержания сессии:
- `-c cookies.txt` - сохранить cookies
- `-b cookies.txt` - использовать сохраненные cookies

## 1. Регистрация и аутентификация

### Регистрация нового пользователя

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "test123456",
    "password_confirm": "test123456",
    "first_name": "Тест",
    "last_name": "Тестов",
    "middle_name": "Тестович"
  }'
```

### Вход в систему (сохранение сессии)

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "user@example.com",
    "password": "user123"
  }'
```

### Проверка текущего пользователя

```bash
curl -X GET http://localhost:5000/api/auth/me \
  -b cookies.txt
```

### Выход из системы

```bash
curl -X POST http://localhost:5000/api/auth/logout \
  -b cookies.txt
```

## 2. Управление профилем

### Получение профиля

```bash
curl -X GET http://localhost:5000/api/user/profile \
  -b cookies.txt
```

### Обновление профиля

```bash
curl -X PUT http://localhost:5000/api/user/profile \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "first_name": "Новое Имя",
    "last_name": "Новая Фамилия",
    "middle_name": "Новое Отчество"
  }'
```

### Изменение пароля

```bash
curl -X PUT http://localhost:5000/api/user/profile/password \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "old_password": "user123",
    "new_password": "newpassword123",
    "new_password_confirm": "newpassword123"
  }'
```

### Удаление аккаунта (мягкое)

```bash
curl -X DELETE http://localhost:5000/api/user/profile \
  -b cookies.txt
```

## 3. Работа с ресурсами (требуют соответствующих прав)

### Статьи

#### Получение списка статей (требует articles:read)

```bash
# Вход как обычный пользователь (имеет articles:read)
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -c user_cookies.txt \
  -d '{"email": "user@example.com", "password": "user123"}'

# Получение статей
curl -X GET http://localhost:5000/api/resources/articles \
  -b user_cookies.txt
```

#### Получение конкретной статьи

```bash
curl -X GET http://localhost:5000/api/resources/articles/1 \
  -b user_cookies.txt
```

#### Создание статьи (требует articles:create)

```bash
# Вход как редактор (имеет articles:create)
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -c editor_cookies.txt \
  -d '{"email": "editor@example.com", "password": "editor123"}'

# Создание статьи
curl -X POST http://localhost:5000/api/resources/articles \
  -H "Content-Type: application/json" \
  -b editor_cookies.txt \
  -d '{
    "title": "Моя новая статья",
    "content": "Содержимое статьи..."
  }'
```

#### Обновление статьи (требует articles:update)

```bash
curl -X PUT http://localhost:5000/api/resources/articles/1 \
  -H "Content-Type: application/json" \
  -b editor_cookies.txt \
  -d '{
    "title": "Обновленное название",
    "content": "Обновленное содержимое"
  }'
```

#### Удаление статьи (требует articles:delete - только admin)

```bash
# Вход как администратор
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -c admin_cookies.txt \
  -d '{"email": "admin@example.com", "password": "admin123"}'

# Удаление статьи
curl -X DELETE http://localhost:5000/api/resources/articles/1 \
  -b admin_cookies.txt
```

### Документы

#### Список документов

```bash
curl -X GET http://localhost:5000/api/resources/documents \
  -b user_cookies.txt
```

#### Создание документа (требует documents:create)

```bash
curl -X POST http://localhost:5000/api/resources/documents \
  -H "Content-Type: application/json" \
  -b editor_cookies.txt \
  -d '{
    "title": "Новый документ",
    "type": "PDF"
  }'
```

#### Удаление документа (требует documents:delete - только admin)

```bash
curl -X DELETE http://localhost:5000/api/resources/documents/1 \
  -b admin_cookies.txt
```

### Отчеты

#### Список отчетов (требует reports:read)

```bash
# Вход как менеджер (имеет reports:read)
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -c manager_cookies.txt \
  -d '{"email": "manager@example.com", "password": "manager123"}'

# Получение отчетов
curl -X GET http://localhost:5000/api/resources/reports \
  -b manager_cookies.txt
```

#### Создание отчета (требует reports:create)

```bash
curl -X POST http://localhost:5000/api/resources/reports \
  -H "Content-Type: application/json" \
  -b manager_cookies.txt \
  -d '{
    "title": "Квартальный отчет Q2 2026",
    "date": "2026-06-30"
  }'
```

#### Обновление отчета (требует reports:update)

```bash
curl -X PUT http://localhost:5000/api/resources/reports/1 \
  -H "Content-Type: application/json" \
  -b manager_cookies.txt \
  -d '{
    "title": "Обновленный отчет",
    "status": "completed"
  }'
```

## 4. Администрирование (только admin)

Войдите как администратор:

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -c admin_cookies.txt \
  -d '{"email": "admin@example.com", "password": "admin123"}'
```

### Управление ролями

#### Получение всех ролей

```bash
curl -X GET http://localhost:5000/api/admin/roles \
  -b admin_cookies.txt
```

#### Создание новой роли

```bash
curl -X POST http://localhost:5000/api/admin/roles \
  -H "Content-Type: application/json" \
  -b admin_cookies.txt \
  -d '{
    "name": "moderator",
    "description": "Модератор контента"
  }'
```

#### Обновление роли

```bash
curl -X PUT http://localhost:5000/api/admin/roles/5 \
  -H "Content-Type: application/json" \
  -b admin_cookies.txt \
  -d '{
    "name": "moderator",
    "description": "Обновленное описание модератора"
  }'
```

#### Удаление роли

```bash
curl -X DELETE http://localhost:5000/api/admin/roles/5 \
  -b admin_cookies.txt
```

### Управление разрешениями

#### Получение всех разрешений

```bash
curl -X GET http://localhost:5000/api/admin/permissions \
  -b admin_cookies.txt
```

#### Создание нового разрешения

```bash
curl -X POST http://localhost:5000/api/admin/permissions \
  -H "Content-Type: application/json" \
  -b admin_cookies.txt \
  -d '{
    "resource_type": "comments",
    "action": "moderate",
    "description": "Модерация комментариев"
  }'
```

#### Удаление разрешения

```bash
curl -X DELETE http://localhost:5000/api/admin/permissions/13 \
  -b admin_cookies.txt
```

### Управление пользователями

#### Получение всех пользователей

```bash
curl -X GET http://localhost:5000/api/admin/users \
  -b admin_cookies.txt
```

#### Назначение роли пользователю

```bash
# Назначить роль editor (id=3) пользователю с id=2
curl -X POST http://localhost:5000/api/admin/users/2/roles \
  -H "Content-Type: application/json" \
  -b admin_cookies.txt \
  -d '{
    "role_id": 3
  }'
```

#### Удаление роли у пользователя

```bash
# Удалить роль editor (id=3) у пользователя с id=2
curl -X DELETE http://localhost:5000/api/admin/users/2/roles/3 \
  -b admin_cookies.txt
```

### Управление разрешениями роли

#### Добавление разрешения к роли

```bash
# Добавить разрешение articles:delete (id=4) к роли editor (id=3)
curl -X POST http://localhost:5000/api/admin/roles/3/permissions \
  -H "Content-Type: application/json" \
  -b admin_cookies.txt \
  -d '{
    "permission_id": 4
  }'
```

#### Удаление разрешения из роли

```bash
# Удалить разрешение articles:delete (id=4) из роли editor (id=3)
curl -X DELETE http://localhost:5000/api/admin/roles/3/permissions/4 \
  -b admin_cookies.txt
```

## 5. Демонстрация работы системы прав доступа

### Сценарий 1: Пользователь без прав пытается создать статью

```bash
# Вход как обычный пользователь
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -c user_cookies.txt \
  -d '{"email": "user@example.com", "password": "user123"}'

# Попытка создать статью -> 403 Forbidden
curl -X POST http://localhost:5000/api/resources/articles \
  -H "Content-Type: application/json" \
  -b user_cookies.txt \
  -d '{"title": "Статья", "content": "Текст"}'
```

**Ожидаемый ответ:**
```json
{
  "error": "Forbidden",
  "message": "Недостаточно прав для выполнения действия create над ресурсом articles"
}
```

### Сценарий 2: Администратор назначает права

```bash
# Вход как администратор
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -c admin_cookies.txt \
  -d '{"email": "admin@example.com", "password": "admin123"}'

# Назначить роль editor пользователю user@example.com (предположим, id=2)
curl -X POST http://localhost:5000/api/admin/users/2/roles \
  -H "Content-Type: application/json" \
  -b admin_cookies.txt \
  -d '{"role_id": 3}'
```

### Сценарий 3: Пользователь теперь может создать статью

```bash
# Повторная попытка создать статью -> 201 Created
curl -X POST http://localhost:5000/api/resources/articles \
  -H "Content-Type: application/json" \
  -b user_cookies.txt \
  -d '{"title": "Моя статья", "content": "Теперь я могу создавать статьи!"}'
```

### Сценарий 4: Попытка доступа без аутентификации

```bash
# Попытка получить статьи без входа -> 401 Unauthorized
curl -X GET http://localhost:5000/api/resources/articles
```

**Ожидаемый ответ:**
```json
{
  "error": "Unauthorized",
  "message": "Необходима авторизация"
}
```

## 6. PowerShell (Windows) версии команд

Для PowerShell используйте:

```powershell
# Регистрация
Invoke-RestMethod -Uri "http://localhost:5000/api/auth/register" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"email":"test@example.com","password":"test123456","password_confirm":"test123456","first_name":"Тест","last_name":"Тестов"}'

# Вход (сохранение сессии)
$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
Invoke-RestMethod -Uri "http://localhost:5000/api/auth/login" `
  -Method Post `
  -ContentType "application/json" `
  -WebSession $session `
  -Body '{"email":"admin@example.com","password":"admin123"}'

# Использование сохраненной сессии
Invoke-RestMethod -Uri "http://localhost:5000/api/auth/me" `
  -Method Get `
  -WebSession $session

# Получение статей
Invoke-RestMethod -Uri "http://localhost:5000/api/resources/articles" `
  -Method Get `
  -WebSession $session
```

## Проверка системы прав

| Пользователь | Может читать статьи | Может создавать статьи | Может удалять статьи | Доступ к отчетам |
|--------------|---------------------|------------------------|----------------------|------------------|
| user         | ✅ Да               | ❌ Нет                 | ❌ Нет               | ❌ Нет           |
| editor       | ✅ Да               | ✅ Да                  | ❌ Нет               | ❌ Нет           |
| manager      | ✅ Да               | ❌ Нет                 | ❌ Нет               | ✅ Да            |
| admin        | ✅ Да               | ✅ Да                  | ✅ Да                | ✅ Да            |
| multirole    | ✅ Да               | ✅ Да                  | ❌ Нет               | ✅ Да            |
