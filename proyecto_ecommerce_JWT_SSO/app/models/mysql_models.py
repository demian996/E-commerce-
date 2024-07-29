from app import db

class Categoria(db.Model):
    __bind_key__ = 'mysql'
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)

class Producto(db.Model):
    __bind_key__ = 'mysql'
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))

class Usuario(db.Model):
    __bind_key__ = 'mysql'
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('cliente', 'administrador', name='roles'), nullable=False)
