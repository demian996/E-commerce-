from app.dao.mysql_dao import CategoriaDAO as MySQLCategoriaDAO, ProductoDAO as MySQLProductoDAO, UsuarioDAO as MySQLUsuarioDAO
from app.dao.postgres_dao import PostgreSQLLogsDAO

class DAOFactory:
    @staticmethod
    def get_categoria_dao(db_type):
        if db_type == 'mysql':
            return MySQLCategoriaDAO()
        # Add logic for other databases if necessary

    @staticmethod
    def get_producto_dao(db_type):
        if db_type == 'mysql':
            return MySQLProductoDAO()
        # Add logic for other databases if necessary

    @staticmethod
    def get_usuario_dao(db_type):
        if db_type == 'mysql':
            return MySQLUsuarioDAO()
        # Add logic for other databases if necessary

    @staticmethod
    def get_logs_dao(db_type, app):
        if db_type == 'postgres':
            return PostgreSQLLogsDAO(app)
        # Add logic for other databases if necessary
