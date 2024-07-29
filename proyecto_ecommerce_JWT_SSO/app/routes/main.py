from flask import Blueprint, jsonify, request, render_template, session, flash, redirect, url_for
from app.factories.dao_factory import DAOFactory
from config_access import verify_token
import functools

main_bp = Blueprint('main', __name__)

# Middleware para verificar token
def token_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        token = request.args.get('token')
        if not token:
            flash('Token no proporcionado', 'danger')
            return redirect(url_for('auth.login'))
        data = verify_token(token)
        if data is None:
            flash('Token inválido o expirado', 'danger')
            return redirect(url_for('auth.login'))
        session['user_id'] = data['user_id']
        session['user_role'] = data['user_role']
        return view(**kwargs)
    return wrapped_view

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/categorias', methods=['GET'])
@token_required
def get_categorias():
    dao = DAOFactory.get_categoria_dao('mysql')
    categorias = dao.get_all()
    return jsonify([{'id': c.id, 'nombre': c.nombre, 'descripcion': c.descripcion} for c in categorias])

@main_bp.route('/categorias/<int:id>', methods=['GET'])
@token_required
def get_categoria(id):
    dao = DAOFactory.get_categoria_dao('mysql')
    categoria = dao.get_by_id(id)
    if categoria:
        return jsonify({'id': categoria.id, 'nombre': categoria.nombre, 'descripcion': categoria.descripcion})
    else:
        return jsonify({'error': 'Categoria no encontrada'}), 404

@main_bp.route('/categorias', methods=['POST'])
@token_required
def create_categoria():
    data = request.get_json()
    dao = DAOFactory.get_categoria_dao('mysql')
    nueva_categoria = dao.create(data['nombre'], data['descripcion'])
    return jsonify({'id': nueva_categoria.id, 'nombre': nueva_categoria.nombre, 'descripcion': nueva_categoria.descripcion}), 201

@main_bp.route('/categorias/<int:id>', methods=['PUT'])
@token_required
def update_categoria(id):
    data = request.get_json()
    dao = DAOFactory.get_categoria_dao('mysql')
    categoria = dao.update(id, data['nombre'], data['descripcion'])
    if categoria:
        return jsonify({'id': categoria.id, 'nombre': categoria.nombre, 'descripcion': categoria.descripcion})
    else:
        return jsonify({'error': 'Categoria no encontrada'}), 404

@main_bp.route('/admin')
@token_required
def home_admin():
    return render_template('home_admin.html', token=request.args.get('token'))

@main_bp.route('/categorias/<int:id>', methods=['DELETE'])
@token_required
def delete_categoria(id):
    dao = DAOFactory.get_categoria_dao('mysql')
    categoria = dao.delete(id)
    if categoria:
        return jsonify({'message': 'Categoria eliminada'})
    else:
        return jsonify({'error': 'Categoria no encontrada'}), 404
