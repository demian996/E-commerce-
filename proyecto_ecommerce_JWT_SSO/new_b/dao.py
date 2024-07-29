from werkzeug.security import generate_password_hash

class Usuario:
    def __init__(self, id, email, contrasena, rol):
        self.id = id
        self.email = email
        self.contrasena = contrasena
        self.rol = rol

class UsuarioDAO:
    @staticmethod
    def get_by_email(email):
        # Simulación de obtención de usuario por email. Debes reemplazar esto con la lógica real de acceso a la base de datos.
        if email == 'admin@example.com':
            contrasena_hash = generate_password_hash('admin')
            return Usuario(id=1, email=email, contrasena=contrasena_hash, rol='administrador')
        return None
