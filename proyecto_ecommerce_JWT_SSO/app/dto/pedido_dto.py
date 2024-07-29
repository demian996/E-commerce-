class PedidoDTO:
    def __init__(self, id, usuario_id, fecha, total, estado):
        self.id = id
        self.usuario_id = usuario_id
        self.fecha = fecha
        self.total = total
        self.estado = estado

    @staticmethod
    def from_model(pedido):
        return PedidoDTO(pedido.id, pedido.usuario_id, pedido.fecha, pedido.total, pedido.estado)
