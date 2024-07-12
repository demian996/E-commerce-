from flask import Blueprint, jsonify, request
from app.factories.dao_factory import DAOFactory

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/', methods=['GET'])
def get_pedidos():
    dao = DAOFactory.get_pedido_dao('postgres')
    pedidos = dao.get_all()
    return jsonify([{'id': p.id, 'usuario_id': p.usuario_id, 'fecha': p.fecha, 'total': p.total, 'estado': p.estado} for p in pedidos])

@pedidos_bp.route('/<int:id>', methods=['GET'])
def get_pedido(id):
    dao = DAOFactory.get_pedido_dao('postgres')
    pedido = dao.get_by_id(id)
    if pedido:
        return jsonify({'id': pedido.id, 'usuario_id': pedido.usuario_id, 'fecha': pedido.fecha, 'total': pedido.total, 'estado': pedido.estado})
    else:
        return jsonify({'error': 'Pedido no encontrado'}), 404

@pedidos_bp.route('/', methods=['POST'])
def create_pedido():
    data = request.get_json()
    dao = DAOFactory.get_pedido_dao('postgres')
    nuevo_pedido = dao.create(data['usuario_id'], data['total'], data['estado'])
    return jsonify({'id': nuevo_pedido.id, 'usuario_id': nuevo_pedido.usuario_id, 'fecha': nuevo_pedido.fecha, 'total': nuevo_pedido.total, 'estado': nuevo_pedido.estado}), 201

@pedidos_bp.route('/<int:id>', methods=['PUT'])
def update_pedido(id):
    data = request.get_json()
    dao = DAOFactory.get_pedido_dao('postgres')
    pedido = dao.update(id, data['total'], data['estado'])
    if pedido:
        return jsonify({'id': pedido.id, 'usuario_id': pedido.usuario_id, 'fecha': pedido.fecha, 'total': pedido.total, 'estado': pedido.estado})
    else:
        return jsonify({'error': 'Pedido no encontrado'}), 404

@pedidos_bp.route('/<int:id>', methods=['DELETE'])
def delete_pedido(id):
    dao = DAOFactory.get_pedido_dao('postgres')
    pedido = dao.delete(id)
    if pedido:
        return jsonify({'message': 'Pedido eliminado'})
    else:
        return jsonify({'error': 'Pedido no encontrado'}), 404
