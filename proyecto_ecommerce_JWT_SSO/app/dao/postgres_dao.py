from datetime import datetime
from app import db
from app.dto.log_transaccion_dto import LogTransaccionDTO
from sqlalchemy.sql import text

class PostgreSQLLogsDAO:
    def __init__(self, app):
        self.app = app

    def registrar_transaccion(self, log_dto):
        try:
            # Mensajes de depuración para verificar los datos antes de la inserción
            print(f"Debug: Registrando transacción:")
            print(f"Debug: Usuario ID: {log_dto.usuario_id}")
            print(f"Debug: Acción: {log_dto.accion}")
            print(f"Debug: Fecha: {datetime.now()}")

            engine = db.get_engine(self.app, bind='postgres')
            with engine.connect() as connection:
                trans = connection.begin()  # Inicia una transacción
                try:
                    connection.execute(
                        text("INSERT INTO logs_transacciones (usuario_id, accion, fecha) VALUES (:usuario_id, :accion, :fecha)"),
                        {'usuario_id': log_dto.usuario_id, 'accion': log_dto.accion, 'fecha': datetime.now()}
                    )
                    trans.commit()  # Comete la transacción
                    print("Debug: Transacción registrada exitosamente")
                except Exception as e:
                    trans.rollback()  # Revertir la transacción en caso de error
                    print(f"Error al registrar transacción: {e}")
                    return False
            return True
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            return False

    def get_all(self):
        try:
            engine = db.get_engine(self.app, bind='postgres')
            with engine.connect() as connection:
                result = connection.execute(text("SELECT * FROM logs_transacciones")).fetchall()
            return result
        except Exception as e:
            print(f"Error al obtener logs: {e}")
            return []
