"""
Módulo de entidades del sistema Software FJ.

Define la clase abstracta EntidadSistema y la clase Cliente, encargada de
representar y validar los datos personales de un cliente (nombre,
identificación, teléfono y correo electrónico) mediante atributos privados,
propiedades con validación y excepciones personalizadas.
"""

from abc import ABC, abstractmethod
from excepciones import (
    ClienteError, NombreInvalidoError, IdentificacionInvalidaError,
    TelefonoInvalidoError, EmailInvalidoError
)
from logger import registrar_log


# ============================================================
# CLASE ABSTRACTA GENERAL
# ============================================================

class EntidadSistema(ABC):
    """
    Clase abstracta que representa una entidad general del sistema.
    """

    @abstractmethod
    def mostrar_informacion(self):
        pass


# ============================================================
# CLASE CLIENTE
# ============================================================

class Cliente(EntidadSistema):
    """
    Clase Cliente para el sistema Software FJ.

    Maneja datos personales del cliente con encapsulación,
    validaciones y excepciones personalizadas.
    """

    def __init__(self, nombre, identificacion, telefono, email):
        try:
            self.__nombre = None
            self.__identificacion = None
            self.__telefono = None
            self.__email = None

            self.nombre = nombre
            self.identificacion = identificacion
            self.telefono = telefono
            self.email = email

            registrar_log(
                "EVENTO",
                f"Cliente creado correctamente: {self.__nombre} - ID: {self.__identificacion}"
            )

        except ClienteError as error:
            registrar_log("ERROR", f"Error al crear cliente: {error}")
            raise

        except Exception as error:
            registrar_log("ERROR", f"Error inesperado al crear cliente: {error}")
            raise ClienteError("Ocurrió un error inesperado al crear el cliente.") from error

    # ========================================================
    # GETTERS Y SETTERS
    # ========================================================

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        if not isinstance(nuevo_nombre, str):
            raise NombreInvalidoError("El nombre debe ser un texto.")

        nuevo_nombre = nuevo_nombre.strip()

        if len(nuevo_nombre) < 3:
            raise NombreInvalidoError("El nombre debe tener mínimo 3 caracteres.")

        if not nuevo_nombre.replace(" ", "").isalpha():
            raise NombreInvalidoError("El nombre solo debe contener letras y espacios.")

        self.__nombre = nuevo_nombre

    @property
    def identificacion(self):
        return self.__identificacion

    @identificacion.setter
    def identificacion(self, nueva_identificacion):
        nueva_identificacion = str(nueva_identificacion).strip()

        if not nueva_identificacion.isdigit():
            raise IdentificacionInvalidaError("La identificación solo debe contener números.")

        if len(nueva_identificacion) < 6 or len(nueva_identificacion) > 12:
            raise IdentificacionInvalidaError(
                "La identificación debe tener entre 6 y 12 dígitos."
            )

        self.__identificacion = nueva_identificacion

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, nuevo_telefono):
        nuevo_telefono = str(nuevo_telefono).strip()

        if not nuevo_telefono.isdigit():
            raise TelefonoInvalidoError("El teléfono solo debe contener números.")

        if len(nuevo_telefono) != 10:
            raise TelefonoInvalidoError("El teléfono debe tener exactamente 10 dígitos.")

        self.__telefono = nuevo_telefono

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, nuevo_email):
        if not isinstance(nuevo_email, str):
            raise EmailInvalidoError("El correo debe ser un texto.")

        nuevo_email = nuevo_email.strip().lower()

        if "@" not in nuevo_email or "." not in nuevo_email:
            raise EmailInvalidoError("El correo electrónico no tiene un formato válido.")

        if nuevo_email.startswith("@") or nuevo_email.endswith("@"):
            raise EmailInvalidoError("El correo electrónico está mal estructurado.")

        self.__email = nuevo_email

    # ========================================================
    # MÉTODOS DE LA CLASE
    # ========================================================

    def actualizar_datos(self, nombre=None, telefono=None, email=None):
        """
        Método para actualizar datos del cliente.
        Usa parámetros opcionales simulando sobrecarga.
        """
        try:
            if nombre is not None:
                self.nombre = nombre

            if telefono is not None:
                self.telefono = telefono

            if email is not None:
                self.email = email

        except ClienteError as error:
            registrar_log(
                "ERROR",
                f"No se pudieron actualizar los datos del cliente {self.__identificacion}: {error}"
            )
            raise

        else:
            registrar_log(
                "EVENTO",
                f"Datos actualizados correctamente para el cliente ID: {self.__identificacion}"
            )

        finally:
            registrar_log(
                "EVENTO",
                f"Finalizó intento de actualización del cliente ID: {self.__identificacion}"
            )

    def mostrar_informacion(self):
        """
        Implementación del método abstracto.
        """
        return (
            f"Cliente: {self.__nombre}\n"
            f"ID: {self.__identificacion}\n"
            f"Teléfono: {self.__telefono}\n"
            f"Email: {self.__email}"
        )

    def __str__(self):
        return f"{self.__nombre} - ID: {self.__identificacion}"
