"""Vistas del panel de sustentabilidad."""

from django.shortcuts import render

try:  # Importación como paquete dentro del proyecto Django.
    from .metricas import obtener_metricas_consumo, obtener_registros_consumo
except ImportError:  # Ejecución directa del módulo.
    from metricas import obtener_metricas_consumo, obtener_registros_consumo


def vista_panel_sustentabilidad(request):
    """Renderiza el panel con las métricas de emisiones por planta."""
    registros = obtener_registros_consumo()
    metricas = obtener_metricas_consumo(registros)

    contexto = {
        "metricas": metricas,
    }

    return render(
        request,
        "sustentabilidad/panel.html",
        contexto,
    )
