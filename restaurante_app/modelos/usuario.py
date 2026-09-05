"""
Este módulo contiene la clase Usuario.
La clase Usuario representa de manera general
a una persona registrada en el sistema.
"""

class Usuario:
    def __init__(
        self,
        identificacion: str,
        nombre: str,
        correo: str
    ):
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo

    @property
    def identificacion(self):
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor):
        if not valor or not isinstance(valor, str):
            raise ValueError(
                "La identificación del usuario es obligatoria."
            )
        self._identificacion = valor

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not isinstance(valor, str):
            raise ValueError(
                "El nombre del usuario es obligatorio."
            )
        self._nombre = valor

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if not valor or not isinstance(valor, str):
            raise ValueError(
                "El correo electrónico es obligatorio."
            )

        if "@" not in valor:
            raise ValueError(
                "El correo electrónico no es válido."
            )

        self._correo = valor

    def mostrar_informacion(self):
        return (
            f"Identificación: {self.identificacion} | "
            f"Nombre: {self.nombre} | "
            f"Correo: {self.correo}"
        )

    def a_diccionario(self):
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo
        }