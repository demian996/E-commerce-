from app.models.mysql_models import Categoria, Producto, Usuario
from app.dto.categoria_dto import CategoriaDTO
from app.dto.producto_dto import ProductoDTO
from app.dto.usuario_dto import UsuarioDTO
from app import db

class CategoriaDAO:
    @staticmethod
    def get_all():
        categorias = Categoria.query.all()
        return [CategoriaDTO.from_model(c) for c in categorias]

    @staticmethod
    def get_by_id(categoria_id):
        categoria = Categoria.query.get(categoria_id)
        return CategoriaDTO.from_model(categoria) if categoria else None

    @staticmethod
    def create(nombre, descripcion):
        nueva_categoria = Categoria(nombre=nombre, descripcion=descripcion)
        db.session.add(nueva_categoria)
        db.session.commit()
        return CategoriaDTO.from_model(nueva_categoria)

    @staticmethod
    def update(categoria_id, nombre, descripcion):
        categoria = Categoria.query.get(categoria_id)
        if categoria:
            categoria.nombre = nombre
            categoria.descripcion = descripcion
            db.session.commit()
            return CategoriaDTO.from_model(categoria)
        return None

    @staticmethod
    def delete(categoria_id):
        categoria = Categoria.query.get(categoria_id)
        if categoria:
            db.session.delete(categoria)
            db.session.commit()
            return CategoriaDTO.from_model(categoria)
        return None

class ProductoDAO:
    @staticmethod
    def get_by_categoria_id(categoria_id):
        productos = Producto.query.filter_by(categoria_id=categoria_id).all()
        return [ProductoDTO.from_model(p) for p in productos]
    @staticmethod
    def get_all():
        productos = Producto.query.all()
        return [ProductoDTO.from_model(p) for p in productos]


    @staticmethod
    def get_by_id(producto_id):
        producto = Producto.query.get(producto_id)
        return ProductoDTO.from_model(producto) if producto else None

    @staticmethod
    def create(nombre, descripcion, precio, categoria_id):
        nuevo_producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, categoria_id=categoria_id)
        db.session.add(nuevo_producto)
        db.session.commit()
        return ProductoDTO.from_model(nuevo_producto)

    @staticmethod
    def update(producto_id, nombre, descripcion, precio, categoria_id):
        producto = Producto.query.get(producto_id)
        if producto:
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.precio = precio
            producto.categoria_id = categoria_id
            db.session.commit()
            return ProductoDTO.from_model(producto)
        return None

    @staticmethod
    def delete(producto_id):
        producto = Producto.query.get(producto_id)
        if producto:
            db.session.delete(producto)
            db.session.commit()
            return ProductoDTO.from_model(producto)
        return None



class UsuarioDAO:
    @staticmethod
    def get_all():
        usuarios = Usuario.query.all()
        return [UsuarioDTO.from_model(u) for u in usuarios]

    @staticmethod
    def get_by_id(usuario_id):
        usuario = Usuario.query.get(usuario_id)
        return UsuarioDTO.from_model(usuario) if usuario else None

    @staticmethod
    def get_by_email(email):
        usuario = Usuario.query.filter_by(email=email).first()
        return UsuarioDTO.from_model(usuario) if usuario else None

    @staticmethod
    def create(nombre, email, contrasena, rol):
        nuevo_usuario = Usuario(nombre=nombre, email=email, contrasena=contrasena, rol=rol)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return UsuarioDTO.from_model(nuevo_usuario)

    @staticmethod
    def update(usuario_id, nombre, email, contrasena, rol):
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            usuario.nombre = nombre
            usuario.email = email
            usuario.contrasena = contrasena
            usuario.rol = rol
            db.session.commit()
            return UsuarioDTO.from_model(usuario)
        return None

    @staticmethod
    def delete(usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return UsuarioDTO.from_model(usuario)
        return None

