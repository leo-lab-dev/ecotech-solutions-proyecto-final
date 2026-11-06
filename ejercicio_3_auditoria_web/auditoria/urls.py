"""Rutas de la aplicación de auditoría."""

from django.urls import path

try:  # Importación como paquete dentro del proyecto Django.
    from .views import vista_panel_sustentabilidad
except ImportError:  # Ejecución directa del módulo.
    from views import vista_panel_sustentabilidad

app_name = "auditoria"

urlpatterns = [
    path(
        "sustentabilidad/",
        vista_panel_sustentabilidad,
        name="panel_sustentabilidad",
    ),
]
