class UsuarioDTO:
    def __init__(self, id, nombre, email, contrasena, rol):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.contrasena = contrasena
        self.rol = rol

    @classmethod
    def from_model(cls, model):
        return cls(
            id=model.id,
            nombre=model.nombre,
            email=model.email,
            contrasena=model.contrasena,
            rol=model.rol
        )
