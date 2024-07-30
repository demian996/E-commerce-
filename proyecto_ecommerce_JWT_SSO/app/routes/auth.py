# app/routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.dao.mysql_dao import UsuarioDAO
from werkzeug.security import check_password_hash, generate_password_hash
from config_access import generate_token, verify_token
from access_log import add_log  # Importar la función para agregar logs
from invalid_tokens import add_invalid_token  # Importar la función para invalidar tokens
import re

auth_bp = Blueprint('auth', __name__)

def validar_email(email):
    pattern = r'^[^@]+@[^@]+\.[^@]+$'
    return re.match(pattern, email) is not None

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        usuario = UsuarioDAO.get_by_email(email)

        if not validar_email(email):
            flash('Correo electrónico con formato no válido', 'danger')
            return redirect(url_for('auth.login'))

        if usuario and check_password_hash(usuario.contrasena, password):
            session['user_id'] = usuario.id
            session['user_name'] = usuario.nombre
            session['user_role'] = usuario.rol
            session['login_method'] = 'credenciales normales'
            flash('Inicio de sesión exitoso', 'success')
            add_log(usuario.id, 'credenciales')  # Registrar acceso con credenciales
            access_token = generate_token({'user_id': usuario.id, 'user_role': usuario.rol})

            # Redirigir según el rol del usuario
            if usuario.rol == 'cliente':
                return redirect(url_for('categorias_bp.listar_categorias', token=access_token))
            elif usuario.rol == 'administrador':
                return redirect(url_for('admin.home_admin', token=access_token))
        else:
            flash('Correo electrónico o contraseña incorrectos', 'danger')
    return render_template('login.html')

@auth_bp.route('/login_with_token', methods=['GET'])
def login_with_token():
    token = request.args.get('token')
    if token:
        data = verify_token(token)
        if data:
            session['user_id'] = data['user_id']
            session['user_role'] = data['user_role']
            session['login_method'] = 'token'
            flash('Inicio de sesión exitoso con token', 'success')
            add_log('TOKEN', 'token')  # Registrar acceso con token
            return redirect(url_for('admin.home_admin', token=token))
        else:
            flash('Token inválido', 'danger')
            return redirect(url_for('auth.login'))
    else:
        flash('Token no proporcionado', 'danger')
        return redirect(url_for('auth.login'))

@auth_bp.route('/advertencia', methods=['GET'])
def advertencia():
    token = request.args.get('token')
    return render_template('advertencia.html', token=token)

@auth_bp.route('/process_advertencia', methods=['POST'])
def process_advertencia():
    token = request.form.get('token')
    if token:
        data = verify_token(token)
        if data:
            session['user_id'] = data['user_id']
            session['user_role'] = data['user_role']
            session['login_method'] = 'token'
            add_log('TOKEN', 'token')  # Registrar acceso con token
            return redirect(url_for('admin.home_admin', token=token))
        else:
            flash('Token inválido', 'danger')
            return redirect(url_for('auth.login'))
    else:
        flash('Token no proporcionado', 'danger')
        return redirect(url_for('auth.login'))

@auth_bp.route('/redirect_to_ecommerce')
def redirect_to_ecommerce():
    token = request.args.get('token')
    if token:
        return redirect(f'http://localhost:5001/protected?token={token}')
    else:
        flash('Token no proporcionado', 'danger')
        return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
def logout():
    token = request.args.get('token')
    if token:
        add_invalid_token(token)  # Invalida el token
    session.clear()
    flash('Has cerrado sesión', 'success')
    return redirect(url_for('main.home'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        contrasena = generate_password_hash(request.form['contrasena'])

        if not validar_email(email):
            flash('Correo electrónico con formato no válido', 'danger')
            return redirect(url_for('auth.register'))

        rol = 'cliente'  # Por defecto, todos los nuevos usuarios son clientes
        usuario = UsuarioDAO.create(nombre, email, contrasena, rol)
        flash('Registro exitoso', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/protected', methods=['GET'])
def protected():
    token = request.args.get('token')
    if token:
        data = verify_token(token)
        if data:
            return jsonify(logged_in_as=data), 200
        else:
            return jsonify(error='Token inválido'), 401
    else:
        return jsonify(error='Token no proporcionado'), 400
