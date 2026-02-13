from flask import Blueprint, request, jsonify, session
from datetime import datetime

from app import db
from app.models import User, Role
from app.auth import (
    hash_password, verify_password, create_user_session, 
    get_current_user, invalidate_user_sessions
)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    required_fields = ['email', 'password', 'password_confirm', 'first_name', 'last_name']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'Поле {field} обязательно для заполнения'}), 400
    
    if data['password'] != data['password_confirm']:
        return jsonify({'error': 'Пароли не совпадают'}), 400
    
    if len(data['password']) < 6:
        return jsonify({'error': 'Пароль должен содержать минимум 6 символов'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Пользователь с таким email уже существует'}), 409
    
    user = User(
        email=data['email'],
        password_hash=hash_password(data['password']),
        first_name=data['first_name'],
        last_name=data['last_name'],
        middle_name=data.get('middle_name')
    )
    
    default_role = Role.query.filter_by(name='user').first()
    if default_role:
        user.roles.append(default_role)
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'Пользователь успешно зарегистрирован',
        'user': user.to_dict()
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email и пароль обязательны'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user:
        return jsonify({'error': 'Неверный email или пароль'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Аккаунт деактивирован'}), 403
    
    if not verify_password(user.password_hash, data['password']):
        return jsonify({'error': 'Неверный email или пароль'}), 401
    
    session_token = create_user_session(user.id)
    session['session_token'] = session_token
    session.permanent = True
    
    return jsonify({
        'message': 'Успешный вход',
        'user': user.to_dict(include_roles=True),
        'session_token': session_token
    }), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session_token = session.get('session_token')
    
    if session_token:
        from app.models import UserSession
        user_session = UserSession.query.filter_by(session_token=session_token).first()
        if user_session:
            user_session.is_active = False
            db.session.commit()
    
    session.clear()
    
    return jsonify({'message': 'Успешный выход'}), 200


@auth_bp.route('/me', methods=['GET'])
def get_me():
    user = get_current_user()
    
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    
    return jsonify({'user': user.to_dict(include_roles=True)}), 200
