from flask import Blueprint, request, jsonify

from app import db
from app.models import User, Role, Permission
from app.auth import login_required, role_required, get_current_user

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/roles', methods=['GET'])
@login_required
@role_required('admin')
def get_roles():
    roles = Role.query.all()
    return jsonify({
        'roles': [role.to_dict(include_permissions=True) for role in roles]
    }), 200


@admin_bp.route('/roles', methods=['POST'])
@login_required
@role_required('admin')
def create_role():
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Имя роли обязательно'}), 400
    
    if Role.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Роль с таким именем уже существует'}), 409
    
    role = Role(
        name=data['name'],
        description=data.get('description')
    )
    
    db.session.add(role)
    db.session.commit()
    
    return jsonify({
        'message': 'Роль успешно создана',
        'role': role.to_dict()
    }), 201


@admin_bp.route('/roles/<int:role_id>', methods=['PUT'])
@login_required
@role_required('admin')
def update_role(role_id):
    role = Role.query.get_or_404(role_id)
    data = request.get_json()
    
    if 'name' in data and data['name']:
        existing_role = Role.query.filter_by(name=data['name']).first()
        if existing_role and existing_role.id != role_id:
            return jsonify({'error': 'Роль с таким именем уже существует'}), 409
        role.name = data['name']
    
    if 'description' in data:
        role.description = data['description']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Роль успешно обновлена',
        'role': role.to_dict()
    }), 200


@admin_bp.route('/roles/<int:role_id>', methods=['DELETE'])
@login_required
@role_required('admin')
def delete_role(role_id):
    role = Role.query.get_or_404(role_id)
    
    if role.name in ['admin', 'user']:
        return jsonify({'error': 'Нельзя удалить системную роль'}), 403
    
    db.session.delete(role)
    db.session.commit()
    
    return jsonify({'message': 'Роль успешно удалена'}), 200


@admin_bp.route('/permissions', methods=['GET'])
@login_required
@role_required('admin')
def get_permissions():
    permissions = Permission.query.all()
    return jsonify({
        'permissions': [perm.to_dict() for perm in permissions]
    }), 200


@admin_bp.route('/permissions', methods=['POST'])
@login_required
@role_required('admin')
def create_permission():
    data = request.get_json()
    
    required_fields = ['resource_type', 'action']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'Поле {field} обязательно'}), 400
    
    existing = Permission.query.filter_by(
        resource_type=data['resource_type'],
        action=data['action']
    ).first()
    
    if existing:
        return jsonify({'error': 'Разрешение уже существует'}), 409
    
    permission = Permission(
        resource_type=data['resource_type'],
        action=data['action'],
        description=data.get('description')
    )
    
    db.session.add(permission)
    db.session.commit()
    
    return jsonify({
        'message': 'Разрешение успешно создано',
        'permission': permission.to_dict()
    }), 201


@admin_bp.route('/permissions/<int:permission_id>', methods=['DELETE'])
@login_required
@role_required('admin')
def delete_permission(permission_id):
    permission = Permission.query.get_or_404(permission_id)
    
    db.session.delete(permission)
    db.session.commit()
    
    return jsonify({'message': 'Разрешение успешно удалено'}), 200


@admin_bp.route('/roles/<int:role_id>/permissions', methods=['POST'])
@login_required
@role_required('admin')
def add_permission_to_role(role_id):
    role = Role.query.get_or_404(role_id)
    data = request.get_json()
    
    if not data or not data.get('permission_id'):
        return jsonify({'error': 'permission_id обязательно'}), 400
    
    permission = Permission.query.get_or_404(data['permission_id'])
    
    if permission in role.permissions:
        return jsonify({'error': 'Разрешение уже назначено этой роли'}), 409
    
    role.permissions.append(permission)
    db.session.commit()
    
    return jsonify({
        'message': 'Разрешение успешно добавлено к роли',
        'role': role.to_dict(include_permissions=True)
    }), 200


@admin_bp.route('/roles/<int:role_id>/permissions/<int:permission_id>', methods=['DELETE'])
@login_required
@role_required('admin')
def remove_permission_from_role(role_id, permission_id):
    role = Role.query.get_or_404(role_id)
    permission = Permission.query.get_or_404(permission_id)
    
    if permission not in role.permissions:
        return jsonify({'error': 'Разрешение не назначено этой роли'}), 404
    
    role.permissions.remove(permission)
    db.session.commit()
    
    return jsonify({'message': 'Разрешение успешно удалено из роли'}), 200


@admin_bp.route('/users', methods=['GET'])
@login_required
@role_required('admin')
def get_users():
    users = User.query.all()
    return jsonify({
        'users': [user.to_dict(include_roles=True) for user in users]
    }), 200


@admin_bp.route('/users/<int:user_id>/roles', methods=['POST'])
@login_required
@role_required('admin')
def add_role_to_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if not data or not data.get('role_id'):
        return jsonify({'error': 'role_id обязательно'}), 400
    
    role = Role.query.get_or_404(data['role_id'])
    
    if role in user.roles:
        return jsonify({'error': 'Роль уже назначена пользователю'}), 409
    
    user.roles.append(role)
    db.session.commit()
    
    return jsonify({
        'message': 'Роль успешно назначена пользователю',
        'user': user.to_dict(include_roles=True)
    }), 200


@admin_bp.route('/users/<int:user_id>/roles/<int:role_id>', methods=['DELETE'])
@login_required
@role_required('admin')
def remove_role_from_user(user_id, role_id):
    user = User.query.get_or_404(user_id)
    role = Role.query.get_or_404(role_id)
    
    if role not in user.roles:
        return jsonify({'error': 'Роль не назначена пользователю'}), 404
    
    current_user = get_current_user()
    if user.id == current_user.id and role.name == 'admin':
        admin_roles = [r for r in user.roles if r.name == 'admin']
        if len(admin_roles) == 1:
            return jsonify({'error': 'Нельзя удалить последнюю роль администратора у себя'}), 403
    
    user.roles.remove(role)
    db.session.commit()
    
    return jsonify({'message': 'Роль успешно удалена у пользователя'}), 200
