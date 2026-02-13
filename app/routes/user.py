from flask import Blueprint, request, jsonify
from datetime import datetime

from app import db
from app.models import User
from app.auth import login_required, get_current_user, invalidate_user_sessions, hash_password

user_bp = Blueprint('user', __name__)


@user_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    user = get_current_user()
    return jsonify({'user': user.to_dict(include_roles=True)}), 200


@user_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    user = get_current_user()
    data = request.get_json()
    
    if 'first_name' in data and data['first_name']:
        user.first_name = data['first_name']
    
    if 'last_name' in data and data['last_name']:
        user.last_name = data['last_name']
    
    if 'middle_name' in data:
        user.middle_name = data['middle_name']
    
    if 'email' in data and data['email']:
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({'error': 'Email уже используется другим пользователем'}), 409
        user.email = data['email']
    
    user.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Профиль успешно обновлен',
        'user': user.to_dict()
    }), 200


@user_bp.route('/profile/password', methods=['PUT'])
@login_required
def change_password():
    from app.auth import verify_password
    
    user = get_current_user()
    data = request.get_json()
    
    required_fields = ['old_password', 'new_password', 'new_password_confirm']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'Поле {field} обязательно'}), 400
    
    if not verify_password(user.password_hash, data['old_password']):
        return jsonify({'error': 'Неверный текущий пароль'}), 401
    
    if data['new_password'] != data['new_password_confirm']:
        return jsonify({'error': 'Новые пароли не совпадают'}), 400
    
    if len(data['new_password']) < 6:
        return jsonify({'error': 'Новый пароль должен содержать минимум 6 символов'}), 400
    
    user.password_hash = hash_password(data['new_password'])
    user.updated_at = datetime.utcnow()
    db.session.commit()
    
    from flask import session
    current_token = session.get('session_token')
    from app.models import UserSession
    UserSession.query.filter(
        UserSession.user_id == user.id,
        UserSession.session_token != current_token,
        UserSession.is_active == True
    ).update({'is_active': False})
    db.session.commit()
    
    return jsonify({'message': 'Пароль успешно изменен'}), 200


@user_bp.route('/profile', methods=['DELETE'])
@login_required
def delete_account():
    user = get_current_user()
    
    user.is_active = False
    user.deleted_at = datetime.utcnow()
    
    invalidate_user_sessions(user.id)
    
    db.session.commit()
    
    from flask import session
    session.clear()
    
    return jsonify({'message': 'Аккаунт успешно удален'}), 200
