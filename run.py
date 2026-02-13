from app import create_app, db
from app.models import User, Role, Permission
from app.auth import hash_password

app = create_app()


@app.cli.command()
def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        print("База данных создана!")
        
        permissions_data = [
            ('articles', 'create', 'Создание статей'),
            ('articles', 'read', 'Чтение статей'),
            ('articles', 'update', 'Обновление статей'),
            ('articles', 'delete', 'Удаление статей'),
            ('documents', 'create', 'Создание документов'),
            ('documents', 'read', 'Чтение документов'),
            ('documents', 'update', 'Обновление документов'),
            ('documents', 'delete', 'Удаление документов'),
            ('reports', 'create', 'Создание отчетов'),
            ('reports', 'read', 'Чтение отчетов'),
            ('reports', 'update', 'Обновление отчетов'),
            ('reports', 'delete', 'Удаление отчетов'),
        ]
        
        permissions = {}
        for resource_type, action, description in permissions_data:
            perm = Permission(
                resource_type=resource_type,
                action=action,
                description=description
            )
            db.session.add(perm)
            permissions[f"{resource_type}:{action}"] = perm
        
        db.session.commit()
        print(f"Создано {len(permissions)} разрешений")
        
        admin_role = Role(
            name='admin',
            description='Администратор системы с полными правами'
        )
        admin_role.permissions = list(permissions.values())
        db.session.add(admin_role)
        
        user_role = Role(
            name='user',
            description='Обычный пользователь с базовыми правами'
        )
        user_role.permissions = [
            permissions['articles:read'],
            permissions['documents:read'],
        ]
        db.session.add(user_role)
        
        editor_role = Role(
            name='editor',
            description='Редактор контента'
        )
        editor_role.permissions = [
            permissions['articles:create'],
            permissions['articles:read'],
            permissions['articles:update'],
            permissions['documents:create'],
            permissions['documents:read'],
            permissions['documents:update'],
        ]
        db.session.add(editor_role)
        
        manager_role = Role(
            name='manager',
            description='Менеджер с доступом к отчетам'
        )
        manager_role.permissions = [
            permissions['articles:read'],
            permissions['documents:read'],
            permissions['reports:create'],
            permissions['reports:read'],
            permissions['reports:update'],
        ]
        db.session.add(manager_role)
        
        db.session.commit()
        print("Созданы роли: admin, user, editor, manager")
        
        admin_user = User(
            email='admin@example.com',
            password_hash=hash_password('admin123'),
            first_name='Алексей',
            last_name='Админов',
            middle_name='Владимирович'
        )
        admin_user.roles.append(admin_role)
        db.session.add(admin_user)
        
        regular_user = User(
            email='user@example.com',
            password_hash=hash_password('user123'),
            first_name='Иван',
            last_name='Иванов',
            middle_name='Петрович'
        )
        regular_user.roles.append(user_role)
        db.session.add(regular_user)
        
        editor_user = User(
            email='editor@example.com',
            password_hash=hash_password('editor123'),
            first_name='Мария',
            last_name='Редакторова',
            middle_name='Сергеевна'
        )
        editor_user.roles.append(editor_role)
        db.session.add(editor_user)
        
        manager_user = User(
            email='manager@example.com',
            password_hash=hash_password('manager123'),
            first_name='Петр',
            last_name='Менеджеров',
            middle_name='Александрович'
        )
        manager_user.roles.append(manager_role)
        db.session.add(manager_user)
        
        multi_role_user = User(
            email='multirole@example.com',
            password_hash=hash_password('multi123'),
            first_name='Ольга',
            last_name='Многоролева',
            middle_name='Дмитриевна'
        )
        multi_role_user.roles.extend([editor_role, manager_role])
        db.session.add(multi_role_user)
        
        db.session.commit()
        print("\nСозданы тестовые пользователи:")
        print("1. admin@example.com / admin123 (роль: admin)")
        print("2. user@example.com / user123 (роль: user)")
        print("3. editor@example.com / editor123 (роль: editor)")
        print("4. manager@example.com / manager123 (роль: manager)")
        print("5. multirole@example.com / multi123 (роли: editor, manager)")
        print("\nИнициализация завершена!")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
