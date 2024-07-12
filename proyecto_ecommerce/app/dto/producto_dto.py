class ProductoDTO:
    def __init__(self, id, nombre, descripcion, precio, categoria_id):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.categoria_id = categoria_id

    @staticmethod
    def from_model(producto):
        return ProductoDTO(producto.id, producto.nombre, producto.descripcion, producto.precio, producto.categoria_id)
