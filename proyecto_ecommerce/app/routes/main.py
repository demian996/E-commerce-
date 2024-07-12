from flask import Blueprint, jsonify, request, render_template
from app.factories.dao_factory import DAOFactory

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/categorias', methods=['GET'])
def get_categorias():
    dao = DAOFactory.get_categoria_dao('mysql')
    categorias = dao.get_all()
    return jsonify([{'id': c.id, 'nombre': c.nombre, 'descripcion': c.descripcion} for c in categorias])

@main_bp.route('/categorias/<int:id>', methods=['GET'])
def get_categoria(id):
    dao = DAOFactory.get_categoria_dao('mysql')
    categoria = dao.get_by_id(id)
    if categoria:
        return jsonify({'id': categoria.id, 'nombre': categoria.nombre, 'descripcion': categoria.descripcion})
    else:
        return jsonify({'error': 'Categoria no encontrada'}), 404

@main_bp.route('/categorias', methods=['POST'])
def create_categoria():
    data = request.get_json()
    dao = DAOFactory.get_categoria_dao('mysql')
    nueva_categoria = dao.create(data['nombre'], data['descripcion'])
    return jsonify({'id': nueva_categoria.id, 'nombre': nueva_categoria.nombre, 'descripcion': nueva_categoria.descripcion}), 201

@main_bp.route('/categorias/<int:id>', methods=['PUT'])
def update_categoria(id):
    data = request.get_json()
    dao = DAOFactory.get_categoria_dao('mysql')
    categoria = dao.update(id, data['nombre'], data['descripcion'])
    if categoria:
        return jsonify({'id': categoria.id, 'nombre': categoria.nombre, 'descripcion': categoria.descripcion})
    else:
        return jsonify({'error': 'Categoria no encontrada'}), 404

@main_bp.route('/admin')
def home_admin():
    return render_template('home_admin.html')

@main_bp.route('/categorias/<int:id>', methods=['DELETE'])
def delete_categoria(id):
    dao = DAOFactory.get_categoria_dao('mysql')
    categoria = dao.delete(id)
    if categoria:
        return jsonify({'message': 'Categoria eliminada'})
    else:
        return jsonify({'error': 'Categoria no encontrada'}), 404

