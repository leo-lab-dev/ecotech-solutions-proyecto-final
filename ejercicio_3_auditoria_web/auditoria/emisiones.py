"""Cálculo de emisiones de carbono a partir del consumo eléctrico."""

from __future__ import annotations

FACTOR_EMISION_PREDETERMINADO = 0.4


def calcular_emisiones_carbono(
    consumo_kwh: float,
    factor_emision: float = FACTOR_EMISION_PREDETERMINADO,
) -> float:
    """Calcula las emisiones de carbono de un consumo eléctrico.

    Args:
        consumo_kwh: Consumo eléctrico en kilovatios hora.
        factor_emision: Factor de emisión en kg de CO2 por kWh. Su valor
            predeterminado es ``0.4``.

    Returns:
        Las emisiones expresadas como ``consumo_kwh * factor_emision``.

    Raises:
        ValueError: si el consumo o el factor no son numéricos o son negativos.
    """
    if isinstance(consumo_kwh, bool) or not isinstance(consumo_kwh, (int, float)):
        raise ValueError("El consumo debe ser un valor numérico")

    if consumo_kwh < 0:
        raise ValueError("El consumo no puede ser negativo")

    if isinstance(factor_emision, bool) or not isinstance(
        factor_emision, (int, float)
    ):
        raise ValueError("El factor de emisión debe ser un valor numérico")

    if factor_emision < 0:
        raise ValueError("El factor de emisión no puede ser negativo")

    return float(consumo_kwh) * float(factor_emision)
