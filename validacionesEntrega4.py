import logging
from abc import ABC, abstractmethod
from datetime import datetime

def registrar_log(tipo, mensaje):

   #Registra eventos y errores en un archivo de logs.

    try:
        with open("software_fj.log", "a", encoding="utf-8") as archivo:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo.write(f"[{fecha}] [{tipo}] {mensaje}\n")
    except Exception as error:
        print(f"No se pudo escribir en el archivo de logs: {error}")



# EXCEPCIONES PERSONALIZADAS

class ClienteError(Exception):
    #Excepción base para errores relacionados con clientes.
    pass

class NombreInvalidoError(ClienteError):
    #Se lanza cuando el nombre del cliente no es válido.
    pass

class IdentificacionInvalidaError(ClienteError):
    #Se lanza cuando la identificación del cliente no es válida
    pass

class TelefonoInvalidoError(ClienteError):
    #Se lanza cuando el teléfono del cliente no es válido.
    pass

class EmailInvalidoError(ClienteError):
    #Se lanza cuando el correo electrónico del cliente no es válido.
    pass

class ValidacionError(Exception): 
    #Se lanza cuando un dato general no cumple con los criterios mínimos de validación.
    pass

class ParametroFaltanteError(Exception): 
    #Se lanza cuando falta un parámetro u objeto obligatorio para completar una operación.
    pass

class OperacionNoPermitidaError(Exception): 
    #Se lanza cuando se intenta realizar un cambio de estado inválido (ej. confirmar una reserva cancelada).
    pass

class ReservaIncorrectaError(Exception): 
    #Se lanza cuando falla el proceso de creación o gestión de una reserva.
    pass

class ServicioNoDisponibleError(Exception): 
    #Se lanza cuando se intenta reservar un servicio que se encuentra inactivo o en mantenimiento.
    pass

class CalculoInconsistenteError(Exception): 
    #Se lanza cuando los parámetros ingresados generan cálculos matemáticos erróneos o negativos.
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
    


# EXCEPCIONES NECESARIAS PARA LAS OPERACIONES

class Servicio(EntidadSistema):
    def __init__(self, id_servicio, nombre, costo_base, disponible=True):
        self.id_servicio = id_servicio
        self.nombre = Validador.validar_texto(nombre, "Nombre del Servicio")
        self.costo_base = Validador.validar_positivo(costo_base, "Costo Base")
        self.disponible = disponible

    @abstractmethod
    def calcular_costo(self, cantidad):
        pass
        
    def mostrar_informacion(self):
        estado = "Disponible" if self.disponible else "No Disponible"
        return f"Servicio [{self.id_servicio}]: {self.nombre} - {estado} - Costo Base: ${self.costo_base}"

class ReservaSala(Servicio):
    def calcular_costo(self, horas):
        horas_validas = Validador.validar_positivo(horas, "Horas de reserva")
        return self.costo_base * horas_validas

class AlquilerEquipo(Servicio):
    def calcular_costo(self, dias):
        dias_validos = Validador.validar_positivo(dias, "Días de alquiler")
        return self.costo_base * dias_validos

class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, sesiones):
        sesiones_validas = Validador.validar_positivo(sesiones, "Número de sesiones")
        return self.costo_base * sesiones_validas

class Reserva(EntidadSistema):
    def __init__(self, cliente, servicio, cantidad):
        try:
            if cliente is None:
                raise ParametroFaltanteError("No se proporcionó un cliente válido para la reserva.")
            if servicio is None:
                raise ParametroFaltanteError("No se proporcionó un servicio válido para la reserva.")
            if not servicio.disponible:
                raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' se encuentra fuera de servicio.")

            self.cliente = cliente
            self.servicio = servicio
            self.cantidad = cantidad
            self.estado = "Pendiente"
            
            try:
                self.subtotal = self.servicio.calcular_costo(self.cantidad)
            except ValidacionError as e:
                raise CalculoInconsistenteError("Los parámetros dados generan un cálculo inconsistente.") from e

            registrar_log("EVENTO", f"Reserva PENDIENTE creada para {self.cliente.nombre} - Servicio: {self.servicio.nombre}")

        except Exception as error:
            registrar_log("ERROR", f"Fallo al intentar crear reserva: {error}")
            raise ReservaIncorrectaError(f"Intento de reserva incorrecto: {error}") from error

    def calcular_total(self, impuesto=0.0, descuento=0.0):
        if impuesto < 0 or descuento < 0:
            raise CalculoInconsistenteError("El impuesto o descuento no pueden ser valores negativos.")
        
        total = self.subtotal + (self.subtotal * impuesto) - (self.subtotal * descuento)
        return total

    def confirmar(self):
        if self.estado == "Cancelada":
            raise OperacionNoPermitidaError("No se puede confirmar una reserva que ya fue cancelada.")
        if self.estado == "Confirmada":
            raise OperacionNoPermitidaError("La reserva ya se encuentra confirmada.")
        
        self.estado = "Confirmada"
        registrar_log("EVENTO", f"Reserva CONFIRMADA para el cliente {self.cliente.nombre}")

    def cancelar(self):
        if self.estado == "Cancelada":
            raise OperacionNoPermitidaError("La reserva ya se encuentra cancelada.")
        self.estado = "Cancelada"
        registrar_log("EVENTO", f"Reserva CANCELADA para el cliente {self.cliente.nombre}")

    def mostrar_informacion(self):
        return f"Reserva de {self.cliente.nombre} | Servicio: {self.servicio.nombre} | Estado: {self.estado} | Subtotal: ${self.subtotal}"

# SIMULACIÓN DE 10 OPERACIONES COMPLETAS

if __name__ == "__main__":
    print("="*60)
    print("INICIANDO SIMULACIÓN DE 10 OPERACIONES - SOFTWARE FJ")
    print("="*60)

    # Listas internas para almacenamiento sin BD
    clientes_db = []
    servicios_db = []
    reservas_db = []

    # Operación 1: Registro Válido de Cliente ---
    print("\n[Operación 1] Intentando realizar registro de cliente válido...")
    try:
        c1 = Cliente("Laura Martinez", "1023456789", "3001234567", "laura@email.com")
    except Exception as e:
        print(f"Error: {e}")
    else:
        clientes_db.append(c1)
        print("Éxito:", c1.mostrar_informacion())
    finally:
        print("Fin de Operación 1")

    # Operación 2: Registro Inválido de Cliente (Datos erróneos) ---
    print("\n[Operación 2] Intentando registrar cliente con datos inválidos (Letras en Teléfono)...")
    try:
        c2 = Cliente("Carlos Perez", "987654321", "TRES119876", "carlos@email.com")
    except TelefonoInvalidoError as e:
        print(f"Excepción controlada correctamente: {e}")
    except Exception as e:
        print(f"Error grave: {e}")
    finally:
        print("Fin de Operación 2")

    # Operación 3: Creación Correcta de Servicio ---
    print("\n[Operación 3] Creando servicio de Reserva de Sala...")
    try:
        s_sala = ReservaSala("S01", "Sala de Juntas Principal", 50000)
        servicios_db.append(s_sala)
        print("Éxito:", s_sala.mostrar_informacion())
    except Exception as e:
        print(f"Error: {e}")

    # Operación 4: Creación Incorrecta de Servicio (Valor negativo) ---
    print("\n[Operación 4] Creando servicio con costo negativo...")
    try:
        s_error = AlquilerEquipo("E01", "Proyector 4K", -15000)
    except ValidacionError as e:
        print(f"Excepción controlada correctamente: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

    # Operación 5: Creación de Servicio No Disponible ---
    print("\n[Operación 5] Creando servicio en mantenimiento (No disponible)...")
    s_asesoria = AsesoriaEspecializada("A01", "Asesoría Arquitectura Cloud", 120000, disponible=False)
    servicios_db.append(s_asesoria)
    print("Éxito:", s_asesoria.mostrar_informacion())

    # Operación 6: Reserva Exitosa ---
    print("\n[Operación 6] Creando reserva válida para Laura (3 horas de Sala)...")
    try:
        r1 = Reserva(clientes_db[0], servicios_db[0], 3)
        reservas_db.append(r1)
        print("Éxito:", r1.mostrar_informacion())
    except ReservaIncorrectaError as e:
        print(f"Error de reserva: {e}")

    # Operación 7: Intento de Reserva con Parámetros Inconsistentes ---
    print("\n[Operación 7] Intentando reservar sala con horas negativas...")
    try:
        r_mala = Reserva(clientes_db[0], servicios_db[0], -5)
    except ReservaIncorrectaError as e:
        # Aquí demostramos el encadenamiento de excepciones (__cause__)
        print(f"Excepción controlada: {e}")
        print(f"Causa original subyacente: {e.__cause__}")

    # Operación 8: Reserva de Servicio No Disponible ---
    print("\n[Operación 8] Intentando reservar la Asesoría que no está disponible...")
    try:
        r_nodisp = Reserva(clientes_db[0], servicios_db[1], 2)
    except ReservaIncorrectaError as e:
        print(f"Excepción controlada: {e}")

    # Operación 9: Operación No Permitida (Confirmar lo cancelado) ---
    print("\n[Operación 9] Probando transiciones de estado de reserva...")
    try:
        reservas_db[0].cancelar()
        print("Reserva cancelada con éxito.")
        print("Intentando confirmar la reserva recién cancelada...")
        reservas_db[0].confirmar() # Esto debe fallar
    except OperacionNoPermitidaError as e:
        print(f"Excepción controlada: {e}")

    # Operación 10: Cálculos con Sobrecarga e Inconsistencias ---
    print("\n[Operación 10] Calculando costos con parámetros opcionales (Sobrecarga)...")
    try:
        # Restauramos estado para la prueba
        reservas_db[0].estado = "Pendiente" 
        
        # Uso normal: 19% impuesto, 10% descuento
        total_ok = reservas_db[0].calcular_total(impuesto=0.19, descuento=0.10)
        print(f"Cálculo correcto (Impuestos y descuentos): ${total_ok}")
        
        # Uso con datos inconsistentes (impuesto negativo)
        print("Intentando calcular con impuesto negativo...")
        reservas_db[0].calcular_total(impuesto=-0.05)
    except CalculoInconsistenteError as e:
        print(f"Excepción controlada: {e}")
    finally:
        print("\n" + "="*60)
        print("SIMULACIÓN FINALIZADA. Revisa el archivo 'software_fj.log'")
        print("="*60)
