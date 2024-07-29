from flask import Blueprint, jsonify, request, session, flash, redirect, url_for
from app.factories.dao_factory import DAOFactory
from config_access import verify_token
import functools

reportes_bp = Blueprint('reportes', __name__)

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

@reportes_bp.route('/categorias', methods=['GET'])
@token_required
def reporte_categorias():
    dao = DAOFactory.get_categoria_dao('mysql')
    categorias = dao.get_all()
    return jsonify([{'id': c.id, 'nombre': c.nombre, 'descripcion': c.descripcion} for c in categorias])

@reportes_bp.route('/pedidos', methods=['GET'])
@token_required
def reporte_pedidos():
    dao = DAOFactory.get_pedido_dao('postgres')
    pedidos = dao.get_all()
    return jsonify([{'id': p.id, 'usuario_id': p.usuario_id, 'fecha': p.fecha, 'total': p.total, 'estado': p.estado} for p in pedidos])

@reportes_bp.route('/usuarios', methods=['GET'])
@token_required
def reporte_usuarios():
    dao = DAOFactory.get_usuario_dao('mysql')
    usuarios = dao.get_all()
    return jsonify([{'id': u.id, 'nombre': u.nombre, 'email': u.email, 'rol': u.rol} for u in usuarios])

@reportes_bp.route('/logs', methods=['GET'])
@token_required
def reporte_logs():
    dao = DAOFactory.get_log_transaccion_dao('postgres')
    logs = dao.get_all()
    return jsonify([{'id': l.id, 'usuario_id': l.usuario_id, 'accion': l.accion, 'fecha': l.fecha} for l in logs])
