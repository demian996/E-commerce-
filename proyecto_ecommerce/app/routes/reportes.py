from flask import Blueprint, jsonify
from app.factories.dao_factory import DAOFactory

reportes_bp = Blueprint('reportes', __name__)

@reportes_bp.route('/categorias', methods=['GET'])
def reporte_categorias():
    dao = DAOFactory.get_categoria_dao('mysql')
    categorias = dao.get_all()
    return jsonify([{'id': c.id, 'nombre': c.nombre, 'descripcion': c.descripcion} for c in categorias])

@reportes_bp.route('/pedidos', methods=['GET'])
def reporte_pedidos():
    dao = DAOFactory.get_pedido_dao('postgres')
    pedidos = dao.get_all()
    return jsonify([{'id': p.id, 'usuario_id': p.usuario_id, 'fecha': p.fecha, 'total': p.total, 'estado': p.estado} for p in pedidos])

@reportes_bp.route('/usuarios', methods=['GET'])
def reporte_usuarios():
    dao = DAOFactory.get_usuario_dao('mysql')
    usuarios = dao.get_all()
    return jsonify([{'id': u.id, 'nombre': u.nombre, 'email': u.email, 'rol': u.rol} for u in usuarios])

@reportes_bp.route('/logs', methods=['GET'])
def reporte_logs():
    dao = DAOFactory.get_log_transaccion_dao('postgres')
    logs = dao.get_all()
    return jsonify([{'id': l.id, 'usuario_id': l.usuario_id, 'accion': l.accion, 'fecha': l.fecha} for l in logs])
