from pathlib import Path

from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante import Restaurante

BASE_DIR = Path(__file__).resolve().parent
DATOS_DIR = BASE_DIR / "datos"

RUTA_PRODUCTOS = DATOS_DIR / "productos.json"
RUTA_USUARIOS = DATOS_DIR / "usuarios.json"
RUTA_VENTAS = DATOS_DIR / "ventas.json"

OPCIONES_MENU = (
    ("1", "Registrar producto"),
    ("2", "Buscar producto"),
    ("3", "Listar productos"),
    ("4", "Actualizar producto"),
    ("5", "Eliminar producto"),
    ("6", "Registrar usuario"),
    ("7", "Buscar usuario por identificación"),
    ("8", "Listar usuarios"),
    ("9", "Actulizar usuario"),
    ("10", "Eliminar usuario"),
    ("11", "Registrar venta"),
    ("12", "Consultar ventas de un usuario"),
    ("13", "Listar ventas"),
    ("14", "Vender producto"),
    ("15", "Salir"),
)

def pedir_texto(mensaje: str) -> str:
    return input(mensaje).strip()

def pedir_entero(mensaje: str) -> int:
    return int(pedir_texto(mensaje))

def pedir_float(mensaje: str) -> float:
    return float(pedir_texto(mensaje))

def mostrar_menu() -> None:
    print("\n========== MENÚ PRINCIPAL ==========")

    for numero, descripcion in OPCIONES_MENU:
        print(f"{numero}. {descripcion}")

def guardar_productos(
    archivo_servicio: ArchivoServicio,
    restaurante: Restaurante,
) -> None:
    if not archivo_servicio.guardar_productos(
        restaurante.listar_productos()
    ):
        print("No se pudieron guardar los productos.")

def guardar_usuarios(
    archivo_servicio: ArchivoServicio,
    restaurante: Restaurante,
) -> None:
    if not archivo_servicio.guardar_usuarios(
        restaurante.listar_usuarios()
    ):
        print("No se pudieron guardar los usuarios.")

def guardar_ventas(
    archivo_servicio: ArchivoServicio,
    restaurante: Restaurante,
) -> None:
    if not archivo_servicio.guardar_ventas(
        restaurante.listar_ventas()
    ):
        print("No se pudieron guardar las ventas.")

def registrar_producto(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio,
) -> None:
    print("\n--- Registrar producto ---")

    codigo = pedir_texto("Código: ")
    nombre = pedir_texto("Nombre: ")
    categoria = pedir_texto("Categoría: ")
    precio = pedir_float("Precio: ")
    stock = pedir_entero("Stock: ")

    try:
        producto = restaurante.registrar_producto(codigo, nombre, categoria, precio, stock)

        guardar_productos(
            archivo_servicio,
            restaurante,
        )

        print("Producto registrado correctamente.")
        print(producto.mostrar_informacion())

    except (ValueError, TypeError) as error:
        print(f"Error: {error}")

def buscar_producto(
    restaurante: Restaurante,
) -> None:
    print("\n--- Buscar producto ---")

    codigo = pedir_texto(
        "Ingrese el código del producto: "
    )

    producto = restaurante.buscar_producto(codigo)

    if producto is None:
        print("Producto no encontrado.")
        return

    print(producto.mostrar_informacion())

def listar_productos(
    restaurante: Restaurante,
) -> None:
    print("\n--- Lista de productos ---")

    productos = restaurante.listar_productos()

    if len(productos) == 0:
        print("No existen productos registrados.")
        return

    for indice, producto in enumerate(productos):
        print(f"{indice + 1}.")
        print(producto.mostrar_informacion())


def actualizar_producto(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio,
) -> None:
    print("\n--- Actualizar producto ---")

    codigo_actual = pedir_texto(
        "Código del producto que desea actualizar: "
    )

    producto_actual = restaurante.buscar_producto(
        codigo_actual
    )

    if producto_actual is None:
        print("Producto no encontrado.")
        return

    codigo = pedir_texto("Nuevo código: ")
    nombre = pedir_texto("Nuevo nombre: ")
    categoria = pedir_texto("Nueva categoría: ")
    precio = pedir_float("Nuevo precio: ")
    stock = pedir_entero("Nuevo stock: ")

    try:
        producto = restaurante.actualizar_producto(codigo_actual, codigo, nombre, categoria, precio, stock,)

        guardar_productos(
            archivo_servicio,
            restaurante,
        )

        if codigo != codigo_actual:
            guardar_ventas(
                archivo_servicio,
                restaurante,
            )

        print("Producto actualizado correctamente.")
        print(producto.mostrar_informacion())

    except (ValueError, TypeError) as error:
        print(f"Error: {error}")


def eliminar_producto(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio,
) -> None:
    print("\n--- Eliminar producto ---")

    codigo = pedir_texto(
        "Código del producto a eliminar: "
    )

    try:
        producto = restaurante.eliminar_producto(codigo)

        guardar_productos(
            archivo_servicio,
            restaurante,
        )

        print("Producto eliminado correctamente.")
        print(f"Producto eliminado: {producto.nombre}")

    except (ValueError, TypeError) as error:
        print(f"Error: {error}")

def registrar_usuario(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio,
) -> None:
    print("\n--- Registrar usuario ---")

    identificacion = pedir_texto("Identificación: ")
    nombre = pedir_texto("Nombre: ")
    correo = pedir_texto("Correo: ")

    try:
        usuario = restaurante.registrar_usuario(
            identificacion,
            nombre,
            correo,
        )

        guardar_usuarios(
            archivo_servicio,
            restaurante,
        )

        print("Usuario registrado correctamente.")
        print(usuario.mostrar_informacion())

    except (ValueError, TypeError) as error:
        print(f"Error: {error}")

def buscar_usuario(
    restaurante: Restaurante,
) -> None:
    print("\n--- Buscar usuario por identificación ---")

    identificacion = pedir_texto(
        "Ingrese la identificación del usuario: "
    )

    usuario = restaurante.buscar_usuario(
        identificacion
    )

    if usuario is None:
        print(
            "No existe un usuario con esa identificación."
        )
        return

    print(usuario.mostrar_informacion())

def listar_usuarios(
    restaurante: Restaurante,
) -> None:
    print("\n--- Lista de usuarios ---")

    usuarios = restaurante.listar_usuarios()

    if len(usuarios) == 0:
        print("No existen usuarios registrados.")
        return

    for indice, usuario in enumerate(usuarios):
        print(f"{indice + 1}.")
        print(usuario.mostrar_informacion())


def actualizar_usuario(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio,
) -> None:
    print("\n--- Actualizar usuario ---")

    identificacion = pedir_texto(
        "Identificación del usuario: "
    )

    usuario = restaurante.buscar_usuario(
        identificacion
    )

    if usuario is None:
        print(
            "No existe un usuario con esa identificación."
        )
        return

    nombre = pedir_texto("Nuevo nombre: ")
    correo = pedir_texto("Nuevo correo: ")

    try:
        usuario = restaurante.actualizar_usuario(
            identificacion,
            nombre,
            correo,
        )

        guardar_usuarios(
            archivo_servicio,
            restaurante,
        )

        print("Usuario actualizado correctamente.")
        print(usuario.mostrar_informacion())

    except (ValueError, TypeError) as error:
        print(f"Error: {error}")

def eliminar_usuario(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio,
) -> None:
    print("\n--- Eliminar usuario ---")

    identificacion = pedir_texto(
        "Identificación del usuario: "
    )

    try:
        usuario = restaurante.eliminar_usuario(
            identificacion
        )

        guardar_usuarios(
            archivo_servicio,
            restaurante,
        )

        print("Usuario eliminado correctamente.")
        print(f"Usuario eliminado: {usuario.nombre}")

    except (ValueError, TypeError) as error:
        print(f"Error: {error}")

def registrar_venta(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio,
) -> None:
    print("\n--- Registrar venta ---")

    identificacion_usuario = pedir_texto(
        "Identificación del usuario: "
    )

    codigo_producto = pedir_texto(
        "Código del producto: "
    )

    cantidad = pedir_entero("Cantidad: ")

    try:
        venta = restaurante.registrar_venta(
            identificacion_usuario,
            codigo_producto,
            cantidad,
        )

        guardar_ventas(
            archivo_servicio,
            restaurante,
        )

        guardar_productos(
            archivo_servicio,
            restaurante,
        )

        print("Venta registrada correctamente.")
        print(
            f"Usuario: {venta.usuario_id} | "
            f"Producto: {venta.producto_codigo} | "
            f"Cantidad: {venta.cantidad}"
        )

    except (ValueError, TypeError) as error:
        print(f"Error: {error}")

def consultar_ventas_usuario(
    restaurante: Restaurante,
) -> None:
    print("\n--- Consultar ventas de un usuario ---")

    identificacion_usuario = pedir_texto(
        "Identificación del usuario: "
    )

    usuario = restaurante.buscar_usuario(
        identificacion_usuario
    )

    if usuario is None:
        print(
            "No existe un usuario con esa identificación."
        )
        return

    ventas = restaurante.consultar_ventas_usuario(
        identificacion_usuario
    )

    if len(ventas) == 0:
        print("El usuario no tiene ventas registradas.")
        return

    print(f"\nUsuario: {usuario.nombre}")

    for venta in ventas:
        producto = restaurante.buscar_producto(
            venta.producto_codigo
        )

        nombre_producto = (
            producto.nombre
            if producto is not None
            else "Producto no disponible"
        )

        print(
            f"Producto: {nombre_producto} | "
            f"Código: {venta.producto_codigo} | "
            f"Cantidad: {venta.cantidad}"
        )

def listar_ventas(
    restaurante: Restaurante,
) -> None:
    print("\n--- Lista de ventas ---")

    ventas = restaurante.listar_ventas()

    if len(ventas) == 0:
        print("No existen ventas registradas.")
        return

    for indice, venta in enumerate(ventas):
        usuario = restaurante.buscar_usuario(
            venta.usuario_id
        )

        producto = restaurante.buscar_producto(
            venta.producto_codigo
        )

        nombre_usuario = (
            usuario.nombre
            if usuario is not None
            else "Usuario no disponible"
        )

        nombre_producto = (
            producto.nombre
            if producto is not None
            else "Producto no disponible"
        )

        print(
            f"{indice + 1}. "
            f"Usuario: {nombre_usuario} | "
            f"Producto: {nombre_producto} | "
            f"Código: {venta.producto_codigo} | "
            f"Cantidad: {venta.cantidad}"
        )

def ejecutar_menu() -> None:
    DATOS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    archivo_servicio = ArchivoServicio(
        str(RUTA_PRODUCTOS),
        str(RUTA_USUARIOS),
        str(RUTA_VENTAS),
    )

    restaurante = Restaurante()

    productos = archivo_servicio.cargar_productos()
    usuarios = archivo_servicio.cargar_usuarios()
    ventas = archivo_servicio.cargar_ventas()

    restaurante.cargar_productos(productos)
    restaurante.cargar_usuarios(usuarios)
    restaurante.cargar_ventas(ventas)

    opciones = {
        "1": lambda: registrar_producto(restaurante, archivo_servicio),
        "2": lambda: buscar_producto(restaurante),
        "3": lambda: listar_productos(restaurante),
        "4": lambda: actualizar_producto(restaurante, archivo_servicio),
        "5": lambda: eliminar_producto(restaurante, archivo_servicio),
        "6": lambda: registrar_usuario(restaurante, archivo_servicio),
        "7": lambda: buscar_usuario(restaurante),
        "8": lambda: listar_usuarios(restaurante),
        "9": lambda: actualizar_usuario(restaurante, archivo_servicio),
        "10": lambda: eliminar_usuario(restaurante, archivo_servicio),
        "11": lambda: registrar_venta(restaurante, archivo_servicio),
        "12": lambda: consultar_ventas_usuario(restaurante),
        "13": lambda: listar_ventas(restaurante),
        "14": lambda: registrar_venta(restaurante, archivo_servicio),
    }

    while True:
        mostrar_menu()

        opcion = pedir_texto(
            "\nSeleccione una opción: "
        )

        if opcion == "15":
            print("Programa finalizado.")
            break

        accion = opciones.get(opcion)

        if accion is None:
            print("Opción no válida.")
        else:
            accion()

if __name__ == "__main__":
    ejecutar_menu()