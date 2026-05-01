import datetime

# ============================================================
# FUNCIÓN DE LOGS 
# ============================================================
def registrar_log(tipo, mensaje):
    """Registra eventos y errores en un archivo de texto externo."""
    try:
        with open("logs_sistema.txt", "a", encoding="utf-8") as archivo:
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo.write(f"[{fecha}] [{tipo}] {mensaje}\n")
    except Exception as e:
        print(f"No se pudo escribir en el log: {e}")

# ============================================================
# EXCEPCIONES PERSONALIZADAS
# ============================================================
class ReservaError(Exception):
    """Excepción base para errores de reserva."""
    pass

class ReservaEstadoError(ReservaError):
    """Se lanza cuando se intenta operar sobre una reserva cancelada o finalizada."""
    pass

# ============================================================
# CLASE RESERVA
# ============================================================
class Reserva:
    def __init__(self, cliente, servicio, duracion):
        """
        Atributos privados para cumplir con el pilar de Encapsulamiento.
        """
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "PENDIENTE"
        self.__costo_total = 0.0

    def procesar_reserva(self):
        """
        Lógica principal con manejo de excepciones (Persona 4).
        """
        print(f"\n--- Iniciando Proceso de Reserva para: {self.__cliente} ---")
        try:
            # Simulamos validación de disponibilidad del servicio
            # (En el código final, esto interactúa con las clases de Persona 2 y 3)
            print(f"Validando disponibilidad de: {self.__servicio}...")
            
            # Cálculo del costo total
            # Nota: Aquí se llamaría al método calcular_costo() del servicio
            self.__costo_total = 50.0 * self.__duracion # Ejemplo base

        except Exception as error:
            self.__estado = "FALLIDA"
            registrar_log("ERROR", f"Fallo en reserva del cliente {self.__cliente}: {error}")
            print(f"Error detectado: {error}")
        
        else:
            self.__estado = "CONFIRMADA"
            registrar_log("EVENTO", f"Reserva exitosa para {self.__cliente}. Total: ${self.__costo_total}")
            print(f"¡Reserva confirmada! Total a pagar: ${self.__costo_total:.2f}")
            
        finally:
            print(f"Operación finalizada. Estado actual: {self.__estado}")

    def cancelar(self):
        """Manejo de estado de la reserva con excepción personalizada."""
        try:
            if self.__estado == "CANCELADA":
                raise ReservaEstadoError(f"La reserva de {self.__cliente} ya se encuentra cancelada.")
            
            self.__estado = "CANCELADA"
            registrar_log("EVENTO", f"Reserva cancelada por el cliente: {self.__cliente}")
            print(f"Reserva de {self.__cliente} ha sido cancelada exitosamente.")
            
        except ReservaEstadoError as e:
            print(f"Aviso de Seguridad: {e}")
            registrar_log("ADVERTENCIA", str(e))

    def mostrar_informacion(self):
        return (f"Reserva: {self.__estado} | Cliente: {self.__cliente} | "
                f"Servicio: {self.__servicio} | Total: ${self.__costo_total}")
    
# ============================================================
# PRUEBA UNITARIA DEL MÓDULO
# ============================================================
if __name__ == "__main__":
    # Prueba rápida de funcionamiento
    mi_reserva = Reserva("Breyner Guerrero", "Alquiler de Computador", 2)
    mi_reserva.procesar_reserva()
    
    # Intento de doble cancelación para probar la excepción
    mi_reserva.cancelar()
    mi_reserva.cancelar()

    