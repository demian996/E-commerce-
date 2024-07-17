# app/routes/admin.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from app.services.log_service import LogService
from app.factories.dao_factory import DAOFactory
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

admin_bp = Blueprint('admin', __name__)

log_service = LogService(current_app)

# Gestión de Categorías
@admin_bp.route('/admin/categorias', methods=['GET', 'POST'])
def gestionar_categorias():
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

        return redirect(url_for('admin.gestionar_categorias'))

    categorias = dao.get_all()
    return render_template('admin/categorias.html', categorias=categorias)

@admin_bp.route('/admin/categorias/editar/<int:id>', methods=['GET', 'POST'])
def editar_categoria(id):
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

        return redirect(url_for('admin.gestionar_categorias'))

    return render_template('admin/editar_categoria.html', categoria=categoria)

@admin_bp.route('/admin/categorias/eliminar/<int:id>', methods=['POST'])
def eliminar_categoria(id):
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

    return redirect(url_for('admin.gestionar_categorias'))

# Gestión de Productos
@admin_bp.route('/admin/productos', methods=['GET', 'POST'])
def gestionar_productos():
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

        return redirect(url_for('admin.gestionar_productos'))

    productos = dao.get_all()
    categorias = DAOFactory.get_categoria_dao('mysql').get_all()  # Para el formulario de agregar/editar productos
    return render_template('admin/productos.html', productos=productos, categorias=categorias)

@admin_bp.route('/admin/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
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

        return redirect(url_for('admin.gestionar_productos'))

    categorias = DAOFactory.get_categoria_dao('mysql').get_all()
    return render_template('admin/editar_producto.html', producto=producto, categorias=categorias)

@admin_bp.route('/admin/productos/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
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

    return redirect(url_for('admin.gestionar_productos'))

# Gestión de Usuarios
@admin_bp.route('/admin/usuarios', methods=['GET', 'POST'])
def gestionar_usuarios():
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

        return redirect(url_for('admin.gestionar_usuarios'))

    usuarios = dao.get_all()
    return render_template('admin/usuarios.html', usuarios=usuarios)

@admin_bp.route('/admin/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
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

        return redirect(url_for('admin.gestionar_usuarios'))

    return render_template('admin/editar_usuario.html', usuario=usuario)

@admin_bp.route('/admin/usuarios/eliminar/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    dao = DAOFactory.get_usuario_dao('mysql')
    usuario = dao.get_by_id(id)
    dao.delete(id)
    flash('Usuario eliminado exitosamente', 'success')

    # Registrar transacción
    usuario_id = session.get('user_id')
    if usuario_id:
        log_service.registrar_transaccion(usuario_id, f'eliminó el usuario: {usuario.nombre}')

    return redirect(url_for('admin.gestionar_usuarios'))

# Ver Logs de Transacciones
@admin_bp.route('/admin/logs', methods=['GET'])
def ver_logs_transacciones():
    logs = log_service.obtener_logs_con_nombres()
    return render_template('admin_logs.html', logs=logs)
