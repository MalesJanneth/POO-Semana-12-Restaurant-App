from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class Restaurante:
    """
    Gestiona las colecciones principales del restaurante y utiliza
    estructuras auxiliares para mejorar las búsquedas y consultas.
    """

    def __init__(self) -> None:
        self._productos: list[Producto] = []
        self._usuarios: list[Usuario] = []
        self._ventas: list[Venta] = []

        self._productos_por_codigo: dict[str, Producto] = {}
        self._usuarios_por_identificacion: dict[str, Usuario] = {}
        self._ventas_por_usuario: dict[str, list[Venta]] = {}
        self._categorias: set[str] = set()

    def _reconstruir_indices(self) -> None:
        """
        Reconstruye las estructuras auxiliares a partir de las
        colecciones principales.
        """
        self._productos_por_codigo = {
            producto.codigo: producto
            for producto in self._productos
        }

        self._usuarios_por_identificacion = {
            usuario.identificacion: usuario
            for usuario in self._usuarios
        }

        self._ventas_por_usuario = {}

        for venta in self._ventas:
            self._ventas_por_usuario.setdefault(
                venta.usuario_id,
                []
            ).append(venta)

        self._categorias = {
            producto.categoria
            for producto in self._productos
        }

    # PRODUCTOS

    def registrar_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int,
        disponible: bool = True,
    ) -> Producto:

        if codigo in self._productos_por_codigo:
            raise ValueError(
                "Ya existe un producto con ese código."
            )

        producto = Producto(
            codigo,
            nombre,
            categoria,
            precio,
            stock,
            disponible,
        )

        self._productos.append(producto)
        self._productos_por_codigo[codigo] = producto
        self._categorias.add(categoria)

        return producto

    def buscar_producto(
        self,
        codigo: str,
    ) -> Producto | None:
        return self._productos_por_codigo.get(codigo)

    def listar_productos(self) -> list[Producto]:
        return list(self._productos)

    def actualizar_producto(
        self,
        codigo_actual: str,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int,
        disponible: bool = True,
    ) -> Producto:

        producto = self._productos_por_codigo.get(codigo_actual)

        if producto is None:
            raise ValueError(
                "No existe un producto con ese código."
            )

        if (
            codigo != codigo_actual
            and codigo in self._productos_por_codigo
        ):
            raise ValueError(
                "Ya existe un producto con el nuevo código."
            )

        if codigo != codigo_actual:
            for venta in self._ventas:
                if venta.producto_codigo == codigo_actual:
                    venta.producto_codigo = codigo

        producto.codigo = codigo
        producto.nombre = nombre
        producto.categoria = categoria
        producto.precio = precio
        producto.stock = stock
        producto.disponible = disponible

        if codigo != codigo_actual:
            del self._productos_por_codigo[codigo_actual]
            self._productos_por_codigo[codigo] = producto

        self._categorias = {
            producto.categoria
            for producto in self._productos
        }

        return producto

    def eliminar_producto(
        self,
        codigo: str,
    ) -> Producto:

        producto = self._productos_por_codigo.get(codigo)

        if producto is None:
            raise ValueError(
                "No existe un producto con ese código."
            )

        self._productos.remove(producto)
        del self._productos_por_codigo[codigo]

        self._categorias = {
            producto.categoria
            for producto in self._productos
        }

        return producto

    def obtener_categorias(self) -> set[str]:
        return set(self._categorias)

    # USUARIOS

    def registrar_usuario(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
    ) -> Usuario:

        if identificacion in self._usuarios_por_identificacion:
            raise ValueError(
                "Ya existe un usuario con esa identificación."
            )

        usuario = Usuario(
            identificacion,
            nombre,
            correo,
        )

        self._usuarios.append(usuario)
        self._usuarios_por_identificacion[
            identificacion
        ] = usuario

        return usuario

    def buscar_usuario(
        self,
        identificacion: str,
    ) -> Usuario | None:
        return self._usuarios_por_identificacion.get(
            identificacion
        )

    def listar_usuarios(self) -> list[Usuario]:
        return list(self._usuarios)

    def actualizar_usuario(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
    ) -> Usuario:

        usuario = self._usuarios_por_identificacion.get(
            identificacion
        )

        if usuario is None:
            raise ValueError(
                "No existe un usuario con esa identificación."
            )

        usuario.nombre = nombre
        usuario.correo = correo

        return usuario

    def eliminar_usuario(
        self,
        identificacion: str,
    ) -> Usuario:

        usuario = self._usuarios_por_identificacion.get(
            identificacion
        )

        if usuario is None:
            raise ValueError(
                "No existe un usuario con esa identificación."
            )

        self._usuarios.remove(usuario)
        del self._usuarios_por_identificacion[
            identificacion
        ]

        return usuario

    # VENTAS

    def registrar_venta(
        self,
        identificacion_usuario: str,
        codigo_producto: str,
        cantidad: int,
    ) -> Venta:

        usuario = self._usuarios_por_identificacion.get(
            identificacion_usuario
        )

        if usuario is None:
            raise ValueError(
                "No existe un usuario con esa identificación."
            )

        producto = self._productos_por_codigo.get(
            codigo_producto
        )

        if producto is None:
            raise ValueError(
                "No existe un producto con ese código."
            )

        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError(
                "La cantidad debe ser un entero mayor que cero."
            )

        if producto.stock < cantidad:
            raise ValueError(
                "No existe suficiente stock disponible."
            )

        venta = Venta(
            usuario.identificacion,
            producto.codigo,
            cantidad,
        )

        self._ventas.append(venta)

        self._ventas_por_usuario.setdefault(
            usuario.identificacion,
            []
        ).append(venta)

        producto.vender(cantidad)

        return venta

    def vender_producto(
        self,
        identificacion_usuario: str,
        codigo_producto: str,
        cantidad: int,
    ) -> Venta:
        return self.registrar_venta(
            identificacion_usuario,
            codigo_producto,
            cantidad,
        )

    def consultar_ventas_usuario(
        self,
        identificacion_usuario: str,
    ) -> list[Venta]:
        return list(
            self._ventas_por_usuario.get(
                identificacion_usuario,
                [],
            )
        )

    def listar_ventas(self) -> list[Venta]:
        return list(self._ventas)

    # CARGA DE DATOS Y RECONSTRUCCIÓN

    def cargar_productos(
        self,
        productos: list[Producto],
    ) -> None:
        self._productos = list(productos)
        self._reconstruir_indices()

    def cargar_usuarios(
        self,
        usuarios: list[Usuario],
    ) -> None:
        self._usuarios = list(usuarios)
        self._reconstruir_indices()

    def cargar_ventas(
        self,
        ventas: list[Venta],
    ) -> None:
        self._ventas = list(ventas)
        self._reconstruir_indices()