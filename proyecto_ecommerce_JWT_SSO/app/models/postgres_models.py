from app import db

class Pedido(db.Model):
    __bind_key__ = 'postgres'
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())
    total = db.Column(db.Numeric(10, 2), nullable=False)
    estado = db.Column(db.String(50), nullable=False)

class DetallePedido(db.Model):
    __bind_key__ = 'postgres'
    __tablename__ = 'detalles_pedidos'
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    producto_id = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)

class LogTransaccion(db.Model):
    __bind_key__ = 'postgres'
    __tablename__ = 'logs_transacciones'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False)
    accion = db.Column(db.String(255), nullable=False)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())
