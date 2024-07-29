from flask import Blueprint, jsonify, request, session, flash, redirect, url_for
from app.factories.dao_factory import DAOFactory
from config_access import verify_token
import functools

pedidos_bp = Blueprint('pedidos', __name__)

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

@pedidos_bp.route('/', methods=['GET'])
@token_required
def get_pedidos():
    dao = DAOFactory.get_pedido_dao('postgres')
    pedidos = dao.get_all()
    return jsonify([{'id': p.id, 'usuario_id': p.usuario_id, 'fecha': p.fecha, 'total': p.total, 'estado': p.estado} for p in pedidos])

@pedidos_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_pedido(id):
    dao = DAOFactory.get_pedido_dao('postgres')
    pedido = dao.get_by_id(id)
    if pedido:
        return jsonify({'id': pedido.id, 'usuario_id': pedido.usuario_id, 'fecha': pedido.fecha, 'total': pedido.total, 'estado': pedido.estado})
    else:
        return jsonify({'error': 'Pedido no encontrado'}), 404

@pedidos_bp.route('/', methods=['POST'])
@token_required
def create_pedido():
    data = request.get_json()
    dao = DAOFactory.get_pedido_dao('postgres')
    nuevo_pedido = dao.create(data['usuario_id'], data['total'], data['estado'])
    return jsonify({'id': nuevo_pedido.id, 'usuario_id': nuevo_pedido.usuario_id, 'fecha': nuevo_pedido.fecha, 'total': nuevo_pedido.total, 'estado': nuevo_pedido.estado}), 201

@pedidos_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_pedido(id):
    data = request.get_json()
    dao = DAOFactory.get_pedido_dao('postgres')
    pedido = dao.update(id, data['total'], data['estado'])
    if pedido:
        return jsonify({'id': pedido.id, 'usuario_id': pedido.usuario_id, 'fecha': pedido.fecha, 'total': pedido.total, 'estado': pedido.estado})
    else:
        return jsonify({'error': 'Pedido no encontrado'}), 404

@pedidos_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_pedido(id):
    dao = DAOFactory.get_pedido_dao('postgres')
    pedido = dao.delete(id)
    if pedido:
        return jsonify({'message': 'Pedido eliminado'})
    else:
        return jsonify({'error': 'Pedido no encontrado'}), 404
