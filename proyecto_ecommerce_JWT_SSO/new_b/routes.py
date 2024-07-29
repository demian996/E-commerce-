import requests
from flask import Blueprint, jsonify, request, current_app, session, flash, redirect, url_for
import functools
from config_access import verify_token, create_access_token
from access_log import add_log

new_b_bp = Blueprint('new_b', __name__)

def token_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        token = request.args.get('token')
        if not token:
            flash('Token no proporcionado', 'danger')
            return redirect(url_for('auth_new_b.login'))
        data = verify_token(token)
        if data is None:
            flash('Token inválido o expirado', 'danger')
            return redirect(url_for('auth_new_b.login'))
        session['user_identity'] = data['user_id']
        add_log('TOKEN', 'token')
        return view(**kwargs)
    return wrapped_view

@new_b_bp.route('/access_ecommerce', methods=['GET'])
@token_required
def access_ecommerce():
    user_identity = session.get('user_identity')
    token = create_access_token({'user_id': user_identity, 'user_role': 'admin'})  # Asigna el rol adecuado

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get('http://ecommerce_app:5000/admin/home_admin', headers=headers)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'No se pudo acceder a ecommerce'}), response.status_code
