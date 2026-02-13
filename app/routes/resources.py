from flask import Blueprint, request, jsonify

from app.auth import login_required, permission_required, get_current_user

resources_bp = Blueprint('resources', __name__)

MOCK_ARTICLES = [
    {'id': 1, 'title': 'Введение в Python', 'content': 'Python - это высокоуровневый язык программирования...', 'author': 'Иван Иванов'},
    {'id': 2, 'title': 'Основы Flask', 'content': 'Flask - микрофреймворк для веб-разработки...', 'author': 'Петр Петров'},
    {'id': 3, 'title': 'SQLAlchemy ORM', 'content': 'SQLAlchemy - это SQL toolkit и ORM для Python...', 'author': 'Сидор Сидоров'},
]

MOCK_DOCUMENTS = [
    {'id': 1, 'title': 'Спецификация проекта', 'type': 'PDF', 'size': '2.4 MB'},
    {'id': 2, 'title': 'Техническое задание', 'type': 'DOCX', 'size': '1.8 MB'},
    {'id': 3, 'title': 'Договор поставки', 'type': 'PDF', 'size': '0.5 MB'},
]

MOCK_REPORTS = [
    {'id': 1, 'title': 'Финансовый отчет Q1 2026', 'date': '2026-03-31', 'status': 'completed'},
    {'id': 2, 'title': 'Отчет по продажам', 'date': '2026-02-01', 'status': 'in_progress'},
    {'id': 3, 'title': 'Аналитический отчет', 'date': '2026-01-15', 'status': 'completed'},
]


@resources_bp.route('/articles', methods=['GET'])
@login_required
@permission_required('articles', 'read')
def get_articles():
    return jsonify({
        'resource_type': 'articles',
        'action': 'read',
        'data': MOCK_ARTICLES
    }), 200


@resources_bp.route('/articles/<int:article_id>', methods=['GET'])
@login_required
@permission_required('articles', 'read')
def get_article(article_id):
    article = next((a for a in MOCK_ARTICLES if a['id'] == article_id), None)
    if not article:
        return jsonify({'error': 'Статья не найдена'}), 404
    
    return jsonify({
        'resource_type': 'articles',
        'action': 'read',
        'data': article
    }), 200


@resources_bp.route('/articles', methods=['POST'])
@login_required
@permission_required('articles', 'create')
def create_article():
    data = request.get_json()
    
    new_article = {
        'id': len(MOCK_ARTICLES) + 1,
        'title': data.get('title', 'Новая статья'),
        'content': data.get('content', ''),
        'author': get_current_user().email
    }
    
    return jsonify({
        'message': 'Статья успешно создана',
        'resource_type': 'articles',
        'action': 'create',
        'data': new_article
    }), 201


@resources_bp.route('/articles/<int:article_id>', methods=['PUT'])
@login_required
@permission_required('articles', 'update')
def update_article(article_id):
    data = request.get_json()
    
    article = next((a for a in MOCK_ARTICLES if a['id'] == article_id), None)
    if not article:
        return jsonify({'error': 'Статья не найдена'}), 404
    
    updated_article = article.copy()
    updated_article.update({
        'title': data.get('title', article['title']),
        'content': data.get('content', article['content'])
    })
    
    return jsonify({
        'message': 'Статья успешно обновлена',
        'resource_type': 'articles',
        'action': 'update',
        'data': updated_article
    }), 200


@resources_bp.route('/articles/<int:article_id>', methods=['DELETE'])
@login_required
@permission_required('articles', 'delete')
def delete_article(article_id):
    article = next((a for a in MOCK_ARTICLES if a['id'] == article_id), None)
    if not article:
        return jsonify({'error': 'Статья не найдена'}), 404
    
    return jsonify({
        'message': f'Статья "{article["title"]}" успешно удалена',
        'resource_type': 'articles',
        'action': 'delete'
    }), 200


@resources_bp.route('/documents', methods=['GET'])
@login_required
@permission_required('documents', 'read')
def get_documents():
    return jsonify({
        'resource_type': 'documents',
        'action': 'read',
        'data': MOCK_DOCUMENTS
    }), 200


@resources_bp.route('/documents', methods=['POST'])
@login_required
@permission_required('documents', 'create')
def create_document():
    data = request.get_json()
    
    new_document = {
        'id': len(MOCK_DOCUMENTS) + 1,
        'title': data.get('title', 'Новый документ'),
        'type': data.get('type', 'PDF'),
        'size': '0 KB'
    }
    
    return jsonify({
        'message': 'Документ успешно создан',
        'resource_type': 'documents',
        'action': 'create',
        'data': new_document
    }), 201


@resources_bp.route('/documents/<int:document_id>', methods=['DELETE'])
@login_required
@permission_required('documents', 'delete')
def delete_document(document_id):
    document = next((d for d in MOCK_DOCUMENTS if d['id'] == document_id), None)
    if not document:
        return jsonify({'error': 'Документ не найден'}), 404
    
    return jsonify({
        'message': f'Документ "{document["title"]}" успешно удален',
        'resource_type': 'documents',
        'action': 'delete'
    }), 200


@resources_bp.route('/reports', methods=['GET'])
@login_required
@permission_required('reports', 'read')
def get_reports():
    return jsonify({
        'resource_type': 'reports',
        'action': 'read',
        'data': MOCK_REPORTS
    }), 200


@resources_bp.route('/reports', methods=['POST'])
@login_required
@permission_required('reports', 'create')
def create_report():
    data = request.get_json()
    
    new_report = {
        'id': len(MOCK_REPORTS) + 1,
        'title': data.get('title', 'Новый отчет'),
        'date': data.get('date', '2026-02-13'),
        'status': 'in_progress'
    }
    
    return jsonify({
        'message': 'Отчет успешно создан',
        'resource_type': 'reports',
        'action': 'create',
        'data': new_report
    }), 201


@resources_bp.route('/reports/<int:report_id>', methods=['PUT'])
@login_required
@permission_required('reports', 'update')
def update_report(report_id):
    data = request.get_json()
    
    report = next((r for r in MOCK_REPORTS if r['id'] == report_id), None)
    if not report:
        return jsonify({'error': 'Отчет не найден'}), 404
    
    updated_report = report.copy()
    updated_report.update({
        'title': data.get('title', report['title']),
        'status': data.get('status', report['status'])
    })
    
    return jsonify({
        'message': 'Отчет успешно обновлен',
        'resource_type': 'reports',
        'action': 'update',
        'data': updated_report
    }), 200
