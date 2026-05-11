import logging
from datetime import datetime

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