class CategoriaDTO:
    def __init__(self, id, nombre, descripcion):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion

    @staticmethod
    def from_model(categoria):
        return CategoriaDTO(categoria.id, categoria.nombre, categoria.descripcion)
