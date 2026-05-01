import logging
from abc import ABC, abstractmethod
from datetime import datetime
import math

# ============================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================

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
# EXCEPCIONES PARA SERVICIOS
# ============================================================

class ServicioError(Exception):
    """Excepción base para errores relacionados con servicios."""
    pass


class ServicioNoDisponibleError(ServicioError):
    """Se lanza cuando un servicio no está disponible."""
    pass


class DuracionInvalidaError(ServicioError):
    """Se lanza cuando la duración del servicio no es válida."""
    pass


class ParametroInvalidoError(ServicioError):
    """Se lanza cuando un parámetro del servicio es inválido."""
    pass

# --- NUEVAS EXCEPCIONES PARA RESERVA (Persona 4) ---
class ReservaError(Exception):
    """Excepción base para errores de reserva."""
    pass

class ReservaEstadoError(ReservaError):
    """Se lanza cuando se intenta operar sobre una reserva cancelada o finalizada."""
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
# CLASE ABSTRACTA SERVICIO
# ============================================================

class Servicio(EntidadSistema, ABC):
    """
    Clase abstracta que representa un servicio genérico.
    Todos los servicios específicos heredan de esta clase.
    """

    def __init__(self, nombre_servicio, precio_base_servicio, disponible=True):
        try:
            self.__nombre_servicio = None
            self.__precio_base_servicio = None
            self.__disponible = None

            self.nombre_servicio = nombre_servicio
            self.precio_base_servicio = precio_base_servicio
            self.disponible = disponible

            registrar_log(
                "EVENTO",
                f"Servicio creado: {self.__nombre_servicio} - Precio base: ${self.__precio_base_servicio}"
            )

        except ServicioError as error:
            registrar_log("ERROR", f"Error al crear servicio: {error}")
            raise

        except Exception as error:
            registrar_log("ERROR", f"Error inesperado al crear servicio: {error}")
            raise ServicioError("Ocurrió un error inesperado al crear el servicio.") from error

    # ========================================================
    # GETTERS Y SETTERS
    # ========================================================

    @property
    def nombre_servicio(self):
        return self.__nombre_servicio

    @nombre_servicio.setter
    def nombre_servicio(self, nuevo_nombre_servicio):
        if not isinstance(nuevo_nombre_servicio, str):
            raise ParametroInvalidoError("El nombre debe ser texto.")

        nuevo_nombre_servicio = nuevo_nombre_servicio.strip()

        if len(nuevo_nombre_servicio) < 3:
            raise ParametroInvalidoError("El nombre debe tener mínimo 3 caracteres.")

        self.__nombre_servicio = nuevo_nombre_servicio

    @property
    def precio_base_servicio(self):
        return self.__precio_base_servicio

    @precio_base_servicio.setter
    def precio_base_servicio(self, nuevo_precio):
        try:
            nuevo_precio = float(nuevo_precio)
        except (TypeError, ValueError):
            raise ParametroInvalidoError("El precio debe ser un número válido.")

        if nuevo_precio <= 0:
            raise ParametroInvalidoError("El precio base debe ser mayor a cero.")

        self.__precio_base_servicio = nuevo_precio

    @property
    def disponible(self):
        return self.__disponible

    @disponible.setter
    def disponible(self, estado):
        if not isinstance(estado, bool):
            raise ParametroInvalidoError("La disponibilidad debe ser True o False.")

        self.__disponible = estado

    # ========================================================
    # MÉTODOS ABSTRACTOS
    # ========================================================

    @abstractmethod
    def calcular_costo(self, duracion=None, **kwargs):
        """
        Calcula el costo del servicio.
        Los hijos implementan esta lógica.
        """
        pass

    @abstractmethod
    def describir(self):
        """
        Devuelve una descripción del servicio.
        """
        pass

    @abstractmethod
    def validar_parametros(self, **kwargs):
        """
        Valida los parámetros específicos de cada servicio.
        """
        pass

    # ========================================================
    # MÉTODOS CONCRETOS (implementados)
    # ========================================================

    def mostrar_informacion(self):
        """Implementación del método abstracto de EntidadSistema."""
        estado = "Disponible" if self.__disponible else "No disponible"
        return f"Servicio: {self.__nombre_servicio}\nPrecio base: ${self.__precio_base_servicio:.2f}\nEstado: {estado}"

    def __str__(self):
        return f"{self.__nombre_servicio} - ${self.__precio_base_servicio:.2f}"


# ============================================================
# SERVICIO 1: RESERVA DE SALAS
# ============================================================

class ReservaSala(Servicio):
    """
    Servicio especializado para reservar salas de reuniones.
    """

    def __init__(self, nombre_servicio, precio_base_servicio, capacidad_maxima):
        self.__capacidad_maxima = None

        #inicialización del servicio base
        super().__init__(nombre_servicio, precio_base_servicio)

        # asignación atributos específicos
        self.capacidad_maxima = capacidad_maxima

        registrar_log("EVENTO", f"Servicio de sala creado: {nombre_servicio} - Capacidad: {capacidad_maxima}")

    @property
    def capacidad_maxima(self):
        return self.__capacidad_maxima

    @capacidad_maxima.setter
    def capacidad_maxima(self, capacidad):
        try:
            capacidad = int(capacidad)
        except (TypeError, ValueError):
            raise ParametroInvalidoError("La capacidad debe ser un número entero.")

        if capacidad < 1:
            raise ParametroInvalidoError("La capacidad mínima es 1 persona.")

        if capacidad > 50:
            raise ParametroInvalidoError("La capacidad máxima es 50 personas.")

        self.__capacidad_maxima = capacidad
        

    def validar_parametros(self, duracion=None, personas=None, **kwargs):
        """Valida parámetros específicos para reserva de sala."""
        if duracion is not None:
            try:
                duracion = float(duracion)
            except (TypeError, ValueError):
                raise DuracionInvalidaError("La duración debe ser un número.")

            if duracion <= 0:
                raise DuracionInvalidaError("La duración debe ser mayor a 0 horas.")

            if duracion > 24:
                raise DuracionInvalidaError("La duración máxima es 24 horas.")

        if personas is not None:
            try:
                personas = int(personas)
            except (TypeError, ValueError):
                raise ParametroInvalidoError("El número de personas debe ser un entero.")

            if personas <= 0:
                raise ParametroInvalidoError("Debe haber al menos 1 persona.")

            if personas > self.capacidad_maxima:
                raise ParametroInvalidoError(
                    f"La sala solo tiene capacidad para {self.capacidad_maxima} personas."
                )

        return True

    def calcular_costo(self, duracion=None, **kwargs):
        """
        Calcula costo de reserva de sala.
        Sobrecarga de métodos: si no se da duración, usa 1 hora por defecto.
        """
        # Validar duración
        if duracion is None:
            duracion = 1.0
            registrar_log("EVENTO", "No se especificó duración, usando 1 hora por defecto.")

        self.validar_parametros(duracion=duracion)

        costo = self.precio_base_servicio * duracion

        return costo

    def calcular_costo_con_descuento(self, duracion, porcentaje_descuento):
        """Método sobrecargado: cálculo de costo con descuento."""
        costo_normal = self.calcular_costo(duracion=duracion)
        descuento = costo_normal * (porcentaje_descuento / 100)
        return costo_normal - descuento

    def describir(self):
        return (f"Reserva de Sala - {self.nombre_servicio}: Capacidad para {self.capacidad_maxima} personas, "
                f"Precio base: ${self.precio_base_servicio:.2f} por hora.")

    def mostrar_informacion(self):
        info_base = super().mostrar_informacion()
        return f"{info_base}\nCapacidad máxima: {self.capacidad_maxima} personas"


# ============================================================
# SERVICIO 2: ALQUILER DE EQUIPOS
# ============================================================

class AlquilerEquipo(Servicio):
    """
    Servicio especializado para alquilar equipos tecnológicos.
    """

    def __init__(self, nombre_servicio, precio_base_servicio, tipo_equipo, requiere_seguro=False):
        self.__tipo_equipo = None
        self.__requiere_seguro = None

        super().__init__(nombre_servicio, precio_base_servicio)

        self.tipo_equipo = tipo_equipo
        self.requiere_seguro = requiere_seguro

        registrar_log("EVENTO", f"Servicio de alquiler creado: {nombre_servicio} - Tipo: {tipo_equipo}")

    @property
    def tipo_equipo(self):
        return self.__tipo_equipo

    @tipo_equipo.setter
    def tipo_equipo(self, tipo):
        if not isinstance(tipo, str) or len(tipo.strip()) < 3:
            raise ParametroInvalidoError("El tipo de equipo debe ser texto con al menos 3 caracteres.")

        self.__tipo_equipo = tipo.strip()

    @property
    def requiere_seguro(self):
        return self.__requiere_seguro

    @requiere_seguro.setter
    def requiere_seguro(self, valor):
        if not isinstance(valor, bool):
            raise ParametroInvalidoError("requiere_seguro debe ser True o False.")

        self.__requiere_seguro = valor

    def validar_parametros(self, duracion=None, cantidad=None, **kwargs):
        """Valida parámetros para alquiler de equipo."""
        if duracion is not None:
            try:
                duracion = float(duracion)
            except (TypeError, ValueError):
                raise DuracionInvalidaError("La duración debe ser un número.")

            if duracion <= 0:
                raise DuracionInvalidaError("La duración debe ser mayor a 0 días.")

        if cantidad is not None:
            try:
                cantidad = int(cantidad)
            except (TypeError, ValueError):
                raise ParametroInvalidoError("La cantidad debe ser un número entero.")

            if cantidad <= 0:
                raise ParametroInvalidoError("La cantidad debe ser al menos 1.")

            if cantidad > 10:
                raise ParametroInvalidoError("No se pueden alquilar más de 10 equipos del mismo tipo.")

        return True

    def calcular_costo(self, duracion=None, cantidad=1, **kwargs):
        """
        Calcula costo de alquiler.
        Sobrecarga: cantidad es opcional (default 1), duración opcional (default 1 día).
        """
        if duracion is None:
            duracion = 1.0
            registrar_log("EVENTO", "No se especificó duración, usando 1 día por defecto.")

        self.validar_parametros(duracion=duracion, cantidad=cantidad)

        costo = self.precio_base_servicio * duracion * cantidad

        if self.requiere_seguro:
            costo += 2000 * duracion * cantidad

        return costo

    def calcular_costo_dia_adicional(self, dias_adicionales):
        """Método sobrecargado: cálculo rápido para extensión de alquiler."""
        return self.precio_base_servicio * dias_adicionales

    def describir(self):
        seguro_txt = "con seguro incluido" if self.requiere_seguro else "sin seguro"
        return (f"Alquiler de Equipo - {self.nombre_servicio}: Tipo {self.tipo_equipo}, "
                f"{seguro_txt}. Precio base: ${self.precio_base_servicio:.2f} por día por unidad.")

    def mostrar_informacion(self):
        info_base = super().mostrar_informacion()
        seguro_txt = "Sí" if self.requiere_seguro else "No"
        return f"{info_base}\nTipo de equipo: {self.tipo_equipo}\nRequiere seguro: {seguro_txt}"


# ============================================================
# SERVICIO 3: ASESORÍAS ESPECIALIZADAS
# ============================================================

class AsesoriaEspecializada(Servicio):
    """
    Servicio especializado para asesorías personalizadas.
    """

    def __init__(self, nombre_servicio, precio_base_servicio, especialidad, nivel_experto="Intermedio"):
        self.__especialidad = None
        self.__nivel_experto = None

        self.niveles_validos = ["Básico", "Intermedio", "Avanzado"]

        super().__init__(nombre_servicio, precio_base_servicio)

        self.especialidad = especialidad
        self.nivel_experto = nivel_experto

        registrar_log("EVENTO", f"Servicio de asesoría creado: {nombre_servicio} - Especialidad: {especialidad}")

        

    @property
    def especialidad(self):
        return self.__especialidad

    @especialidad.setter
    def especialidad(self, esp):
        if not isinstance(esp, str) or len(esp.strip()) < 3:
            raise ParametroInvalidoError("La especialidad debe ser texto con al menos 3 caracteres.")

        self.__especialidad = esp.strip()

    @property
    def nivel_experto(self):
        return self.__nivel_experto

    @nivel_experto.setter
    def nivel_experto(self, nivel):
        if nivel not in self.niveles_validos:
            raise ParametroInvalidoError(f"Nivel inválido. Los niveles son: {', '.join(self.niveles_validos)}")

        self.__nivel_experto = nivel

    def validar_parametros(self, duracion=None, **kwargs):
        """Valida parámetros para asesoría."""
        if duracion is not None:
            try:
                duracion = float(duracion)
            except (TypeError, ValueError):
                raise DuracionInvalidaError("La duración debe ser un número.")

            if duracion <= 0:
                raise DuracionInvalidaError("La duración debe ser mayor a 0 horas.")

            if duracion > 8:
                raise DuracionInvalidaError("La asesoría no puede durar más de 8 horas continuas.")

        return True

    def calcular_costo(self, duracion=None, **kwargs):
        """
        Calcula costo de asesoría según nivel del experto.
        """
        if duracion is None:
            duracion = 1.0
            registrar_log("EVENTO", "No se especificó duración, usando 1 hora por defecto.")

        self.validar_parametros(duracion=duracion)

        # Multiplicador según nivel de experto
        multiplicador = {
            "Básico": 1.0,
            "Intermedio": 1.5,
            "Avanzado": 2.0
        }.get(self.nivel_experto, 1.0)

        costo = self.precio_base_servicio * duracion * multiplicador

        return costo

    def calcular_costo_paquete(self, horas, numero_sesiones):
        """Método sobrecargado: costo por paquete de sesiones."""
        costo_por_sesion = self.calcular_costo(duracion=horas)
        return costo_por_sesion * numero_sesiones * 0.9  # 10% descuento por paquete

    def describir(self):
        return (f"Asesoría Especializada - {self.nombre_servicio}: Especialidad en {self.especialidad}, "
                f"nivel {self.nivel_experto}. Precio base: ${self.precio_base_servicio:.2f} por hora.")

    def mostrar_informacion(self):
        info_base = super().mostrar_informacion()
        return f"{info_base}\nEspecialidad: {self.especialidad}\nNivel del experto: {self.nivel_experto}"

def mostrar_informacion(self):
        info_base = super().mostrar_informacion()
        return f"{info_base}\nEspecialidad: {self.__especialidad}\nNivel del experto: {self.__nivel_experto}"

# ============================================================
# CLASE RESERVA
# ============================================================

class Reserva(EntidadSistema):
    def __init__(self, cliente, servicio, duracion):
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "PENDIENTE"
        self.__costo_total = 0.0

    def procesar_reserva(self):
        print(f"\n--- Iniciando Proceso de Reserva para: {self.__cliente.nombre} ---")
        try:
            if not self.__servicio.disponible:
                raise ServicioNoDisponibleError(f"El servicio '{self.__servicio.nombre_servicio}' no está disponible.")

            # Cálculo de costo usando el polimorfismo de la Persona 2 y 3
            self.__costo_total = self.__servicio.calcular_costo(self.__duracion)
            
        except (ServicioError, Exception) as error:
            self.__estado = "FALLIDA"
            registrar_log("ERROR", f"Fallo en reserva: {error}")
            print(f"Error detectado: {error}")
        else:
            self.__estado = "CONFIRMADA"
            registrar_log("EVENTO", f"Reserva exitosa para {self.__cliente.nombre}. Total: ${self.__costo_total}")
            print(f"¡Reserva confirmada! Total a pagar: ${self.__costo_total:.2f}")
        finally:
            print(f"Operación finalizada. Estado actual: {self.__estado}")

    def cancelar(self):
        try:
            if self.__estado == "CANCELADA":
                raise ReservaEstadoError("La reserva ya está cancelada.")
            self.__estado = "CANCELADA"
            registrar_log("EVENTO", f"Reserva cancelada: {self.__cliente.nombre}")
        except ReservaEstadoError as e:
            print(f"Aviso: {e}")

    def mostrar_informacion(self):
        return (f"Reserva: {self.__estado} | Cliente: {self.__cliente.nombre} | "
                f"Servicio: {self.__servicio.nombre_servicio} | Total: ${self.__costo_total}")


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

# ============================================================
# PRUEBAS DE FUNCIONAMIENTO SERVICIOS
# ============================================================

    print("\n" + "="*60)
    print("PRUEBAS DEL MÓDULO DE SERVICIOS")
    print("="*60)

    # Crear lista de servicios
    servicios = []

    # Servicio 1: Reserva de sala
    try:
        sala1 = ReservaSala("Sala Ejecutiva", 30000, 10)
        servicios.append(sala1)
        print("✓ Sala creada:", sala1.mostrar_informacion())
    except ServicioError as e:
        print(f"✗ Error: {e}")

    # Servicio 2: Alquiler de equipo
    try:
        equipo1 = AlquilerEquipo("Laptop Gamer", 25000, "Computadora", True)
        servicios.append(equipo1)
        print("\n✓ Equipo creado:", equipo1.mostrar_informacion())
    except ServicioError as e:
        print(f"✗ Error: {e}")

    # Servicio 3: Asesoría - CORREGIDO: usar "Avanzado" no "nivel_experto"
    try:
        asesoria1 = AsesoriaEspecializada("Python Avanzado", 50000, "Programación", "Avanzado")
        servicios.append(asesoria1)
        print("\n✓ Asesoría creada:", asesoria1.mostrar_informacion())
    except ServicioError as e:
        print(f"✗ Error: {e}")

    # Pruebas de cálculo de costos
    print("\n" + "-"*60)
    print("CÁLCULO DE COSTOS")
    print("-"*60)

    if len(servicios) >= 1:
        print(f"\n{sala1.describir()}")
        print(f"Costo 2 horas: ${sala1.calcular_costo(duracion=2):.2f}")
        print(f"Costo 3 horas con 10% descuento: ${sala1.calcular_costo_con_descuento(3, 10):.2f}")

    if len(servicios) >= 2:
        print(f"\n{equipo1.describir()}")
        print(f"Costo 3 días (2 equipos): ${equipo1.calcular_costo(duracion=3, cantidad=2):.2f}")
        print(f"Costo día adicional: ${equipo1.calcular_costo_dia_adicional(1):.2f}")

    if len(servicios) >= 3:
        print(f"\n{asesoria1.describir()}")
        print(f"Costo 2 horas: ${asesoria1.calcular_costo(duracion=2):.2f}")
        print(f"Paquete 3 sesiones de 2 horas: ${asesoria1.calcular_costo_paquete(2, 3):.2f}")

    # Pruebas con errores
    print("\n" + "-"*60)
    print("PRUEBA DE MANEJO DE ERRORES")
    print("-"*60)

    try:
        sala_invalida = ReservaSala("Sala", 30000, 10)
    except ServicioError as e:
        print(f"✗ Error esperado: {e}")

    try:
        # Esto es solo para demostrar que Servicio es abstracta
        print("\nIntentando instanciar clase abstracta...")
    except Exception as e:
        print(f"✗ Error: {e}")

    try:
        if len(servicios) >= 1:
            sala1.validar_parametros(duracion=25)  # Duración > 24
    except DuracionInvalidaError as e:
        print(f"✗ Error esperado (duración inválida): {e}")

    print("\n✓ Pruebas completadas. Revisa 'software_fj.log' para eventos.")

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
