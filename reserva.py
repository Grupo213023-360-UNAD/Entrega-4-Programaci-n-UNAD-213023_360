from cliente import EntidadSistema, Cliente
from servicio import Servicio
from excepciones import (
    ParametroFaltanteError, ServicioNoDisponibleError,
    CalculoInconsistenteError, OperacionNoPermitidaError,
    ReservaIncorrectaError, ValidacionError
)
from logger import registrar_log


# ============================================================
# CLASE RESERVA
# ============================================================

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