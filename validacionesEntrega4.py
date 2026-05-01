import logging
from abc import ABC, abstractmethod
from datetime import datetime

    # Configuración del log de errores
logging.basicConfig(
    filename='software_fj_errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

#Clase base para excepciones.
class SoftwareFJError(Exception):
    pass

    #Se lanza cuando los datos de entrada no cumplen el formato.
class ValidacionError(SoftwareFJError):
    pass
    #Se lanza cuando una acción (reserva/cancelación) no es permitida.
class OperacionInvalidaError(SoftwareFJError):
    pass


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