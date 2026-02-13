from functools import wraps
from flask import request, jsonify, session
from datetime import datetime, timedelta
import secrets

from app import db, bcrypt
from app.models import User, UserSession


def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')


def verify_password(password_hash, password):
    return bcrypt.check_password_hash(password_hash, password)


def create_session_token():
    return secrets.token_urlsafe(32)


def create_user_session(user_id, expires_in_hours=1):
    session_token = create_session_token()
    expires_at = datetime.utcnow() + timedelta(hours=expires_in_hours)
    
    user_session = UserSession(
        user_id=user_id,
        session_token=session_token,
        expires_at=expires_at
    )
    
    db.session.add(user_session)
    db.session.commit()
    
    return session_token


def get_current_user():
    session_token = session.get('session_token')
    
    if not session_token:
        return None
    
    user_session = UserSession.query.filter_by(
        session_token=session_token,
        is_active=True
    ).first()
    
    if not user_session:
        return None
    
    if user_session.expires_at < datetime.utcnow():
        user_session.is_active = False
        db.session.commit()
        return None
    
    user = User.query.get(user_session.user_id)
    
    if not user or not user.is_active:
        return None
    
    return user


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if user is None:
            return jsonify({'error': 'Unauthorized', 'message': 'Необходима авторизация'}), 401
        return f(*args, **kwargs)
    return decorated_function


def permission_required(resource_type, action):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            if user is None:
                return jsonify({'error': 'Unauthorized', 'message': 'Необходима авторизация'}), 401
            
            if not user.has_permission(resource_type, action):
                return jsonify({
                    'error': 'Forbidden', 
                    'message': f'Недостаточно прав для выполнения действия {action} над ресурсом {resource_type}'
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def role_required(role_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            if user is None:
                return jsonify({'error': 'Unauthorized', 'message': 'Необходима авторизация'}), 401
            
            if not user.has_role(role_name):
                return jsonify({
                    'error': 'Forbidden', 
                    'message': f'Требуется роль {role_name}'
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def invalidate_user_sessions(user_id):
    UserSession.query.filter_by(user_id=user_id, is_active=True).update({'is_active': False})
    db.session.commit()
