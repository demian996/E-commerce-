# log_transaccion_dto.py
class LogTransaccionDTO:
    def __init__(self, id, usuario_id, usuario_nombre, accion, fecha):
        self.id = id
        self.usuario_id = usuario_id
        self.usuario_nombre = usuario_nombre
        self.accion = accion
        self.fecha = fecha