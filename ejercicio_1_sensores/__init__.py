"""Ejercicio 1: sanitización y análisis estadístico de sensores."""

try:  # Importación como paquete desde la raíz del repositorio.
    from .sensores import generar_resumen_sensores, limpiar_registro_sensor
except ImportError:  # Ejecución desde el directorio del ejercicio.
    from sensores import generar_resumen_sensores, limpiar_registro_sensor

__all__ = ["limpiar_registro_sensor", "generar_resumen_sensores"]
