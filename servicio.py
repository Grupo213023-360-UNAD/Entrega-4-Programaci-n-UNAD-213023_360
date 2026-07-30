"""
Módulo de servicios del sistema Software FJ.

Define la clase abstracta Servicio y sus tres implementaciones
concretas: ReservaSala, AlquilerEquipo y AsesoriaEspecializada,
además de la clase auxiliar Validador, que centraliza reglas de
validación reutilizables entre los distintos tipos de servicio.
"""

from abc import ABC, abstractmethod
from cliente import EntidadSistema
from excepciones import ValidacionError
from logger import registrar_log


# ============================================================
# VALIDADOR
# ============================================================

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
# CLASE ABSTRACTA SERVICIO
# ============================================================

class Servicio(EntidadSistema, ABC):
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


# ============================================================
# SERVICIO RESERVA SALA
# ============================================================

class ReservaSala(Servicio):
    def __init__(self, id_servicio, nombre, costo_base, disponible=True, capacidad_maxima=50):
        super().__init__(id_servicio, nombre, costo_base, disponible)
        self.capacidad_maxima = capacidad_maxima

    def calcular_costo(self, horas):
        horas_validas = Validador.validar_positivo(horas, "Horas de reserva")
        return self.costo_base * horas_validas

    # ========================================================
    # MÉTODOS SOBRECARGADOS 
    # ========================================================
    
    def calcular_costo_con_descuento(self, horas, porcentaje_descuento):
        """
        Método sobrecargado: calcula costo con descuento.
        """
        costo_normal = self.calcular_costo(horas)
        descuento = costo_normal * (porcentaje_descuento / 100)
        return costo_normal - descuento

    def describir(self):
        """
        Método para describir el servicio (requerimiento del ejercicio).
        """
        return f"Reserva de Sala - {self.nombre}: Capacidad para {self.capacidad_maxima} personas, Precio base: ${self.costo_base:.2f} por hora."

    def validar_parametros(self, horas=None, personas=None):
        """
        Validación específica para reserva de sala.
        """
        if horas is not None and horas > 24:
            raise ValidacionError("La duración máxima es 24 horas.")
        if personas is not None and personas > self.capacidad_maxima:
            raise ValidacionError(f"La sala solo tiene capacidad para {self.capacidad_maxima} personas.")
        return True


# ============================================================
# SERVICIO ALQUILER EQUIPO
# ============================================================

class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio, nombre, costo_base, disponible=True, tipo_equipo="Genérico", requiere_seguro=False):
        super().__init__(id_servicio, nombre, costo_base, disponible)
        self.tipo_equipo = tipo_equipo  
        self.requiere_seguro = requiere_seguro  
    def calcular_costo(self, dias):
        dias_validos = Validador.validar_positivo(dias, "Días de alquiler")
        costo = self.costo_base * dias_validos
        if self.requiere_seguro:
            costo += 2000 * dias_validos  # Costo adicional por seguro
        return costo

    # ========================================================
    # MÉTODOS SOBRECARGADOS
    # ========================================================
    
    def calcular_costo_cantidad(self, dias, cantidad=1):
        """
        Método sobrecargado: calcula costo para múltiples equipos.
        """
        dias_validos = Validador.validar_positivo(dias, "Días de alquiler")
        cantidad_validos = Validador.validar_positivo(cantidad, "Cantidad")
        costo = self.costo_base * dias_validos * cantidad_validos
        if self.requiere_seguro:
            costo += 2000 * dias_validos * cantidad_validos
        return costo

    def calcular_costo_dia_adicional(self, dias_adicionales):
        """
        Método sobrecargado: cálculo rápido para extensión.
        """
        return self.calcular_costo(dias_adicionales)

    def describir(self):
        """
        Método para describir el servicio.
        """
        seguro_txt = "con seguro incluido" if self.requiere_seguro else "sin seguro"
        return f"Alquiler de Equipo - {self.nombre}: Tipo {self.tipo_equipo}, {seguro_txt}. Precio base: ${self.costo_base:.2f} por día."

    def validar_parametros(self, dias=None, cantidad=None):
        """
        Validación específica para alquiler de equipo.
        """
        if cantidad is not None and cantidad > 10:
            raise ValidacionError("No se pueden alquilar más de 10 equipos del mismo tipo.")
        return True


# ============================================================
# SERVICIO ASESORÍA
# ============================================================

class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio, nombre, costo_base, disponible=True, especialidad="General", nivel_experto="Intermedio"):
        super().__init__(id_servicio, nombre, costo_base, disponible)
        self.especialidad = especialidad  
        self.nivel_experto = nivel_experto 
        self.niveles_validos = ["Básico", "Intermedio", "Avanzado"]

    def calcular_costo(self, sesiones):
        sesiones_validas = Validador.validar_positivo(sesiones, "Número de sesiones")
        
        # Multiplicador según nivel de experto
        multiplicador = {
            "Básico": 1.0,
            "Intermedio": 1.5,
            "Avanzado": 2.0
        }.get(self.nivel_experto, 1.0)
        
        return self.costo_base * sesiones_validas * multiplicador

    # ========================================================
    # MÉTODOS SOBRECARGADOS
    # ========================================================
    
    def calcular_costo_por_hora(self, horas):
        """
        Método sobrecargado: calcula costo por horas en lugar de sesiones.
        """
        horas_validas = Validador.validar_positivo(horas, "Horas")
        multiplicador = {"Básico": 1.0, "Intermedio": 1.5, "Avanzado": 2.0}.get(self.nivel_experto, 1.0)
        return self.costo_base * horas_validas * multiplicador

    def calcular_costo_paquete(self, sesiones, horas_por_sesion):
        """
        Método sobrecargado: costo por paquete de sesiones con descuento.
        """
        costo_por_sesion = self.calcular_costo_por_hora(horas_por_sesion)
        return costo_por_sesion * sesiones * 0.9  # 10% descuento por paquete

    def describir(self):
        """
        Método para describir el servicio.
        """
        return f"Asesoría Especializada - {self.nombre}: Especialidad en {self.especialidad}, nivel {self.nivel_experto}. Precio base: ${self.costo_base:.2f} por sesión."

    def validar_parametros(self, sesiones=None, horas=None):
        """
        Validación específica para asesoría.
        """
        if horas is not None and horas > 8:
            raise ValidacionError("La asesoría no puede durar más de 8 horas continuas.")
        return True
