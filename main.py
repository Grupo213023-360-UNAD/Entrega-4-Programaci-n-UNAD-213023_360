from cliente import Cliente
from servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva
from excepciones import (
    TelefonoInvalidoError, ValidacionError, ReservaIncorrectaError,
    OperacionNoPermitidaError, CalculoInconsistenteError
)


# ============================================================
# PRUEBAS DE FUNCIONAMIENTO DEL CLIENTE
# ============================================================

if __name__ == "__main__":
    # PRIMERA PARTE: PRUEBAS DE CLIENTE
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

        except Exception as error:
            print(f"No se pudo registrar el cliente: {error}")

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

    except Exception as error:
        print(f"No se pudo actualizar el cliente: {error}")

    print("\nRevisa el archivo 'software_fj.log' para ver los eventos y errores registrados.\n")


# ============================================================
# SEGUNDA PARTE: SIMULACIÓN DE 10 OPERACIONES COMPLETAS
# ============================================================

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
        reservas_db[0].confirmar()
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

    
# ============================================================
# TERCERA PARTE: DEMOSTRACIÓN DE MÉTODOS SOBRECARGADOS Y FUNCIONALIDADES AVANZADAS
# ============================================================

    print("\n" + "="*60)
    print("DEMOSTRACIÓN DE MÉTODOS SOBRECARGADOS Y VALIDACIONES AVANZADAS")
    print("="*60)
    print("A continuación se muestran las capacidades extendidas del sistema:")
    print("- Métodos sobrecargados para cálculos alternativos")
    print("- Método describir() para cada tipo de servicio")
    print("- Validaciones específicas por tipo de servicio")
    print("- Atributos adicionales (capacidad, tipo equipo, nivel experto)\n")

    # Creación de servicios con características avanzadas
    print(">>> CREANDO SERVICIOS CON CARACTERÍSTICAS AVANZADAS")
    
    sala_premium = ReservaSala("S02", "Sala Ejecutiva Premium", 80000, capacidad_maxima=15)
    equipo_gamer = AlquilerEquipo("E02", "Laptop Gamer RTX", 45000, tipo_equipo="Computadora", requiere_seguro=True)
    asesoria_avanzada = AsesoriaEspecializada("A02", "Inteligencia Artificial", 120000, especialidad="Machine Learning", nivel_experto="Avanzado")
    
    print("✓ Sala Premium creada (capacidad máxima: 15 personas)")
    print("✓ Laptop Gamer creada (con seguro incluido)")
    print("✓ Asesoría IA creada (nivel Avanzado)\n")

    # Demostración del método describir()
    print(">>> DESCRIPCIÓN DE SERVICIOS (Método describir())")
    print(f"1. {sala_premium.describir()}")
    print(f"2. {equipo_gamer.describir()}")
    print(f"3. {asesoria_avanzada.describir()}\n")

    # Demostración de métodos sobrecargados
    print(">>> MÉTODOS SOBRECARGADOS - RESERVA DE SALA")
    print(f"  Costo normal (3 horas): ${sala_premium.calcular_costo(3):.2f}")
    print(f"  Costo con descuento del 15%: ${sala_premium.calcular_costo_con_descuento(3, 15):.2f}")
    
    print("\n>>> MÉTODOS SOBRECARGADOS - ALQUILER DE EQUIPO")
    print(f"  Costo normal (5 días): ${equipo_gamer.calcular_costo(5):.2f}")
    print(f"  Costo para 3 equipos (5 días): ${equipo_gamer.calcular_costo_cantidad(5, 3):.2f}")
    print(f"  Costo día adicional: ${equipo_gamer.calcular_costo_dia_adicional(1):.2f}")
    
    print("\n>>> MÉTODOS SOBRECARGADOS - ASESORÍA ESPECIALIZADA")
    print(f"  Costo normal (3 sesiones): ${asesoria_avanzada.calcular_costo(3):.2f}")
    print(f"  Costo por horas (4 horas): ${asesoria_avanzada.calcular_costo_por_hora(4):.2f}")
    print(f"  Paquete 5 sesiones de 2 horas c/u: ${asesoria_avanzada.calcular_costo_paquete(5, 2):.2f}")

    # Demostración de validaciones
    print("\n>>> VALIDACIONES ESPECÍFICAS POR SERVICIO")
    
    print("\n  Validación de sala (capacidad excedida):")
    try:
        sala_premium.validar_parametros(horas=2, personas=20)
        print("Parámetros válidos")
    except ValidacionError as e:
        print(f"Error controlado: {e}")
    
    print("\n  Validación de equipo (cantidad excedida):")
    try:
        equipo_gamer.validar_parametros(dias=3, cantidad=12)
        print("Parámetros válidos")
    except ValidacionError as e:
        print(f"Error controlado: {e}")
    
    print("\n  Validación de asesoría (duración excedida):")
    try:
        asesoria_avanzada.validar_parametros(horas=10)
        print("Parámetros válidos")
    except ValidacionError as e:
        print(f"Error controlado: {e}")

    # Demostración de reserva con servicios extendidos
    print("\n>>> RESERVA CON SERVICIO EXTENDIDO")
    try:
        cliente_ejemplo = Cliente("Usuario Prueba", "999999999", "3112223344", "test@email.com")
        reserva_extendida = Reserva(cliente_ejemplo, sala_premium, 2)
        print(f"Reserva creada: {reserva_extendida.mostrar_informacion()}")
        reserva_extendida.confirmar()
        print("Reserva confirmada exitosamente")
    except Exception as e:
        print(f"Error en reserva: {e}")

    print("\n" + "="*60)
    print("DEMOSTRACIÓN COMPLETADA - TODAS LAS FUNCIONALIDADES OPERATIVAS")
    print("="*60)
    print("\nTodas las operaciones han sido registradas en 'software_fj.log'")
    print("="*60)