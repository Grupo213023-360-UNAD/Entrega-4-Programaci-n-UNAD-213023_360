# Arquitectura del Sistema — Software FJ

Este documento amplía el diseño orientado a objetos aplicado en el proyecto, complementando el resumen del README principal.

## 1. Capa de entidades (`cliente.py`)

- `EntidadSistema` es una clase abstracta (hereda de `ABC`) que define el contrato mínimo que debe cumplir cualquier entidad registrable en el sistema.
- `Cliente` implementa ese contrato. Sus atributos (`__nombre`, `__identificacion`, `__telefono`, `__email`) son privados y solo se accede a ellos mediante propiedades (`@property` / `@<atributo>.setter`), lo que permite validar cada valor antes de asignarlo (por ejemplo, formato de email o longitud del nombre).
- Cualquier valor inválido lanza una excepción específica de `excepciones.py` (por ejemplo `EmailInvalidoError`), en lugar de un error genérico.

## 2. Capa de servicios (`servicio.py`)

- `Servicio` es la clase abstracta base. Declara los métodos que toda oferta de la empresa debe implementar: describir el servicio, validar sus parámetros y calcular su costo.
- Tres subclases concretas modelan los servicios reales del negocio ficticio:
  - `ReservaSala`: calcula el costo según horas reservadas y aplica descuentos por volumen.
  - `AlquilerEquipo`: calcula el costo según cantidad de equipos y días de alquiler.
  - `AsesoriaEspecializada`: calcula el costo según horas de asesoría y nivel de especialización.
- La clase `Validador` centraliza reglas de validación reutilizables (por ejemplo, verificar que un número sea positivo), evitando duplicar lógica en cada subclase.
- La "sobrecarga" de métodos se simula con parámetros opcionales y `*args`/`**kwargs`, ya que Python no soporta sobrecarga nativa como otros lenguajes tipados.

## 3. Capa de reservas (`reserva.py`)

- `Reserva` es la clase que conecta a un `Cliente` con un `Servicio` y gestiona su ciclo de vida mediante un estado simple (Pendiente → Confirmada / Cancelada).
- `calcular_total()` aplica impuesto y descuento sobre el costo base que entrega el `Servicio` asociado.
- Los errores de cálculo o de estado inválido se relanzan como excepciones propias (`ReservaIncorrectaError`, `CalculoInconsistenteError`) usando `raise ... from error` para conservar la traza original.

## 4. Manejo de errores (`excepciones.py`)

Se definió una jerarquía propia en lugar de usar excepciones genéricas de Python, lo que permite capturar errores de forma selectiva:

- `ClienteError` agrupa los errores de datos de cliente (`NombreInvalidoError`, `IdentificacionInvalidaError`, `TelefonoInvalidoError`, `EmailInvalidoError`).
- Excepciones independientes cubren otros escenarios: parámetros faltantes, operaciones no permitidas, reservas incorrectas, servicios no disponibles e inconsistencias de cálculo.

## 5. Trazabilidad (`logger.py`)

- `registrar_log(tipo, mensaje)` centraliza el registro de eventos en `software_fj.log`, con marca de tiempo, para poder auditar qué operaciones se ejecutaron durante una corrida del programa.

## 6. Orquestación (`main.py`)

- Actúa como script de demostración: crea clientes y servicios de prueba (todos ficticios), ejecuta reservas y muestra en consola tanto los casos exitosos como el manejo controlado de errores.
- No contiene lógica de negocio propia: delega todo el trabajo a las clases de los demás módulos, lo cual mantiene una separación clara de responsabilidades.

## Por qué este diseño

Separar el proyecto en módulos por responsabilidad (entidades, servicios, reservas, excepciones, logging y orquestación) facilita mantener, probar y extender el sistema — por ejemplo, agregar un nuevo tipo de servicio implica solo crear una nueva subclase de `Servicio`, sin modificar el resto del código.
