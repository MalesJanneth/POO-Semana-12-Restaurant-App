"""
Servicio encargado de la persistencia de productos,
usuarios y ventas mediante archivos JSON.
"""

import json

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

class ArchivoServicio:
    """
    Gestiona la lectura y escritura de productos,
    usuarios y ventas en archivos JSON.
    """

    def __init__(
        self,
        ruta_productos: str,
        ruta_usuarios: str,
        ruta_ventas: str,
    ) -> None:
        self._ruta_productos = ruta_productos
        self._ruta_usuarios = ruta_usuarios
        self._ruta_ventas = ruta_ventas

    def guardar_productos(
        self,
        productos: list[Producto],
    ) -> bool:
        """Guarda los productos en formato JSON."""

        datos_productos = [
            producto.a_diccionario()
            for producto in productos
        ]

        try:
            with open(
                self._ruta_productos,
                "w",
                encoding="utf-8",
            ) as archivo:

                json.dump(
                    datos_productos,
                    archivo,
                    ensure_ascii=False,
                    indent=4,
                )

            return True

        except PermissionError:
            print(
                "\nError: no existen permisos suficientes "
                "para escribir productos.json."
            )
            return False

        except FileNotFoundError:
            print(
                "\nError: no se encontró la carpeta "
                "destinada al archivo de productos."
            )
            return False

    def cargar_productos(self) -> list[Producto]:
        """Carga productos desde productos.json."""

        try:
            with open(
                self._ruta_productos,
                "r",
                encoding="utf-8",
            ) as archivo:

                datos = json.load(archivo)

        except FileNotFoundError:
            print(
                "\nAviso: todavía no existe productos.json. "
                "Se iniciará con productos vacíos."
            )
            return []

        except json.JSONDecodeError:
            print(
                "\nError: productos.json no contiene "
                "un formato JSON válido."
            )
            return []

        except PermissionError:
            print(
                "\nError: no existen permisos suficientes "
                "para leer productos.json."
            )
            return []

        if not isinstance(datos, list):
            print(
                "\nError: productos.json debe contener "
                "una lista de productos."
            )
            return []

        productos: list[Producto] = []

        for numero_registro, registro in enumerate(
            datos,
            start=1,
        ):
            try:
                if not isinstance(registro, dict):
                    raise ValueError(
                        "El registro no tiene formato de diccionario."
                    )

                producto = Producto(
                    codigo=registro["codigo"],
                    nombre=registro["nombre"],
                    categoria=registro["categoria"],
                    precio=registro["precio"],
                    stock=registro["stock"],
                    disponible=registro["disponible"],
                )

                productos.append(producto)

            except KeyError as error:
                print(
                    f"\nAviso: se omitió el registro "
                    f"{numero_registro} porque falta la clave "
                    f"{error}."
                )

            except ValueError as error:
                print(
                    f"\nAviso: se omitió el registro "
                    f"{numero_registro} por contener datos "
                    f"inválidos: {error}"
                )

            except TypeError as error:
                print(
                    f"\nAviso: se omitió el registro "
                    f"{numero_registro} por contener tipos "
                    f"de datos inválidos: {error}"
                )

        return productos

    def guardar_usuarios(
        self,
        usuarios: list[Usuario],
    ) -> bool:
        """Guarda los usuarios en formato JSON."""

        datos_usuarios = [
            usuario.a_diccionario()
            for usuario in usuarios
        ]

        try:
            with open(
                self._ruta_usuarios,
                "w",
                encoding="utf-8",
            ) as archivo:

                json.dump(
                    datos_usuarios,
                    archivo,
                    ensure_ascii=False,
                    indent=4,
                )

            return True

        except PermissionError:
            print(
                "\nError: no existen permisos suficientes "
                "para escribir usuarios.json."
            )
            return False

        except FileNotFoundError:
            print(
                "\nError: no se encontró la carpeta "
                "destinada al archivo de usuarios."
            )
            return False

    def cargar_usuarios(self) -> list[Usuario]:
        """Carga usuarios desde usuarios.json."""

        try:
            with open(
                self._ruta_usuarios,
                "r",
                encoding="utf-8",
            ) as archivo:

                datos = json.load(archivo)

        except FileNotFoundError:
            print(
                "\nAviso: todavía no existe usuarios.json. "
                "Se iniciará con usuarios vacíos."
            )
            return []

        except json.JSONDecodeError:
            print(
                "\nError: usuarios.json no contiene "
                "un formato JSON válido."
            )
            return []

        except PermissionError:
            print(
                "\nError: no existen permisos suficientes "
                "para leer usuarios.json."
            )
            return []

        if not isinstance(datos, list):
            print(
                "\nError: usuarios.json debe contener "
                "una lista de usuarios."
            )
            return []

        usuarios: list[Usuario] = []

        for numero_registro, registro in enumerate(
            datos,
            start=1,
        ):
            try:
                if not isinstance(registro, dict):
                    raise ValueError(
                        "El registro no tiene formato de diccionario."
                    )

                usuario = Usuario(
                    identificacion=registro["identificacion"],
                    nombre=registro["nombre"],
                    correo=registro["correo"],
                )

                usuarios.append(usuario)

            except KeyError as error:
                print(
                    f"\nAviso: se omitió el registro "
                    f"{numero_registro} porque falta la clave "
                    f"{error}."
                )

            except ValueError as error:
                print(
                    f"\nAviso: se omitió el registro "
                    f"{numero_registro} por contener datos "
                    f"inválidos: {error}"
                )

            except TypeError as error:
                print(
                    f"\nAviso: se omitió el registro "
                    f"{numero_registro} por contener tipos "
                    f"de datos inválidos: {error}"
                )

        return usuarios

    def guardar_ventas(
        self,
        ventas: list[Venta],
    ) -> bool:
        """Guarda las ventas en formato JSON."""

        datos_ventas = [
            venta.a_diccionario()
            for venta in ventas
        ]

        try:
            with open(
                self._ruta_ventas,
                "w",
                encoding="utf-8",
            ) as archivo:

                json.dump(
                    datos_ventas,
                    archivo,
                    ensure_ascii=False,
                    indent=4,
                )

            return True

        except PermissionError:
            print(
                "\nError: no existen permisos suficientes "
                "para escribir ventas.json."
            )
            return False

        except FileNotFoundError:
            print(
                "\nError: no se encontró la carpeta "
                "destinada al archivo de ventas."
            )
            return False

    def cargar_ventas(self) -> list[Venta]:
        """Carga ventas desde ventas.json."""

        try:
            with open(
                self._ruta_ventas,
                "r",
                encoding="utf-8",
            ) as archivo:

                datos = json.load(archivo)

        except FileNotFoundError:
            print(
                "\nAviso: todavía no existe ventas.json. "
                "Se iniciará con ventas vacías."
            )
            return []

        except json.JSONDecodeError:
            print(
                "\nError: ventas.json no contiene "
                "un formato JSON válido."
            )
            return []

        except PermissionError:
            print(
                "\nError: no existen permisos suficientes "
                "para leer ventas.json."
            )
            return []

        if not isinstance(datos, list):
            print(
                "\nError: ventas.json debe contener "
                "una lista de ventas."
            )
            return []

        ventas: list[Venta] = []

        for numero_registro, registro in enumerate(
            datos,
            start=1,
        ):
            try:
                if not isinstance(registro, dict):
                    raise ValueError(
                        "El registro no tiene formato de diccionario."
                    )

                venta = Venta(
                    usuario_id=registro["usuario_id"],
                    producto_codigo=registro["producto_codigo"],
                    cantidad=registro["cantidad"],
                )

                ventas.append(venta)

            except KeyError as error:
                print(
                    f"\nAviso: se omitió el registro "
                    f"{numero_registro} porque falta la clave "
                    f"{error}."
                )

            except ValueError as error:
                print(
                    f"\nAviso: se omitió el registro "
                    f"{numero_registro} por contener datos "
                    f"inválidos: {error}"
                )

            except TypeError as error:
                print(
                    f"\nAviso: se omitió el registro "
                    f"{numero_registro} por contener tipos "
                    f"de datos inválidos: {error}"
                )

        return ventas