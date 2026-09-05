class Producto:
    def __init__(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int,
        disponible: bool = True
    ):
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock
        self.disponible = disponible

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        if not valor or not isinstance(valor, str):
            raise ValueError("El código del producto es obligatorio.")
        self._codigo = valor

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not isinstance(valor, str):
            raise ValueError("El nombre del producto es obligatorio.")
        self._nombre = valor

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, valor):
        if not valor or not isinstance(valor, str):
            raise ValueError("La categoría del producto es obligatoria.")
        self._categoria = valor

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("El precio debe ser un número mayor o igual a cero.")
        self._precio = float(valor)

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        if not isinstance(valor, int) or valor < 0:
            raise ValueError("El stock debe ser un entero mayor o igual a cero.")
        self._stock = valor

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        if not isinstance(valor, bool):
            raise ValueError("La disponibilidad debe ser verdadera o falsa.")
        self._disponible = valor

    def vender(self, cantidad):
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero mayor que cero.")

        if cantidad > self.stock:
            raise ValueError("No hay suficiente stock disponible.")

        self.stock -= cantidad

        if self.stock == 0:
            self.disponible = False

    def mostrar_informacion(self):
        return (
            f"Código: {self.codigo} | "
            f"Nombre: {self.nombre} | "
            f"Categoría: {self.categoria} | "
            f"Precio: ${self.precio:.2f} | "
            f"Stock: {self.stock} | "
            f"Disponible: {self.disponible}"
        )

    def a_diccionario(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock,
            "disponible": self.disponible
        }