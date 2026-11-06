"""Demostración del catálogo, sus validaciones y la persistencia en JSON."""

from pathlib import Path

from excepciones import StockInvalidoError
from inventario import GestorInventario
from modelos import DispositivoEcologico, PanelSolar

RUTA_CATALOGO = Path(__file__).resolve().parent / "catalogo_ecotech.json"


def main() -> None:
    """Ejecuta el flujo demostrativo del ejercicio 2."""
    dispositivos = [
        DispositivoEcologico("ECO-001", "Cargador solar portátil", 25, 39.9),
        DispositivoEcologico("ECO-002", "Batería de respaldo", 12, 129.0),
        PanelSolar(
            "ECO-003",
            "Panel solar residencial 450W",
            stock=8,
            potencia_watts=450,
            eficiencia=21.5,
            tecnologia="Monocristalino",
            precio=349.99,
        ),
    ]

    print("=" * 56)
    print("CATÁLOGO ECOTECH SOLUTIONS")
    print("=" * 56)

    for dispositivo in dispositivos:
        print(dispositivo.generar_ficha_tecnica())
        print("-" * 56)

    panel = dispositivos[-1]
    stock_valido = panel.stock

    try:
        panel.stock = -3
    except StockInvalidoError as error:
        print(f"Stock rechazado: {error}")
        print(f"El stock válido se conserva: {panel.stock} unidades")

    assert panel.stock == stock_valido

    gestor = GestorInventario()
    ruta = gestor.guardar_catalogo_json(dispositivos, RUTA_CATALOGO)

    print(f"Catálogo exportado correctamente en: {ruta}")


if __name__ == "__main__":
    main()
