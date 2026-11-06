"""Procesamiento de métricas de consumo y emisiones por planta."""

from __future__ import annotations

from typing import Any

try:  # Importación como paquete dentro del proyecto Django.
    from .emisiones import calcular_emisiones_carbono
except ImportError:  # Ejecución directa del módulo.
    from emisiones import calcular_emisiones_carbono

REGISTROS_CONSUMO_SIMULADOS = [
    {"planta": "Planta Norte", "consumo_kwh": 1500},
    {"planta": "Planta Sur", "consumo_kwh": 2500},
    {"planta": "Planta Este", "consumo_kwh": 1000},
    {"planta": "Planta Norte", "consumo_kwh": 500},
]


def obtener_registros_consumo() -> list[dict[str, Any]]:
    """Devuelve el historial de consumos simulado para el panel."""
    return [registro.copy() for registro in REGISTROS_CONSUMO_SIMULADOS]


def obtener_metricas_consumo(
    registros: list[dict[str, Any]],
) -> dict[str, Any]:
    """Calcula las métricas globales y por planta del historial de consumos.

    La planta de mayor consumo se determina comparando el consumo acumulado de
    cada planta. En caso de empate se conserva la primera planta encontrada.

    Args:
        registros: Lista de diccionarios con ``planta`` y ``consumo_kwh``.

    Returns:
        Diccionario con ``total_emisiones``, ``planta_mayor_consumo``,
        ``consumo_mayor_planta`` y ``emisiones_por_planta``. Para un historial
        vacío, ``planta_mayor_consumo`` es ``None`` y los valores numéricos son
        ``0.0``.

    Raises:
        ValueError: si un registro no indica la planta o el consumo no es válido.
    """
    consumos_por_planta: dict[str, float] = {}
    emisiones_por_planta: dict[str, float] = {}

    for registro in registros:
        if not isinstance(registro, dict):
            raise ValueError("Cada registro debe ser un diccionario")

        planta = str(registro.get("planta", "")).strip()
        if not planta:
            raise ValueError("Cada registro debe indicar la planta")

        consumo = registro.get("consumo_kwh")
        emisiones = calcular_emisiones_carbono(consumo)

        consumos_por_planta[planta] = consumos_por_planta.get(planta, 0.0) + float(
            consumo
        )
        emisiones_por_planta[planta] = (
            emisiones_por_planta.get(planta, 0.0) + emisiones
        )

    if not consumos_por_planta:
        return {
            "total_emisiones": 0.0,
            "planta_mayor_consumo": None,
            "consumo_mayor_planta": 0.0,
            "emisiones_por_planta": {},
        }

    planta_mayor_consumo = max(consumos_por_planta, key=consumos_por_planta.get)

    return {
        "total_emisiones": sum(emisiones_por_planta.values()),
        "planta_mayor_consumo": planta_mayor_consumo,
        "consumo_mayor_planta": consumos_por_planta[planta_mayor_consumo],
        "emisiones_por_planta": emisiones_por_planta,
    }
