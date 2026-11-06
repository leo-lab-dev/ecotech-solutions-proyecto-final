"""Demostración del flujo de sanitización y análisis de sensores."""

from sensores import generar_resumen_sensores, limpiar_registro_sensor

UMBRAL_TEMPERATURA = 30.0

REGISTROS_CRUDOS = [
    {
        "sensor_id": " SENSOR-001 ",
        "temperatura": "24.5C",
        "ubicacion": "Planta Norte",
    },
    {
        "sensor_id": "SENSOR-002",
        "temperatura": " 35.2 °C ",
        "ubicacion": "  Planta   Sur ",
    },
    {
        "sensor_id": "SENSOR-003",
        "temperatura": "31",
    },
    {
        "sensor_id": "SENSOR-004",
        "temperatura": "18.75 C",
        "ubicacion": "Planta Este",
    },
]


def main() -> None:
    """Procesa los registros de ejemplo e imprime el reporte consolidado."""
    sensores_limpios = []

    for registro in REGISTROS_CRUDOS:
        try:
            sensores_limpios.append(limpiar_registro_sensor(registro))
        except (TypeError, ValueError) as error:
            print(f"Registro descartado: {error}")

    alertas, promedio = generar_resumen_sensores(
        sensores_limpios,
        UMBRAL_TEMPERATURA,
    )

    print("=" * 48)
    print("REPORTE DE SENSORES - ECOTECH SOLUTIONS")
    print("=" * 48)
    print(f"Sensores procesados: {len(sensores_limpios)}")
    print(f"Promedio global de temperatura: {promedio:.2f} °C")
    print(f"Umbral utilizado: {UMBRAL_TEMPERATURA:.2f} °C")
    print(f"Sensores en alerta: {', '.join(alertas) if alertas else 'Ninguno'}")
    print("=" * 48)


if __name__ == "__main__":
    main()
