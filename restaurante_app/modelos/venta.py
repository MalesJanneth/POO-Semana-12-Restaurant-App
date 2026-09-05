"""
Este módulo contiene la clase Venta.
La clase Venta representa la relación entre
un usuario y un producto vendido.
"""

class Venta:
    def __init__(
        self,
        usuario_id: str,
        producto_codigo: str,
        cantidad: int
    ):
        self.usuario_id = usuario_id
        self.producto_codigo = producto_codigo
        self.cantidad = cantidad

    @property
    def usuario_id(self):
        return self._usuario_id

    @usuario_id.setter
    def usuario_id(self, valor):
        if not valor or not isinstance(valor, str):
            raise ValueError(
                "La identificación del usuario es obligatoria."
            )
        self._usuario_id = valor

    @property
    def producto_codigo(self):
        return self._producto_codigo

    @producto_codigo.setter
    def producto_codigo(self, valor):
        if not valor or not isinstance(valor, str):
            raise ValueError(
                "El código del producto es obligatorio."
            )
        self._producto_codigo = valor

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError(
                "La cantidad debe ser un entero mayor que cero."
            )
        self._cantidad = valor

    def a_diccionario(self):
        return {
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "cantidad": self.cantidad
        }