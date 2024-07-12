class DetallePedidoDTO:
    def __init__(self, id, pedido_id, producto_id, cantidad, precio_unitario):
        self.id = id
        self.pedido_id = pedido_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario

    @staticmethod
    def from_model(detalle_pedido):
        return DetallePedidoDTO(detalle_pedido.id, detalle_pedido.pedido_id, detalle_pedido.producto_id, detalle_pedido.cantidad, detalle_pedido.precio_unitario)
