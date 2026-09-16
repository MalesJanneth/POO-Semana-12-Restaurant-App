from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class Restaurante:
    """
    Gestiona las colecciones principales del restaurante y utiliza
    estructuras auxiliares para mejorar las búsquedas y consultas.
    """

    def __init__(self) -> None:
        # Colecciones principales.
        # Se mantienen como listas porque permiten almacenar, recorrer
        # y persistir los objetos.
        self._productos: list[Producto] = []
        self._usuarios: list[Usuario] = []
        self._ventas: list[Venta] = []

        # Índices auxiliares para búsquedas frecuentes.
        self._productos_por_codigo: dict[str, Producto] = {}
        self._usuarios_por_identificacion: dict[str, Usuario] = {}

        # Índice agrupado para consultar las ventas de un usuario
        # sin recorrer toda la colección de ventas.
        self._ventas_por_usuario: dict[str, list[Venta]] = {}

    # =========================================================
    # PRODUCTOS
    # =========================================================

    def registrar_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int,
        disponible: bool = True,
    ) -> Producto:

        # Se consulta el índice en lugar de recorrer la lista.
        if codigo in self._productos_por_codigo:
            raise ValueError("Ya existe un producto con ese código.")

        producto = Producto(
            codigo,
            nombre,
            categoria,
            precio,
            stock,
            disponible,
        )

        # Se actualizan la colección principal y el índice.
        self._productos.append(producto)
        self._productos_por_codigo[codigo] = producto

        return producto

    def buscar_producto(
        self,
        codigo: str,
    ) -> Producto | None:
        """
        Busca un producto directamente mediante el índice por código.
        """
        return self._productos_por_codigo.get(codigo)

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

        # Búsqueda mediante el índice.
        producto = self._productos_por_codigo.get(codigo_actual)

        if producto is None:
            raise ValueError(
                "No existe un producto con ese código."
            )

        # Se verifica que el nuevo código no pertenezca a otro producto.
        if (
            codigo != codigo_actual
            and codigo in self._productos_por_codigo
        ):
            raise ValueError(
                "Ya existe un producto con el nuevo código."
            )

        # Si cambia el código, se actualiza el código utilizado
        # en las ventas existentes para mantener la relación.
        if codigo != codigo_actual:
            for venta in self._ventas:
                if venta.producto_codigo == codigo_actual:
                    venta.producto_codigo = codigo

        # Se actualiza el mismo objeto en lugar de crear otro.
        producto.codigo = codigo
        producto.nombre = nombre
        producto.categoria = categoria
        producto.precio = precio
        producto.stock = stock
        producto.disponible = disponible

        # Se sincroniza el índice de productos.
        if codigo != codigo_actual:
            del self._productos_por_codigo[codigo_actual]
            self._productos_por_codigo[codigo] = producto

        return producto

    def eliminar_producto(
        self,
        codigo: str,
    ) -> Producto:

        # Búsqueda mediante el índice.
        producto = self._productos_por_codigo.get(codigo)

        if producto is None:
            raise ValueError(
                "No existe un producto con ese código."
            )

        # Se elimina de la colección principal.
        self._productos.remove(producto)

        # Se elimina del índice.
        del self._productos_por_codigo[codigo]

        return producto

    def listar_productos(self) -> list[Producto]:
        return list(self._productos)

    def obtener_productos(self) -> list[Producto]:
        return list(self._productos)

    def obtener_categorias(self) -> set[str]:
        """
        Utiliza un set porque las categorías no deben repetirse.
        """
        return {
            producto.categoria
            for producto in self._productos
        }

    # =========================================================
    # USUARIOS
    # =========================================================

    def registrar_usuario(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
    ) -> Usuario:

        # Validación mediante el índice.
        if identificacion in self._usuarios_por_identificacion:
            raise ValueError(
                "Ya existe un usuario con esa identificación."
            )

        usuario = Usuario(
            identificacion,
            nombre,
            correo,
        )

        # Se actualizan la colección principal y el índice.
        self._usuarios.append(usuario)
        self._usuarios_por_identificacion[
            identificacion
        ] = usuario

        return usuario

    def buscar_usuario(
        self,
        identificacion: str,
    ) -> Usuario | None:
        """
        Busca un usuario directamente mediante el índice.
        """
        return self._usuarios_por_identificacion.get(
            identificacion
        )

    def listar_usuarios(self) -> list[Usuario]:
        return list(self._usuarios)

    def obtener_usuarios(self) -> list[Usuario]:
        return list(self._usuarios)

    # =========================================================
    # VENTAS
    # =========================================================

    def vender_producto(
        self,
        identificacion_usuario: str,
        codigo_producto: str,
        cantidad: int,
    ) -> Venta:

        # Búsqueda del usuario mediante el índice.
        usuario = self._usuarios_por_identificacion.get(
            identificacion_usuario
        )

        if usuario is None:
            raise ValueError(
                "No existe un usuario con esa identificación."
            )

        # Búsqueda del producto mediante el índice.
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

        # Se crea la venta como objeto.
        venta = Venta(
            usuario.identificacion,
            producto.codigo,
            cantidad,
        )

        # Se actualiza la colección principal de ventas.
        self._ventas.append(venta)

        # Se actualiza el índice de ventas por usuario.
        ventas_usuario = self._ventas_por_usuario.setdefault(
            usuario.identificacion,
            []
        )

        ventas_usuario.append(venta)

        # Se actualiza el stock del producto.
        producto.vender(cantidad)

        return venta

    def obtener_ventas(self) -> list[Venta]:
        return list(self._ventas)

    def consultar_ventas_usuario(
        self,
        identificacion_usuario: str,
    ) -> list[Venta]:
        """
        Consulta las ventas utilizando el índice agrupado por usuario.
        De esta manera no es necesario recorrer toda la lista de ventas.
        """
        return list(
            self._ventas_por_usuario.get(
                identificacion_usuario,
                [],
            )
        )

    # =========================================================
    # CARGA Y RECONSTRUCCIÓN DE ÍNDICES
    # =========================================================

    def cargar_productos(
        self,
        productos: list[Producto],
    ) -> None:
        """
        Carga los productos recuperados desde JSON y reconstruye
        el índice de productos por código.
        """
        self._productos = list(productos)

        self._productos_por_codigo = {
            producto.codigo: producto
            for producto in self._productos
        }

    def cargar_usuarios(
        self,
        usuarios: list[Usuario],
    ) -> None:
        """
        Carga los usuarios recuperados desde JSON y reconstruye
        el índice de usuarios por identificación.
        """
        self._usuarios = list(usuarios)

        self._usuarios_por_identificacion = {
            usuario.identificacion: usuario
            for usuario in self._usuarios
        }

    def cargar_ventas(
        self,
        ventas: list[Venta],
    ) -> None:
        """
        Carga las ventas recuperadas desde JSON y reconstruye
        el índice agrupado por usuario.
        """
        self._ventas = list(ventas)

        self._ventas_por_usuario = {}

        for venta in self._ventas:
            ventas_usuario = self._ventas_por_usuario.setdefault(
                venta.usuario_id,
                []
            )

            ventas_usuario.append(venta)

    # =========================================================
    # MÉTODOS INTERNOS DE BÚSQUEDA
    # =========================================================

    def _buscar_producto_por_codigo(
        self,
        codigo: str,
    ) -> Producto | None:
        return self._productos_por_codigo.get(codigo)

    def _buscar_usuario_por_identificacion(
        self,
        identificacion: str,
    ) -> Usuario | None:
        return self._usuarios_por_identificacion.get(
            identificacion
        )