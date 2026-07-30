"""
Módulo de excepciones personalizadas del sistema Software FJ.

Define una jerarquía propia de excepciones para validar datos de clientes
y reservas, permitiendo capturar y manejar errores de forma específica
en lugar de usar excepciones genéricas de Python.
"""

# EXCEPCIONES PERSONALIZADAS

class ClienteError(Exception):
    # Excepción base para errores relacionados con clientes.
    pass

class NombreInvalidoError(ClienteError):
    # Se lanza cuando el nombre del cliente no es válido.
    pass

class IdentificacionInvalidaError(ClienteError):
    # Se lanza cuando la identificación del cliente no es válida
    pass

class TelefonoInvalidoError(ClienteError):
    # Se lanza cuando el teléfono del cliente no es válido.
    pass

class EmailInvalidoError(ClienteError):
    # Se lanza cuando el correo electrónico del cliente no es válido.
    pass

class ValidacionError(Exception): 
    # Se lanza cuando un dato general no cumple con los criterios mínimos de validación.
    pass

class ParametroFaltanteError(Exception): 
    # Se lanza cuando falta un parámetro u objeto obligatorio para completar una operación.
    pass

class OperacionNoPermitidaError(Exception): 
    # Se lanza cuando se intenta realizar un cambio de estado inválido (ej. confirmar una reserva cancelada).
    pass

class ReservaIncorrectaError(Exception): 
    # Se lanza cuando falla el proceso de creación o gestión de una reserva.
    pass

class ServicioNoDisponibleError(Exception): 
    # Se lanza cuando se intenta reservar un servicio que se encuentra inactivo o en mantenimiento.
    pass

class CalculoInconsistenteError(Exception): 
    # Se lanza cuando los parámetros ingresados generan cálculos matemáticos erróneos o negativos.
    pass
