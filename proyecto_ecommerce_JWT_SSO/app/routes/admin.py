# app/routes/admin.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from app.services.log_service import LogService
from app.factories.dao_factory import DAOFactory
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from config_access import verify_token
from invalid_tokens import is_token_invalid  # Importar la función para verificar tokens inválidos
import functools

admin_bp = Blueprint('admin', __name__)

log_service = LogService(current_app)

# Middleware para verificar token
def token_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        token = request.args.get('token')
        if not token:
            flash('Token no proporcionado', 'danger')
            return redirect(url_for('auth.login'))
        if is_token_invalid(token):
            flash('Token inválido o expirado', 'danger')
            return redirect(url_for('auth.login'))
        data = verify_token(token)
        if data is None:
            flash('Token inválido o expirado', 'danger')
            return redirect(url_for('auth.login'))
        session['user_id'] = data['user_id']
        session['user_role'] = data['user_role']
        return view(token=token, **kwargs)
    return wrapped_view

# Rutas protegidas con el middleware `token_required`
@admin_bp.route('/home_admin')
@token_required
def home_admin(token):
    return render_template('home_admin.html', token=token)

# Gestión de Categorías
@admin_bp.route('/categorias', methods=['GET', 'POST'])
@token_required
def gestionar_categorias(token):
    dao = DAOFactory.get_categoria_dao('mysql')

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        dao.create(nombre, descripcion)
        flash('Categoría agregada exitosamente', 'success')

        # Registrar transacción
        usuario_id = session.get('user_id')
        if usuario_id:
            log_service.registrar_transaccion(usuario_id, f'creó una nueva categoría: {nombre}')

        return redirect(url_for('admin.gestionar_categorias', token=token))

    categorias = dao.get_all()
    return render_template('admin/categorias.html', categorias=categorias, token=token)

@admin_bp.route('/categorias/editar/<int:id>', methods=['GET', 'POST'])
@token_required
def editar_categoria(id, token):
    dao = DAOFactory.get_categoria_dao('mysql')
    categoria = dao.get_by_id(id)

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        dao.update(id, nombre, descripcion)
        flash('Categoría actualizada exitosamente', 'success')

        # Registrar transacción
        usuario_id = session.get('user_id')
        if usuario_id:
            log_service.registrar_transaccion(usuario_id, f'editó la categoría: {nombre}')

        return redirect(url_for('admin.gestionar_categorias', token=token))

    return render_template('admin/editar_categoria.html', categoria=categoria, token=token)

@admin_bp.route('/categorias/eliminar/<int:id>', methods=['POST'])
@token_required
def eliminar_categoria(id, token):
    dao = DAOFactory.get_categoria_dao('mysql')
    categoria = dao.get_by_id(id)
    try:
        dao.delete(id)
        flash('Categoría eliminada exitosamente', 'success')

        # Registrar transacción
        usuario_id = session.get('user_id')
        if usuario_id:
            log_service.registrar_transaccion(usuario_id, f'eliminó la categoría: {categoria.nombre}')

    except IntegrityError:
        flash('No se puede eliminar la categoría porque hay productos asociados a ella.', 'danger')

    return redirect(url_for('admin.gestionar_categorias', token=token))

# Gestión de Productos
@admin_bp.route('/productos', methods=['GET', 'POST'])
@token_required
def gestionar_productos(token):
    dao = DAOFactory.get_producto_dao('mysql')

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        categoria_id = request.form['categoria_id']
        dao.create(nombre, descripcion, precio, categoria_id)
        flash('Producto agregado exitosamente', 'success')

        # Registrar transacción
        usuario_id = session.get('user_id')
        if usuario_id:
            log_service.registrar_transaccion(usuario_id, f'creó un nuevo producto: {nombre}')

        return redirect(url_for('admin.gestionar_productos', token=token))

    productos = dao.get_all()
    categorias = DAOFactory.get_categoria_dao('mysql').get_all()  # Para el formulario de agregar/editar productos
    return render_template('admin/productos.html', productos=productos, categorias=categorias, token=token)

@admin_bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@token_required
def editar_producto(id, token):
    dao = DAOFactory.get_producto_dao('mysql')
    producto = dao.get_by_id(id)

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        categoria_id = request.form['categoria_id']
        dao.update(id, nombre, descripcion, precio, categoria_id)
        flash('Producto actualizado exitosamente', 'success')

        # Registrar transacción
        usuario_id = session.get('user_id')
        if usuario_id:
            log_service.registrar_transaccion(usuario_id, f'editó el producto: {nombre}')

        return redirect(url_for('admin.gestionar_productos', token=token))

    categorias = DAOFactory.get_categoria_dao('mysql').get_all()
    return render_template('admin/editar_producto.html', producto=producto, categorias=categorias, token=token)

@admin_bp.route('/productos/eliminar/<int:id>', methods=['POST'])
@token_required
def eliminar_producto(id, token):
    dao = DAOFactory.get_producto_dao('mysql')
    producto = dao.get_by_id(id)

    try:
        dao.delete(id)
        flash('Producto eliminado exitosamente', 'success')

        # Registrar transacción
        usuario_id = session.get('user_id')
        if usuario_id:
            log_service.registrar_transaccion(usuario_id, f'eliminó el producto: {producto.nombre}')

    except IntegrityError:
        flash('No se puede eliminar el producto porque está asociado a otras entidades.', 'danger')

    return redirect(url_for('admin.gestionar_productos', token=token))

# Gestión de Usuarios
@admin_bp.route('/usuarios', methods=['GET', 'POST'])
@token_required
def gestionar_usuarios(token):
    dao = DAOFactory.get_usuario_dao('mysql')

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        contrasena = request.form['contrasena']
        rol = request.form['rol']
        contrasena_hash = generate_password_hash(contrasena)
        dao.create(nombre, email, contrasena_hash, rol)
        flash('Usuario agregado exitosamente', 'success')

        # Registrar transacción
        usuario_id = session.get('user_id')
        if usuario_id:
            log_service.registrar_transaccion(usuario_id, f'creó un nuevo usuario: {nombre}')

        return redirect(url_for('admin.gestionar_usuarios', token=token))

    usuarios = dao.get_all()
    return render_template('admin/usuarios.html', usuarios=usuarios, token=token)

@admin_bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@token_required
def editar_usuario(id, token):
    dao = DAOFactory.get_usuario_dao('mysql')
    usuario = dao.get_by_id(id)

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        contrasena = request.form['contrasena']
        rol = request.form['rol']
        if contrasena:  # Solo hashear si se proporciona una nueva contraseña
            contrasena_hash = generate_password_hash(contrasena)
        else:
            contrasena_hash = usuario.contrasena  # Mantener la contraseña existente si no se proporciona una nueva
        dao.update(id, nombre, email, contrasena_hash, rol)
        flash('Usuario actualizado exitosamente', 'success')

        # Registrar transacción
        usuario_id = session.get('user_id')
        if usuario_id:
            log_service.registrar_transaccion(usuario_id, f'editó el usuario: {nombre}')

        return redirect(url_for('admin.gestionar_usuarios', token=token))

    return render_template('admin/editar_usuario.html', usuario=usuario, token=token)

@admin_bp.route('/usuarios/eliminar/<int:id>', methods=['POST'])
@token_required
def eliminar_usuario(id, token):
    dao = DAOFactory.get_usuario_dao('mysql')
    usuario = dao.get_by_id(id)
    dao.delete(id)
    flash('Usuario eliminado exitosamente', 'success')

    # Registrar transacción
    usuario_id = session.get('user_id')
    if usuario_id:
        log_service.registrar_transaccion(usuario_id, f'eliminó el usuario: {usuario.nombre}')

    return redirect(url_for('admin.gestionar_usuarios', token=token))

# Ver Logs de Transacciones
@admin_bp.route('/logs', methods=['GET'])
@token_required
def ver_logs_transacciones(token):
    logs = log_service.obtener_logs_con_nombres()
    return render_template('admin_logs.html', logs=logs, token=token)
