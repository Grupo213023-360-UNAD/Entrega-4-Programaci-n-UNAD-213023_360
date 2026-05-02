import logging
from abc import ABC, abstractmethod
from datetime import datetime

def registrar_log(tipo, mensaje):
    """
    Registra eventos y errores en un archivo de logs.
    """
    try:
        with open("software_fj.log", "a", encoding="utf-8") as archivo:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo.write(f"[{fecha}] [{tipo}] {mensaje}\n")
    except Exception as error:
        print(f"No se pudo escribir en el archivo de logs: {error}")


# ============================================================
# EXCEPCIONES PERSONALIZADAS
# ============================================================

class ClienteError(Exception):
    """
    Excepción base para errores relacionados con clientes.
    """
    pass


class NombreInvalidoError(ClienteError):
    """
    Se lanza cuando el nombre del cliente no es válido.
    """
    pass


class IdentificacionInvalidaError(ClienteError):
    """
    Se lanza cuando la identificación del cliente no es válida.
    """
    pass


class TelefonoInvalidoError(ClienteError):
    """
    Se lanza cuando el teléfono del cliente no es válido.
    """
    pass


class EmailInvalidoError(ClienteError):
    """
    Se lanza cuando el correo electrónico del cliente no es válido.
    """
    pass


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


# ============================================================
# PRUEBAS DE FUNCIONAMIENTO
# ============================================================

if __name__ == "__main__":

    clientes = []

    datos_clientes = [
        {
            "nombre": "Laura Martínez",
            "identificacion": "1023456789",
            "telefono": "3001234567",
            "email": "laura@email.com"
        },
        {
            "nombre": "Carlos Pérez",
            "identificacion": "987654321",
            "telefono": "3119876543",
            "email": "carlos@email.com"
        },
        {
            "nombre": "Ana",
            "identificacion": "12345678",
            "telefono": "3204567890",
            "email": "ana@email.com"
        },
        {
            "nombre": "Lu",
            "identificacion": "123456",
            "telefono": "3000000000",
            "email": "lu@email.com"
        },
        {
            "nombre": "Pedro123",
            "identificacion": "123456789",
            "telefono": "3001112233",
            "email": "pedro@email.com"
        },
        {
            "nombre": "María Gómez",
            "identificacion": "ABC123",
            "telefono": "3002223344",
            "email": "maria@email.com"
        },
        {
            "nombre": "Sofía Torres",
            "identificacion": "1234567890",
            "telefono": "12345",
            "email": "sofia@email.com"
        },
        {
            "nombre": "Andrés Rojas",
            "identificacion": "1234567890",
            "telefono": "3015557788",
            "email": "correo_invalido"
        }
    ]

    print("===== REGISTRO DE CLIENTES SOFTWARE FJ =====\n")

    for datos in datos_clientes:
        try:
            cliente = Cliente(
                datos["nombre"],
                datos["identificacion"],
                datos["telefono"],
                datos["email"]
            )

        except ClienteError as error:
            print(f"No se pudo registrar el cliente: {error}")

        except Exception as error:
            print(f"Error grave no controlado: {error}")

        else:
            clientes.append(cliente)
            print("Cliente registrado correctamente:")
            print(cliente.mostrar_informacion())
            print("-" * 40)

        finally:
            print("Proceso de registro finalizado.\n")

    print("===== CLIENTES REGISTRADOS EXITOSAMENTE =====")

    for cliente in clientes:
        print(cliente)

    print("\n===== PRUEBA DE ACTUALIZACIÓN =====")

    try:
        clientes[0].actualizar_datos(
            telefono="3109998888",
            email="laura.nuevo@email.com"
        )

        print("Datos actualizados correctamente:")
        print(clientes[0].mostrar_informacion())

    except ClienteError as error:
        print(f"No se pudo actualizar el cliente: {error}")

    print("\nRevisa el archivo 'software_fj.log' para ver los eventos y errores registrados.")


class Validador:
    @staticmethod
    def validar_texto(valor, nombre_campo):
        if not isinstance(valor, str) or len(valor.strip()) < 5:
            raise ValidacionError(f"El campo '{nombre_campo}' debe ser texto y tener al menos 3 caracteres.")
        return valor.strip()

    @staticmethod
    def validar_positivo(valor, nombre_campo):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValidacionError(f"El valor de '{nombre_campo}' debe ser un número positivo.")
        return valor

@staticmethod
def validar_correo(correo):
        if "@" not in correo or "." not in correo:
            raise ValidacionError(f"El formato de correo '{correo}' es inválido.")
        return correo

# ============================================================
# EXCEPCION PARA LOS SERVICIOS
# ============================================================

class ServicioError(Exception):
    """Excepcion base para los errores relacionados con los servicios"""
    pass

# ============================================================
# CLASE ABSTRACTA PARA EL SERVICIO
# ============================================================

class Servicio(ABC):
    """
    Clase abstracta que define la plantilla para todos los servicios mencionados
    """
    @abstractmethod
    def calcular_costo(self, duracion):
        """Calculamos el costo total del servicio segun la duracion"""
        pass
    @abstractmethod
    def describir(self):
        """ Nos Devuelve una descripcion del servicio"""
        pass
    @abstractmethod
    def validar_parametros(self, duracion):
        """Validamos los parametros especificos del servicio"""
        pass

# ============================================================
# SERVICIO 1: RESERVA DE LA SALA
# ============================================================

class ReservaSala(Servicio):
    def __init__(self, nombre_sala, costo_por_hora=50):
        self.nombre_sala = nombre_sala
        self.costo_por_hora = costo_por_hora
        registrar_log("EVENTO", f"Servicio creado: ReservaSala - {nombre_sala}")

    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise ServicioError("¡Error! La duracion debe ser mayor a 0h")
        if duracion > 8:
            raise ServicioError("¡Error! No se puede reservar una sala por mas de 8 horas seguidas")
        return True

    def calcular_costo(self, duracion):
        try:
            self.validar_parametros(duracion)
            costo = self.costo_por_hora * duracion
            registrar_log("EVENTO", f"Calculo de costo ReservaSala: {costo} para {duracion} hora(s)")
            return costo
        except ServicioError as e:
            registrar_log("ERROR", f"Error al calcular costo de ReservaSala: {e}")
            raise
        except Exception as e:
            registrar_log("ERROR", f"Error inesperado en ReservaSala: {e}")
            raise ServicioError("¡Error en calculo de costo!") from e

    def describir(self):
        return f"Reserva de sala '{self.nombre_sala}' - ${self.costo_por_hora}/hora"

# ============================================================
# SERVICIO 2: ALQUILER DEL EQUIPO
# ============================================================

class AlquilerEquipo(Servicio):
    def __init__(self, nombre_equipo, costo_por_dia=30):
        self.nombre_equipo = nombre_equipo
        self.costo_por_dia = costo_por_dia
        registrar_log("EVENTO", f"Servicio creado: AlquilerEquipo - {nombre_equipo}")

    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise ServicioError("¡Error! Los dias de alquiler deben ser positivos")
        if duracion > 30:
            raise ServicioError("¡Error! No se puede alquilar por mas de 30 dias")
        return True

    def calcular_costo(self, duracion):
        try:
            self.validar_parametros(duracion)
            costo = self.costo_por_dia * duracion
            registrar_log("EVENTO", f"Calculo de costo AlquilerEquipo: {costo} para {duracion} dia(s)")
            return costo
        except ServicioError as e:
            registrar_log("ERROR", f"Error al calcular costo de AlquilerEquipo: {e}")
            raise
        except Exception as e:
            registrar_log("ERROR", f"Error inesperado en AlquilerEquipo: {e}")
            raise ServicioError("¡Error en calculo de costo!") from e

    def describir(self):
        return f"Alquiler de equipo '{self.nombre_equipo}' - ${self.costo_por_dia}/doa"

# ============================================================
# SERVICIO 3: ASESORIA ESPECIALIZADA
# ============================================================

class Asesoria(Servicio):
    def __init__(self, tema, costo_por_hora=80):
        self.tema = tema
        self.costo_por_hora = costo_por_hora
        registrar_log("EVENTO", f"Servicio creado: Asesoria - {tema}")

    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise ServicioError("¡Error! La duracion de la asesoria debe ser mayor a 0h")
        if duracion > 4:
            raise ServicioError("¡Error! Las asesorias no pueden durar mas de 4h")
        return True

    def calcular_costo(self, duracion):
        try:
            self.validar_parametros(duracion)
            costo = self.costo_por_hora * duracion
            registrar_log("EVENTO", f"Calculo de costo Asesoria: {costo} para {duracion} hora(s)")
            return costo
        except ServicioError as e:
            registrar_log("ERROR", f"Error al calcular costo de Asesoria: {e}")
            raise
        except Exception as e:
            registrar_log("ERROR", f"Error inesperado en Asesoria: {e}")
            raise ServicioError("¡Error en calculo de costo!") from e

    def describir(self):
        return f"Asesoria sobre '{self.tema}' - ${self.costo_por_hora}/hora"