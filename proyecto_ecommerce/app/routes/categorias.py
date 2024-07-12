from flask import Blueprint, jsonify, request, render_template
from app.factories.dao_factory import DAOFactory

categorias_bp = Blueprint('categorias_bp', __name__)

# Rutas existentes para la API JSON
@categorias_bp.route('/', methods=['GET'])
def get_categorias():
    dao = DAOFactory.get_categoria_dao('mysql')
    categorias = dao.get_all()
    return jsonify([{'id': c.id, 'nombre': c.nombre, 'descripcion': c.descripcion} for c in categorias])

@categorias_bp.route('/<int:id>', methods=['GET'])
def get_categoria(id):
    dao = DAOFactory.get_categoria_dao('mysql')
    categoria = dao.get_by_id(id)
    if categoria:
        return jsonify({'id': categoria.id, 'nombre': categoria.nombre, 'descripcion': categoria.descripcion})
    else:
        return jsonify({'error': 'Categoria no encontrada'}), 404

@categorias_bp.route('/', methods=['POST'])
def create_categoria():
    data = request.get_json()
    dao = DAOFactory.get_categoria_dao('mysql')
    nueva_categoria = dao.create(data['nombre'], data['descripcion'])
    return jsonify({'id': nueva_categoria.id, 'nombre': nueva_categoria.nombre, 'descripcion': nueva_categoria.descripcion}), 201

@categorias_bp.route('/<int:id>', methods=['PUT'])
def update_categoria(id):
    data = request.get_json()
    dao = DAOFactory.get_categoria_dao('mysql')
    categoria = dao.update(id, data['nombre'], data['descripcion'])
    if categoria:
        return jsonify({'id': categoria.id, 'nombre': categoria.nombre, 'descripcion': categoria.descripcion})
    else:
        return jsonify({'error': 'Categoria no encontrada'}), 404

@categorias_bp.route('/<int:id>', methods=['DELETE'])
def delete_categoria(id):
    dao = DAOFactory.get_categoria_dao('mysql')
    categoria = dao.delete(id)
    if categoria:
        return jsonify({'message': 'Categoria eliminada'})
    else:
        return jsonify({'error': 'Categoria no encontrada'}), 404

# Nuevas rutas para las vistas HTML
@categorias_bp.route('/categorias', methods=['GET'])
def listar_categorias():
    dao = DAOFactory.get_categoria_dao('mysql')
    categorias = dao.get_all()
    return render_template('categorias.html', categorias=categorias)

@categorias_bp.route('/categorias/<int:categoria_id>', methods=['GET'])
def listar_productos(categoria_id):
    dao_categoria = DAOFactory.get_categoria_dao('mysql')
    dao_producto = DAOFactory.get_producto_dao('mysql')
    categoria = dao_categoria.get_by_id(categoria_id)
    productos = dao_producto.get_by_categoria_id(categoria_id)
    return render_template('productos.html', categoria=categoria, productos=productos)

@categorias_bp.route('/api/categorias', methods=['GET'])
def get_categorias_json():
    dao = DAOFactory.get_categoria_dao('mysql')
    categorias = dao.get_all()
    return jsonify([{'id': c.id, 'nombre': c.nombre, 'descripcion': c.descripcion} for c in categorias])
