"""
Programa principal del sistema Restaurante App.

Este módulo coordina la interacción con el usuario
mediante un menú de consola y utiliza los métodos
proporcionados por Restaurante.
"""

from pathlib import Path

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante import Restaurante


RUTA_DATOS = Path(__file__).resolve().parent / "datos"

RUTA_PRODUCTOS = str(
    RUTA_DATOS / "productos.json"
)

RUTA_USUARIOS = str(
    RUTA_DATOS / "usuarios.json"
)

RUTA_VENTAS = str(
    RUTA_DATOS / "ventas.json"
)


OPCIONES_MENU: tuple[str, ...] = (
    "1. Registrar producto",
    "2. Buscar producto",
    "3. Actualizar producto",
    "4. Eliminar producto",
    "5. Listar productos",
    "6. Registrar usuario",
    "7. Listar usuarios",
    "8. Mostrar categorías",
    "9. Vender producto",
    "10. Consultar ventas de un usuario",
    "11. Salir",
)


def mostrar_menu() -> None:
    """Muestra el menú principal del sistema."""

    print("\n" + "=" * 50)
    print("          SISTEMA DE RESTAURANTE")
    print("=" * 50)

    for opcion_menu in OPCIONES_MENU:
        print(opcion_menu)

    print("=" * 50)


def registrar_producto(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio,
) -> None:
    """Solicita los datos y registra un producto."""

    print("\n--- REGISTRAR PRODUCTO ---")

    try:
        codigo = input("Código: ").strip()
        nombre = input("Nombre: ").strip()
        categoria = input("Categoría: ").strip()

        precio = float(
            input("Precio: ").strip().replace(",", ".")
        )

        stock = int(
            input("Stock: ").strip()
        )

        producto = Producto(
            codigo=codigo,
            nombre=nombre,
            categoria=categoria,
            precio=precio,
            stock=stock,
        )

        resultado = restaurante.registrar_producto(producto)

        print(f"\n{resultado}")

        if "correctamente" in resultado:
            archivo_servicio.guardar_productos(
                restaurante.obtener_productos()
            )

    except ValueError as error:
        print(f"\nError: {error}")


def buscar_producto(
    restaurante: Restaurante,
) -> None:
    """Busca un producto mediante su código."""

    print("\n--- BUSCAR PRODUCTO ---")

    codigo = input(
        "Ingrese el código del producto: "
    ).strip()

    if not codigo:
        print("\nError: el código no puede estar vacío.")
        return

    producto = restaurante.buscar_producto(codigo)

    if producto is None:
        print(
            f"\nNo se encontró un producto con el código "
            f"{codigo}."
        )
        return

    print("\n=== PRODUCTO ENCONTRADO ===")
    print(producto.mostrar_informacion())


def actualizar_producto(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio,
) -> None:
    """Solicita los nuevos datos y actualiza un producto."""

    print("\n--- ACTUALIZAR PRODUCTO ---")

    codigo_actual = input(
        "Código del producto que desea actualizar: "
    ).strip()

    if not codigo_actual:
        print("\nError: el código no puede estar vacío.")
        return

    producto = restaurante.buscar_producto(codigo_actual)

    if producto is None:
        print(
            f"\nNo existe un producto con el código "
            f"{codigo_actual}."
        )
        return

    print("\nIngrese los nuevos datos.")
    print("Presione Enter para conservar el valor actual.")

    try:
        nuevo_codigo = input(
            f"Código [{producto.codigo}]: "
        ).strip()

        nuevo_nombre = input(
            f"Nombre [{producto.nombre}]: "
        ).strip()

        nueva_categoria = input(
            f"Categoría [{producto.categoria}]: "
        ).strip()

        precio_texto = input(
            f"Precio [{producto.precio:.2f}]: "
        ).strip()

        stock_texto = input(
            f"Stock [{producto.stock}]: "
        ).strip()

        disponibilidad_texto = input(
            "¿Está disponible? (s/n): "
        ).strip().lower()

        if not nuevo_codigo:
            nuevo_codigo = producto.codigo

        if not nuevo_nombre:
            nuevo_nombre = producto.nombre

        if not nueva_categoria:
            nueva_categoria = producto.categoria

        if precio_texto:
            nuevo_precio = float(
                precio_texto.replace(",", ".")
            )
        else:
            nuevo_precio = producto.precio

        if stock_texto:
            nuevo_stock = int(stock_texto)
        else:
            nuevo_stock = producto.stock

        if not disponibilidad_texto:
            nueva_disponibilidad = producto.disponible

        elif disponibilidad_texto in ("s", "si", "sí"):
            nueva_disponibilidad = True

        elif disponibilidad_texto in ("n", "no"):
            nueva_disponibilidad = False

        else:
            print(
                "\nError: debe ingresar 's' para sí "
                "o 'n' para no."
            )
            return

        resultado = restaurante.actualizar_producto(
            codigo_actual=codigo_actual,
            nuevo_codigo=nuevo_codigo,
            nuevo_nombre=nuevo_nombre,
            nueva_categoria=nueva_categoria,
            nuevo_precio=nuevo_precio,
            nuevo_stock=nuevo_stock,
            nueva_disponibilidad=nueva_disponibilidad,
        )

        print(f"\n{resultado}")

        if "correctamente" in resultado:
            archivo_servicio.guardar_productos(
                restaurante.obtener_productos()
            )

    except ValueError as error:
        print(f"\nError: {error}")


def eliminar_producto(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio,
) -> None:
    """Elimina un producto mediante su código."""

    print("\n--- ELIMINAR PRODUCTO ---")

    codigo = input(
        "Ingrese el código del producto que desea eliminar: "
    ).strip()

    if not codigo:
        print("\nError: el código no puede estar vacío.")
        return

    producto = restaurante.buscar_producto(codigo)

    if producto is None:
        print(
            f"\nNo existe un producto con el código "
            f"{codigo}."
        )
        return

    confirmacion = input(
        f'¿Está seguro de eliminar "{producto.nombre}"? (s/n): '
    ).strip().lower()

    if confirmacion not in ("s", "si", "sí"):
        print("\nOperación cancelada.")
        return

    resultado = restaurante.eliminar_producto(codigo)

    print(f"\n{resultado}")

    if "correctamente" in resultado:
        archivo_servicio.guardar_productos(
            restaurante.obtener_productos()
        )


def listar_productos(
    restaurante: Restaurante,
) -> None:
    """
    Muestra todos los productos registrados.

    La lista principal sigue almacenando objetos Producto.
    Para mostrar sus datos se utiliza el método
    mostrar_informacion().
    """

    productos = restaurante.listar_productos()

    if not productos:
        print("\nNo existen productos registrados.")
        return

    print("\n=== PRODUCTOS REGISTRADOS ===")

    for producto in productos:
        print(producto.mostrar_informacion())


def registrar_usuario(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio,
) -> None:
    """Solicita los datos y registra un usuario."""

    print("\n--- REGISTRAR USUARIO ---")

    try:
        identificacion = input(
            "Identificación: "
        ).strip()

        nombre = input(
            "Nombre: "
        ).strip()

        correo = input(
            "Correo: "
        ).strip()

        usuario = Usuario(
            identificacion=identificacion,
            nombre=nombre,
            correo=correo,
        )

        resultado = restaurante.registrar_usuario(usuario)

        print(f"\n{resultado}")

        if "correctamente" in resultado:
            archivo_servicio.guardar_usuarios(
                restaurante.obtener_usuarios()
            )

    except ValueError as error:
        print(f"\nError: {error}")


def listar_usuarios(
    restaurante: Restaurante,
) -> None:
    """
    Muestra todos los usuarios registrados.

    Los objetos Usuario se mantienen en la lista principal
    y se utiliza mostrar_informacion() para su presentación.
    """

    usuarios = restaurante.listar_usuarios()

    if not usuarios:
        print("\nNo existen usuarios registrados.")
        return

    print("\n=== USUARIOS REGISTRADOS ===")

    for usuario in usuarios:
        print(usuario.mostrar_informacion())


def mostrar_categorias(
    restaurante: Restaurante,
) -> None:
    """Muestra las categorías únicas de los productos."""

    categorias = restaurante.obtener_categorias()

    if not categorias:
        print("\nNo existen categorías registradas.")
        return

    print("\n=== CATEGORÍAS DISPONIBLES ===")

    for categoria in sorted(categorias):
        print(f"- {categoria}")


def vender_producto(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio,
) -> None:
    """Solicita los datos y registra una venta."""

    print("\n--- VENDER PRODUCTO ---")

    try:
        identificacion_usuario = input(
            "Identificación del usuario: "
        ).strip()

        codigo_producto = input(
            "Código del producto: "
        ).strip()

        cantidad = int(
            input("Cantidad: ").strip()
        )

        resultado = restaurante.vender_producto(
            codigo_producto=codigo_producto,
            identificacion_usuario=identificacion_usuario,
            cantidad=cantidad,
        )

        if not resultado:
            print(
                "\nVenta rechazada. Verifique que el usuario "
                "y el producto existan, que la cantidad sea "
                "mayor que cero y que exista stock suficiente."
            )
            return

        archivo_servicio.guardar_ventas(
            restaurante.obtener_ventas()
        )

        archivo_servicio.guardar_productos(
            restaurante.obtener_productos()
        )

        print("\nVenta registrada correctamente.")

    except ValueError as error:
        print(f"\nError: {error}")


def consultar_ventas_usuario(
    restaurante: Restaurante,
) -> None:
    """Muestra las ventas realizadas por un usuario."""

    print("\n--- CONSULTAR VENTAS DE UN USUARIO ---")

    identificacion_usuario = input(
        "Identificación del usuario: "
    ).strip()

    if not identificacion_usuario:
        print(
            "\nError: la identificación "
            "no puede estar vacía."
        )
        return

    ventas = restaurante.consultar_ventas_usuario(
        identificacion_usuario
    )

    if not ventas:
        print(
            "\nNo existen ventas registradas "
            "para este usuario."
        )
        return

    print("\n=== VENTAS DEL USUARIO ===")

    for venta in ventas:
        producto = restaurante.buscar_producto(
            venta.producto_codigo
        )

        if producto is not None:
            print(
                f"Producto: {producto.nombre} | "
                f"Código: {venta.producto_codigo} | "
                f"Cantidad: {venta.cantidad}"
            )

        else:
            print(
                f"Producto: {venta.producto_codigo} | "
                f"Cantidad: {venta.cantidad}"
            )


def obtener_acciones_menu() -> dict[str, str]:
    """
    Devuelve un diccionario que relaciona cada opción
    del menú con el nombre de la operación correspondiente.
    """

    return {
        "1": "registrar_producto",
        "2": "buscar_producto",
        "3": "actualizar_producto",
        "4": "eliminar_producto",
        "5": "listar_productos",
        "6": "registrar_usuario",
        "7": "listar_usuarios",
        "8": "mostrar_categorias",
        "9": "vender_producto",
        "10": "consultar_ventas_usuario",
    }


def ejecutar_accion(
    accion: str,
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio,
) -> None:
    """Ejecuta la operación correspondiente al menú."""

    if accion == "registrar_producto":
        registrar_producto(
            restaurante,
            archivo_servicio,
        )

    elif accion == "buscar_producto":
        buscar_producto(restaurante)

    elif accion == "actualizar_producto":
        actualizar_producto(
            restaurante,
            archivo_servicio,
        )

    elif accion == "eliminar_producto":
        eliminar_producto(
            restaurante,
            archivo_servicio,
        )

    elif accion == "listar_productos":
        listar_productos(restaurante)

    elif accion == "registrar_usuario":
        registrar_usuario(
            restaurante,
            archivo_servicio,
        )

    elif accion == "listar_usuarios":
        listar_usuarios(restaurante)

    elif accion == "mostrar_categorias":
        mostrar_categorias(restaurante)

    elif accion == "vender_producto":
        vender_producto(
            restaurante,
            archivo_servicio,
        )

    elif accion == "consultar_ventas_usuario":
        consultar_ventas_usuario(restaurante)


def main() -> None:
    """
    Punto de entrada de la aplicación.

    Se crean los servicios, se cargan los datos almacenados
    en JSON y posteriormente se reconstruyen los índices
    en memoria mediante Restaurante.
    """

    restaurante = Restaurante()

    archivo_servicio = ArchivoServicio(
        ruta_productos=RUTA_PRODUCTOS,
        ruta_usuarios=RUTA_USUARIOS,
        ruta_ventas=RUTA_VENTAS,
    )

    # ========================================================
    # CARGAR DATOS DESDE JSON
    # ========================================================

    productos_cargados = (
        archivo_servicio.cargar_productos()
    )

    usuarios_cargados = (
        archivo_servicio.cargar_usuarios()
    )

    ventas_cargadas = (
        archivo_servicio.cargar_ventas()
    )

    # ========================================================
    # CARGAR COLECCIONES Y RECONSTRUIR ÍNDICES
    # ========================================================

    restaurante.cargar_productos(
        productos_cargados
    )

    restaurante.cargar_usuarios(
        usuarios_cargados
    )

    restaurante.cargar_ventas(
        ventas_cargadas
    )

    # ========================================================
    # MENÚ
    # ========================================================

    acciones_menu = obtener_acciones_menu()

    while True:
        mostrar_menu()

        opcion = input(
            "\nSeleccione una opción: "
        ).strip()

        if opcion == "11":
            print(
                "\nGracias por utilizar Restaurante App."
            )
            break

        accion = acciones_menu.get(opcion)

        if accion is None:
            print(
                "\nOpción no válida. "
                "Seleccione una opción del 1 al 11."
            )
            continue

        try:
            ejecutar_accion(
                accion,
                restaurante,
                archivo_servicio,
            )

        except (ValueError, TypeError) as error:
            print(f"\nError: {error}")

        except KeyboardInterrupt:
            print(
                "\n\nPrograma interrumpido por el usuario."
            )
            break


if __name__ == "__main__":
    main()