"""Ejercicio 2: catálogo de dispositivos ecológicos."""

try:  # Importación como paquete desde la raíz del repositorio.
    from .excepciones import StockInvalidoError
    from .inventario import GestorInventario
    from .modelos import DispositivoEcologico, PanelSolar
except ImportError:  # Ejecución desde el directorio del ejercicio.
    from excepciones import StockInvalidoError
    from inventario import GestorInventario
    from modelos import DispositivoEcologico, PanelSolar

__all__ = [
    "StockInvalidoError",
    "DispositivoEcologico",
    "PanelSolar",
    "GestorInventario",
]
