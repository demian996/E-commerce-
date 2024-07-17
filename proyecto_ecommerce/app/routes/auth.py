from flask import Blueprint, jsonify,  render_template, request, redirect, url_for, flash, session
from app.dao.mysql_dao import UsuarioDAO
from werkzeug.security import check_password_hash, generate_password_hash
from app.factories.dao_factory import DAOFactory
import re
auth_bp = Blueprint('auth', __name__)


def validar_email(email):
    # @._
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
            return redirect(url_for('auth.register'))

        if usuario and check_password_hash(usuario.contrasena, password):
            session['user_id'] = usuario.id
            session['user_name'] = usuario.nombre
            session['user_role'] = usuario.rol
            flash('Inicio de sesión exitoso', 'success')
            if usuario.rol == 'cliente':
                return redirect(url_for('categorias_bp.listar_categorias'))
            elif usuario.rol == 'administrador':
                return redirect(url_for('main.home_admin'))
        else:
            flash('Correo electrónico o contraseña incorrectos', 'danger')
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
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