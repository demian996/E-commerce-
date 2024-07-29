# app/services/log_service.py
from app.factories.dao_factory import DAOFactory
from app.dto.log_transaccion_dto import LogTransaccionDTO

class LogService:
    def __init__(self, app):
        self.logs_dao = DAOFactory.get_logs_dao('postgres', app)
        self.usuarios_dao = DAOFactory.get_usuario_dao('mysql')

    def registrar_transaccion(self, usuario_id, accion):
        usuario = self.usuarios_dao.get_by_id(usuario_id)
        usuario_nombre = usuario.nombre if usuario else "Usuario no encontrado"
        mensaje = f'{usuario_nombre} {accion}'
        log_dto = LogTransaccionDTO(None, usuario_id, usuario_nombre, mensaje, None)
        return self.logs_dao.registrar_transaccion(log_dto)

    def obtener_logs_con_nombres(self):
        logs = self.logs_dao.get_all()
        logs_con_nombres = []
        for log in logs:
            usuario = self.usuarios_dao.get_by_id(log.usuario_id)
            usuario_nombre = usuario.nombre if usuario else "Usuario no encontrado"
            log_dto = LogTransaccionDTO(
                id=log.id,
                usuario_id=log.usuario_id,
                usuario_nombre=usuario_nombre,
                accion=log.accion,
                fecha=log.fecha
            )
            logs_con_nombres.append(log_dto)
        return logs_con_nombres
