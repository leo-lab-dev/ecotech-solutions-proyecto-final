"""Normalización de lecturas de sensores y generación de resúmenes.

El módulo separa dos responsabilidades:

* ``limpiar_registro_sensor``: normaliza un registro crudo.
* ``generar_resumen_sensores``: analiza una colección ya normalizada.
"""

from __future__ import annotations

from typing import Any

UBICACION_DESCONOCIDA = "Ubicación desconocida"

# Se ordenan de más específico a más general para quitar correctamente "°C".
_SUFIJOS_TEMPERATURA = ("°C", "C", "K", "F")


def _normalizar_identificador(valor: Any) -> str:
    """Devuelve el identificador sin espacios sobrantes.

    Raises:
        ValueError: si el identificador está ausente o vacío.
    """
    if valor is None:
        raise ValueError("El registro no contiene 'sensor_id'")

    identificador = str(valor).strip()
    if not identificador:
        raise ValueError("El 'sensor_id' no puede estar vacío")

    return identificador


def _normalizar_temperatura(valor: Any) -> float:
    """Convierte la temperatura cruda a ``float`` quitando el sufijo de unidad.

    Raises:
        ValueError: si la temperatura está ausente o no es convertible.
    """
    if valor is None:
        raise ValueError("El registro no contiene 'temperatura'")

    if isinstance(valor, bool):
        raise ValueError(f"Temperatura inválida: {valor!r}")

    if isinstance(valor, (int, float)):
        return float(valor)

    if not isinstance(valor, str):
        raise ValueError(f"Temperatura inválida: {valor!r}")

    texto = valor.strip().upper()
    for sufijo in _SUFIJOS_TEMPERATURA:
        if texto.endswith(sufijo):
            texto = texto[: -len(sufijo)].strip()
            break

    if not texto:
        raise ValueError(f"Temperatura inválida: {valor!r}")

    try:
        return float(texto)
    except ValueError as error:
        raise ValueError(f"Temperatura inválida: {valor!r}") from error


def _normalizar_ubicacion(valor: Any) -> str:
    """Normaliza la ubicación y aplica un valor predeterminado si falta."""
    if valor is None:
        return UBICACION_DESCONOCIDA

    ubicacion = " ".join(str(valor).split())
    return ubicacion or UBICACION_DESCONOCIDA


def limpiar_registro_sensor(registro_raw: dict[str, Any]) -> dict[str, Any]:
    """Normaliza un registro crudo de sensor sin modificar el original.

    Args:
        registro_raw: Diccionario con ``sensor_id``, ``temperatura`` y,
            opcionalmente, ``ubicacion``.

    Returns:
        Un nuevo diccionario con el identificador limpio, la temperatura como
        ``float`` y la ubicación normalizada.

    Raises:
        TypeError: si ``registro_raw`` no es un diccionario.
        ValueError: si el identificador o la temperatura no son válidos.
    """
    if not isinstance(registro_raw, dict):
        raise TypeError("El registro debe ser un diccionario")

    return {
        "sensor_id": _normalizar_identificador(registro_raw.get("sensor_id")),
        "temperatura": _normalizar_temperatura(registro_raw.get("temperatura")),
        "ubicacion": _normalizar_ubicacion(registro_raw.get("ubicacion")),
    }


def generar_resumen_sensores(
    lista_sensores_limpios: list[dict[str, Any]],
    umbral_temperatura: float,
) -> tuple[list[str], float]:
    """Genera la lista de sensores en alerta y el promedio térmico global.

    Un sensor se considera en alerta solo si su temperatura es estrictamente
    mayor que el umbral.

    Args:
        lista_sensores_limpios: Sensores previamente normalizados.
        umbral_temperatura: Temperatura límite para generar una alerta.

    Returns:
        Una tupla ``(sensores_en_alerta, promedio_temperatura)``. Para una
        colección vacía el promedio es ``0.0``.
    """
    sensores = list(lista_sensores_limpios)
    umbral = float(umbral_temperatura)

    sensores_en_alerta = [
        sensor["sensor_id"]
        for sensor in sensores
        if float(sensor["temperatura"]) > umbral
    ]

    if not sensores:
        return sensores_en_alerta, 0.0

    promedio = sum(float(sensor["temperatura"]) for sensor in sensores) / len(sensores)
    return sensores_en_alerta, promedio
