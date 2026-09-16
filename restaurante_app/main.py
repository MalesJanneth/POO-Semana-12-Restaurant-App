from pathlib import Path

from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante import Restaurante


BASE_DIR = Path(__file__).resolve().parent
DATOS_DIR = BASE_DIR / "datos"

RUTA_PRODUCTOS = DATOS_DIR / "productos.json"
RUTA_USUARIOS = DATOS_DIR / "usuarios.json"
RUTA_VENTAS = DATOS_DIR / "ventas.json"


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
    print("\n========== MENÚ PRINCIPAL ==========")

    for opcion in OPCIONES_MENU:
        print(opcion)


def leer_entero(mensaje: str) -> int:
    return int(input(mensaje).strip())


def leer_float(mensaje: str) -> float:
    return float(input(mensaje).strip())


def registrar_producto(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio,
) -> None:

    try:
        codigo = input("Código: ").strip()
        nombre = input("Nombre: ").strip()
        categoria = input("Categoría: ").strip()
        precio = leer_float("Precio: ")
        stock = leer_entero("Stock: ")

        producto = restaurante.registrar_producto(
            codigo,
            nombre,
            categoria,
            precio,
            stock,
        )

        if archivo_servicio.guardar_productos(
            restaurante.obtener_productos()
        ):
            print(
                "Producto registrado y guardado correctamente."
            )
        else:
            print(
                "Producto registrado en memoria, "
                "pero no pudo guardarse en productos.json."
            )

        print(producto.mostrar_informacion())

    except (ValueError, TypeError) as error:
        print(f"Error: {error}")


def buscar_producto(
    restaurante: Restaurante,
) -> None:

    codigo = input(
        "Ingrese el código del producto: "
    ).strip()

    producto = restaurante.buscar_producto(codigo)

    if producto is None:
        print("Producto no encontrado.")
        return

    print(producto.mostrar_informacion())


def actualizar_producto(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio,
) -> None:

    try:
        codigo_actual = input(
            "Código del producto que desea actualizar: "
        ).strip()

        producto_actual = restaurante.buscar_producto(
            codigo_actual
        )

        if producto_actual is None:
            print("Producto no encontrado.")
            return

        print("Ingrese los nuevos datos:")

        codigo = input("Nuevo código: ").strip()
        nombre = input("Nuevo nombre: ").strip()
        categoria = input("Nueva categoría: ").strip()
        precio = leer_float("Nuevo precio: ")
        stock = leer_entero("Nuevo stock: ")

        producto = restaurante.actualizar_producto(
            codigo_actual,
            codigo,
            nombre,
            categoria,
            precio,
            stock,
        )

        if archivo_servicio.guardar_productos(
            restaurante.obtener_productos()
        ):
            print(
                "Producto actualizado y guardado correctamente."
            )
        else:
            print(
                "Producto actualizado en memoria, "
                "pero no pudo guardarse en productos.json."
            )

        # Las ventas se actualizan internamente si cambió
        # el código del producto.
        if codigo != codigo_actual:
            if archivo_servicio.guardar_ventas(
                restaurante.obtener_ventas()
            ):
                print(
                    "Las ventas relacionadas también fueron actualizadas."
                )
            else:
                print(
                    "No se pudo actualizar ventas.json."
                )

        print(producto.mostrar_informacion())

    except (ValueError, TypeError) as error:
        print(f"Error: {error}")


def eliminar_producto(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio,
) -> None:

    try:
        codigo = input(
            "Código del producto a eliminar: "
        ).strip()

        producto = restaurante.eliminar_producto(codigo)

        if archivo_servicio.guardar_productos(
            restaurante.obtener_productos()
        ):
            print(
                "Producto eliminado y cambios guardados correctamente."
            )
        else:
            print(
                "Producto eliminado en memoria, "
                "pero no pudo actualizarse productos.json."
            )

        print(
            f"Producto eliminado: {producto.nombre}"
        )

    except (ValueError, TypeError) as error:
        print(f"Error: {error}")


def listar_productos(
    restaurante: Restaurante,
) -> None:

    productos = restaurante.listar_productos()

    if not productos:
        print("No existen productos registrados.")
        return

    print("\n========== PRODUCTOS ==========")

    for producto in productos:
        print(producto.mostrar_informacion())


def registrar_usuario(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio,
) -> None:

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

        usuario = restaurante.registrar_usuario(
            identificacion,
            nombre,
            correo,
        )

        if archivo_servicio.guardar_usuarios(
            restaurante.obtener_usuarios()
        ):
            print(
                "Usuario registrado y guardado correctamente."
            )
        else:
            print(
                "Usuario registrado en memoria, "
                "pero no pudo guardarse en usuarios.json."
            )

        print(usuario.mostrar_informacion())

    except (ValueError, TypeError) as error:
        print(f"Error: {error}")


def listar_usuarios(
    restaurante: Restaurante,
) -> None:

    usuarios = restaurante.listar_usuarios()

    if not usuarios:
        print("No existen usuarios registrados.")
        return

    print("\n========== USUARIOS ==========")

    for usuario in usuarios:
        print(usuario.mostrar_informacion())


def mostrar_categorias(
    restaurante: Restaurante,
) -> None:

    categorias = restaurante.obtener_categorias()

    if not categorias:
        print("No existen categorías registradas.")
        return

    print("\n========== CATEGORÍAS ==========")

    for categoria in sorted(categorias):
        print(f"- {categoria}")


def vender_producto(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio,
) -> None:

    try:
        identificacion_usuario = input(
            "Identificación del usuario: "
        ).strip()

        codigo_producto = input(
            "Código del producto: "
        ).strip()

        cantidad = leer_entero(
            "Cantidad: "
        )

        venta = restaurante.vender_producto(
            identificacion_usuario,
            codigo_producto,
            cantidad,
        )

        ventas_guardadas = archivo_servicio.guardar_ventas(
            restaurante.obtener_ventas()
        )

        productos_guardados = archivo_servicio.guardar_productos(
            restaurante.obtener_productos()
        )

        if ventas_guardadas and productos_guardados:
            print(
                "Venta realizada y datos guardados correctamente."
            )
        else:
            print(
                "La venta se realizó en memoria, "
                "pero no se pudieron guardar correctamente "
                "todos los archivos JSON."
            )

        print(
            f"Venta registrada: usuario {venta.usuario_id}, "
            f"producto {venta.producto_codigo}, "
            f"cantidad {venta.cantidad}."
        )

    except (ValueError, TypeError) as error:
        print(f"Error: {error}")


def consultar_ventas_usuario(
    restaurante: Restaurante,
) -> None:

    identificacion_usuario = input(
        "Identificación del usuario: "
    ).strip()

    usuario = restaurante.buscar_usuario(
        identificacion_usuario
    )

    if usuario is None:
        print(
            "No existe un usuario con esa identificación."
        )
        return

    # Esta consulta utiliza directamente el índice
    # de ventas agrupadas por usuario.
    ventas = restaurante.consultar_ventas_usuario(
        identificacion_usuario
    )

    if not ventas:
        print(
            "El usuario no tiene ventas registradas."
        )
        return

    print(
        f"\n========== VENTAS DE {usuario.nombre} =========="
    )

    for venta in ventas:

        # La búsqueda del producto también utiliza
        # el índice por código.
        producto = restaurante.buscar_producto(
            venta.producto_codigo
        )

        if producto is not None:
            nombre_producto = producto.nombre
        else:
            nombre_producto = "Producto no disponible"

        print(
            f"Producto: {nombre_producto} | "
            f"Código: {venta.producto_codigo} | "
            f"Cantidad: {venta.cantidad}"
        )


def obtener_acciones_menu() -> dict[str, str]:
    """
    Diccionario auxiliar que representa las opciones válidas
    del menú.
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
        "11": "salir",
    }


def ejecutar_accion(
    opcion: str,
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio,
) -> bool:

    acciones = obtener_acciones_menu()

    if opcion not in acciones:
        print("Opción no válida.")
        return True

    if opcion == "1":
        registrar_producto(
            restaurante,
            archivo_servicio,
        )

    elif opcion == "2":
        buscar_producto(restaurante)

    elif opcion == "3":
        actualizar_producto(
            restaurante,
            archivo_servicio,
        )

    elif opcion == "4":
        eliminar_producto(
            restaurante,
            archivo_servicio,
        )

    elif opcion == "5":
        listar_productos(restaurante)

    elif opcion == "6":
        registrar_usuario(
            restaurante,
            archivo_servicio,
        )

    elif opcion == "7":
        listar_usuarios(restaurante)

    elif opcion == "8":
        mostrar_categorias(restaurante)

    elif opcion == "9":
        vender_producto(
            restaurante,
            archivo_servicio,
        )

    elif opcion == "10":
        consultar_ventas_usuario(
            restaurante
        )

    elif opcion == "11":
        print("Programa finalizado.")
        return False

    return True


def main() -> None:

    DATOS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    restaurante = Restaurante()

    archivo_servicio = ArchivoServicio(
        str(RUTA_PRODUCTOS),
        str(RUTA_USUARIOS),
        str(RUTA_VENTAS),
    )

    # =========================================================
    # CARGA DE DATOS Y RECONSTRUCCIÓN DE ÍNDICES
    # =========================================================

    productos = archivo_servicio.cargar_productos()
    usuarios = archivo_servicio.cargar_usuarios()
    ventas = archivo_servicio.cargar_ventas()

    restaurante.cargar_productos(productos)
    restaurante.cargar_usuarios(usuarios)
    restaurante.cargar_ventas(ventas)

    # Los índices auxiliares quedan reconstruidos dentro
    # de Restaurante a partir de los objetos recuperados.

    while True:

        mostrar_menu()

        opcion = input(
            "\nSeleccione una opción: "
        ).strip()

        continuar = ejecutar_accion(
            opcion,
            restaurante,
            archivo_servicio,
        )

        if not continuar:
            break


if __name__ == "__main__":
    main()