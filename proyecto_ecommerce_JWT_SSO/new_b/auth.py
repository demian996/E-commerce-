from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from config_access import create_access_token, verify_token
from dao import UsuarioDAO
from access_log import add_log  # Importar el método para agregar logs
import re  # Importar el módulo re

auth_new_b_bp = Blueprint('auth_new_b', __name__)

def validar_email(email):
    pattern = r'^[^@]+@[^@]+\.[^@]+$'
    return re.match(pattern, email) is not None

@auth_new_b_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Correo electrónico y contraseña son requeridos', 'danger')
            return redirect(url_for('auth_new_b.login'))

        usuario = UsuarioDAO.get_by_email(email)

        if not validar_email(email):
            flash('Correo electrónico con formato no válido', 'danger')
            return redirect(url_for('auth_new_b.login'))

        if usuario:
            if check_password_hash(usuario.contrasena, password):
                session['user_id'] = usuario.id
                session['user_name'] = usuario.email
                session['user_role'] = usuario.rol
                session['login_method'] = 'credenciales normales'
                flash('Inicio de sesión exitoso', 'success')
                identity = {'user_id': usuario.id, 'user_role': usuario.rol}
                access_token = create_access_token(identity)
                add_log(usuario.id, 'credenciales')  # Registrar acceso con credenciales
                return redirect(url_for('index', token=access_token))
            else:
                flash('Contraseña incorrecta', 'danger')
        else:
            flash('Usuario no encontrado', 'danger')
    return render_template('login.html')
