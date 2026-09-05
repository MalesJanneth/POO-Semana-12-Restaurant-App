"""
Módulo que contiene la clase Restaurante.

Restaurante administra las colecciones principales de
productos, usuarios y ventas, utilizando diccionarios
como índices en memoria para optimizar las búsquedas
frecuentes.
"""

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class Restaurante:
    def __init__(self):
        # ========================================================
        # COLECCIONES PRINCIPALES
        # ========================================================

        # Las listas se mantienen como colecciones principales
        # para almacenar y recorrer los objetos del sistema.
        self._productos: list[Producto] = []
        self._usuarios: list[Usuario] = []
        self._ventas: list[Venta] = []

        # ========================================================
        # ÍNDICES EN MEMORIA
        # ========================================================

        # Índice de productos por código.
        # Permite realizar búsquedas directas mediante el código.
        self._productos_por_codigo: dict[str, Producto] = {}

        # Índice de usuarios por identificación.
        # Permite realizar búsquedas directas mediante la identificación.
        self._usuarios_por_identificacion: dict[str, Usuario] = {}

        # Índice de ventas agrupadas por usuario.
        # Evita recorrer toda la lista de ventas al consultar
        # las ventas de un usuario específico.
        self._ventas_por_usuario: dict[str, list[Venta]] = {}

    # ============================================================
    # PRODUCTOS
    # ============================================================

    def registrar_producto(self, producto: Producto) -> str:
        """
        Registra un producto.

        Se actualizan tanto la lista principal como
        el índice por código.
        """

        if self._buscar_producto_por_codigo(producto.codigo) is not None:
            raise ValueError(
                "Ya existe un producto con ese código."
            )

        # Colección principal
        self._productos.append(producto)

        # Índice
        self._productos_por_codigo[producto.codigo] = producto

        return "Producto registrado correctamente."

    def buscar_producto(
        self,
        codigo: str
    ) -> Producto | None:
        """
        Busca un producto utilizando el índice por código.

        La búsqueda mediante diccionario tiene una complejidad
        promedio O(1).
        """

        return self._buscar_producto_por_codigo(codigo)

    def actualizar_producto(
        self,
        codigo_actual: str,
        nuevo_codigo: str,
        nuevo_nombre: str,
        nueva_categoria: str,
        nuevo_precio: float,
        nuevo_stock: int,
        nueva_disponibilidad: bool = True
    ) -> str:
        """
        Actualiza los datos de un producto.

        Si cambia el código, también se actualiza el índice
        correspondiente para mantener la coherencia.
        """

        producto_actual = self._buscar_producto_por_codigo(
            codigo_actual
        )

        if producto_actual is None:
            raise ValueError(
                "No existe un producto con ese código."
            )

        # Si el código cambia, comprobar que el nuevo código
        # no pertenezca a otro producto.
        if nuevo_codigo != codigo_actual:

            producto_con_nuevo_codigo = (
                self._buscar_producto_por_codigo(
                    nuevo_codigo
                )
            )

            if producto_con_nuevo_codigo is not None:
                raise ValueError(
                    "Ya existe otro producto con el nuevo código."
                )

        # Crear objeto actualizado.
        producto_actualizado = Producto(
            codigo=nuevo_codigo,
            nombre=nuevo_nombre,
            categoria=nueva_categoria,
            precio=nuevo_precio,
            stock=nuevo_stock,
            disponible=nueva_disponibilidad
        )

        # Reemplazar en la lista principal.
        indice = self._productos.index(producto_actual)
        self._productos[indice] = producto_actualizado

        # ========================================================
        # ACTUALIZACIÓN DEL ÍNDICE
        # ========================================================

        del self._productos_por_codigo[codigo_actual]

        self._productos_por_codigo[nuevo_codigo] = (
            producto_actualizado
        )

        return "Producto actualizado correctamente."

    def eliminar_producto(self, codigo: str) -> str:
        """
        Elimina un producto de la lista principal
        y de su índice.
        """

        producto = self._buscar_producto_por_codigo(codigo)

        if producto is None:
            raise ValueError(
                "No existe un producto con ese código."
            )

        # Eliminar de la colección principal.
        self._productos.remove(producto)

        # Eliminar del índice.
        del self._productos_por_codigo[codigo]

        return "Producto eliminado correctamente."

    def listar_productos(self) -> list[Producto]:
        """
        Devuelve una copia de la lista principal de productos.
        """

        return self._productos.copy()

    def obtener_productos(self) -> list[Producto]:
        """
        Devuelve una copia de la lista principal de productos.
        """

        return self._productos.copy()

    def obtener_categorias(self) -> set[str]:
        """
        Devuelve las categorías únicas de los productos.

        Se utiliza un SET porque solamente interesan los
        valores únicos y se desea evitar categorías repetidas.
        """

        return {
            producto.categoria
            for producto in self._productos
        }

    # ============================================================
    # USUARIOS
    # ============================================================

    def registrar_usuario(self, usuario: Usuario) -> str:
        """
        Registra un usuario y actualiza el índice
        de identificaciones.
        """

        if self._buscar_usuario_por_identificacion(
            usuario.identificacion
        ) is not None:
            raise ValueError(
                "Ya existe un usuario con esa identificación."
            )

        # Colección principal.
        self._usuarios.append(usuario)

        # Índice.
        self._usuarios_por_identificacion[
            usuario.identificacion
        ] = usuario

        return "Usuario registrado correctamente."

    def buscar_usuario(
        self,
        identificacion: str
    ) -> Usuario | None:
        """
        Busca un usuario utilizando el índice
        de identificaciones.
        """

        return self._buscar_usuario_por_identificacion(
            identificacion
        )

    def listar_usuarios(self) -> list[Usuario]:
        """
        Devuelve una copia de la lista principal de usuarios.
        """

        return self._usuarios.copy()

    def obtener_usuarios(self) -> list[Usuario]:
        """
        Devuelve una copia de la lista principal de usuarios.
        """

        return self._usuarios.copy()

    # ============================================================
    # VENTAS
    # ============================================================

    def vender_producto(
        self,
        codigo_producto: str,
        identificacion_usuario: str,
        cantidad: int
    ) -> Venta | None:
        """
        Registra una venta y actualiza el stock.

        Las búsquedas de usuario y producto se realizan mediante
        sus respectivos índices.

        Además, la venta se almacena en:
        1. La lista principal de ventas.
        2. El índice de ventas por usuario.
        """

        # ========================================================
        # BUSCAR USUARIO MEDIANTE ÍNDICE
        # ========================================================

        usuario = self._buscar_usuario_por_identificacion(
            identificacion_usuario
        )

        if usuario is None:
            raise ValueError(
                "No existe un usuario con esa identificación."
            )

        # ========================================================
        # BUSCAR PRODUCTO MEDIANTE ÍNDICE
        # ========================================================

        producto = self._buscar_producto_por_codigo(
            codigo_producto
        )

        if producto is None:
            raise ValueError(
                "No existe un producto con ese código."
            )

        # ========================================================
        # VALIDAR CANTIDAD
        # ========================================================

        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError(
                "La cantidad debe ser un entero mayor que cero."
            )

        # ========================================================
        # VALIDAR STOCK
        # ========================================================

        if cantidad > producto.stock:
            raise ValueError(
                "No existe suficiente stock disponible."
            )

        # ========================================================
        # CREAR VENTA
        # ========================================================

        venta = Venta(
            usuario_id=identificacion_usuario,
            producto_codigo=codigo_producto,
            cantidad=cantidad
        )

        # ========================================================
        # ACTUALIZAR LISTA PRINCIPAL DE VENTAS
        # ========================================================

        self._ventas.append(venta)

        # ========================================================
        # ACTUALIZAR ÍNDICE DE VENTAS POR USUARIO
        # ========================================================

        if identificacion_usuario not in self._ventas_por_usuario:
            self._ventas_por_usuario[
                identificacion_usuario
            ] = []

        self._ventas_por_usuario[
            identificacion_usuario
        ].append(venta)

        # ========================================================
        # ACTUALIZAR STOCK
        # ========================================================

        producto.vender(cantidad)

        return venta

    def obtener_ventas(self) -> list[Venta]:
        """
        Devuelve una copia de la lista principal de ventas.
        """

        return self._ventas.copy()

    def consultar_ventas_usuario(
        self,
        identificacion_usuario: str
    ) -> list[Venta]:
        """
        Consulta las ventas de un usuario utilizando el índice.

        No es necesario recorrer toda la lista principal de ventas.
        """

        ventas = self._ventas_por_usuario.get(
            identificacion_usuario,
            []
        )

        return ventas.copy()

    # ============================================================
    # BÚSQUEDAS INTERNAS OPTIMIZADAS
    # ============================================================

    def _buscar_producto_por_codigo(
        self,
        codigo: str
    ) -> Producto | None:
        """
        Realiza una búsqueda directa en el diccionario índice
        de productos.

        Complejidad promedio: O(1).
        """

        return self._productos_por_codigo.get(codigo)

    def _buscar_usuario_por_identificacion(
        self,
        identificacion: str
    ) -> Usuario | None:
        """
        Realiza una búsqueda directa en el diccionario índice
        de usuarios.

        Complejidad promedio: O(1).
        """

        return self._usuarios_por_identificacion.get(
            identificacion
        )

    # ============================================================
    # CARGA Y RECONSTRUCCIÓN DE ÍNDICES
    # ============================================================

    def cargar_productos(
        self,
        productos: list[Producto]
    ) -> None:
        """
        Carga productos desde los objetos recuperados del JSON.

        Después de cargar la lista principal se reconstruye
        el índice de productos por código.
        """

        # Lista principal.
        self._productos = list(productos)

        # Reconstrucción del índice.
        self._productos_por_codigo = {
            producto.codigo: producto
            for producto in self._productos
        }

    def cargar_usuarios(
        self,
        usuarios: list[Usuario]
    ) -> None:
        """
        Carga usuarios desde los objetos recuperados del JSON.

        Después de cargar la lista principal se reconstruye
        el índice de usuarios por identificación.
        """

        # Lista principal.
        self._usuarios = list(usuarios)

        # Reconstrucción del índice.
        self._usuarios_por_identificacion = {
            usuario.identificacion: usuario
            for usuario in self._usuarios
        }

    def cargar_ventas(
        self,
        ventas: list[Venta]
    ) -> None:
        """
        Carga ventas desde los objetos recuperados del JSON.

        Después de cargar la lista principal se reconstruye
        el índice de ventas agrupadas por usuario.
        """

        # Lista principal.
        self._ventas = list(ventas)

        # Reiniciar índice.
        self._ventas_por_usuario = {}

        # Reconstruir índice.
        for venta in self._ventas:

            if venta.usuario_id not in self._ventas_por_usuario:
                self._ventas_por_usuario[
                    venta.usuario_id
                ] = []

            self._ventas_por_usuario[
                venta.usuario_id
            ].append(venta)