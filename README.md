# Sistema de Gestión de Servicios — Software FJ

Proyecto académico desarrollado como Entrega 4 del curso de Programación (UNAD, 213023_360). Simula el sistema de reservas de una empresa ficticia ("Software FJ") que ofrece tres tipos de servicios: reserva de salas, alquiler de equipos y asesoría especializada.

Todos los clientes, identificaciones y datos de prueba usados en `main.py` son **ficticios**, generados únicamente para validar el funcionamiento del sistema.

## Objetivo

Aplicar los principios de Programación Orientada a Objetos (POO) vistos en el curso: clases abstractas, herencia, encapsulamiento, sobrecarga de métodos y manejo de excepciones personalizadas, en un caso de uso realista de gestión de reservas y servicios.

## Arquitectura

El sistema está organizado en módulos independientes, cada uno con una responsabilidad clara:

| Módulo | Responsabilidad |
|---|---|
| `cliente.py` | Define la clase abstracta `EntidadSistema` y la clase `Cliente`, con atributos privados, propiedades (getters/setters) y validaciones. |
| `servicio.py` | Define la clase abstracta `Servicio` y sus tres implementaciones concretas: `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada`, además de la clase auxiliar `Validador`. |
| `reserva.py` | Define la clase `Reserva`, que asocia un `Cliente` con un `Servicio`, gestiona su estado (Pendiente / Confirmada / Cancelada) y calcula el costo total con impuestos y descuentos. |
| `excepciones.py` | Jerarquía de excepciones personalizadas para validar datos del cliente y de las reservas. |
| `logger.py` | Registra en `software_fj.log` cada operación relevante del sistema, con marca de tiempo. |
| `main.py` | Script de demostración: crea clientes y servicios de prueba, ejecuta reservas y muestra el manejo de errores. |

### Diagrama de clases (texto)

```
EntidadSistema (ABC)
   └── Cliente

Servicio (ABC)
   ├── ReservaSala
   ├── AlquilerEquipo
   └── AsesoriaEspecializada

Reserva
   ├── usa → Cliente
   └── usa → Servicio

ClienteError (Exception)
   ├── NombreInvalidoError
   ├── IdentificacionInvalidaError
   ├── TelefonoInvalidoError
   └── EmailInvalidoError

Otras excepciones: ValidacionError, ParametroFaltanteError,
OperacionNoPermitidaError, ReservaIncorrectaError,
ServicioNoDisponibleError, CalculoInconsistenteError
```

### Principios de POO aplicados

- **Abstracción:** `EntidadSistema` y `Servicio` son clases abstractas (ABC) que obligan a las subclases a implementar sus propios métodos.
- **Encapsulamiento:** atributos privados (`__nombre`, `__identificacion`, etc.) expuestos mediante propiedades con validación.
- **Herencia:** `Cliente` hereda de `EntidadSistema`; `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada` heredan de `Servicio`.
- **Sobrecarga de métodos (simulada):** métodos como `calcular_costo_con_descuento` y `calcular_costo_cantidad` aceptan distintos parámetros para adaptarse a cada tipo de servicio.
- **Manejo de excepciones:** validaciones específicas con una jerarquía de excepciones propia, incluyendo encadenamiento (`raise ... from error`).

## Estructura del repositorio

```
Entrega-4-Programaci-n-UNAD-213023_360/
├── README.md
├── docs/
│   └── arquitectura.md
├── .gitignore
├── cliente.py
├── servicio.py
├── reserva.py
├── excepciones.py
├── logger.py
├── main.py
└── software_fj.log
```

## Cómo ejecutarlo

1. Clonar el repositorio.
2. Asegurarse de tener Python 3.9+ instalado (no requiere librerías externas).
3. Ejecutar:

```bash
python main.py
```

4. El script mostrará en consola la simulación de registro de clientes, creación de servicios y reservas, y generará un archivo `software_fj.log` con el detalle de cada operación.

## Resultado esperado

La consola muestra el resultado de 10 operaciones de prueba (registro de clientes válidos e inválidos, creación de reservas, cálculo de costos con descuentos e impuestos, y manejo de errores controlados mediante las excepciones personalizadas).

## Contexto académico

Este repositorio corresponde a una entrega grupal del programa de Ingeniería de Sistemas (UNAD). Los datos de clientes y servicios son ficticios y se usan exclusivamente con fines de evaluación del curso.
