"""Pruebas de los modelos del catálogo EcoTech."""

import unittest

from excepciones import StockInvalidoError
from modelos import DispositivoEcologico, PanelSolar


class TestDispositivoEcologico(unittest.TestCase):
    """Verifica la clase base y el encapsulamiento del stock."""

    def test_instanciacion_de_clase_base(self):
        dispositivo = DispositivoEcologico("ECO-001", "Cargador solar", 10)

        self.assertEqual(dispositivo.identificador, "ECO-001")
        self.assertEqual(dispositivo.nombre, "Cargador solar")
        self.assertEqual(dispositivo.stock, 10)

    def test_asignacion_de_stock_valido(self):
        dispositivo = DispositivoEcologico("ECO-001", "Cargador solar", 10)

        dispositivo.stock = 15

        self.assertEqual(dispositivo.stock, 15)

    def test_rechaza_stock_negativo_en_creacion(self):
        with self.assertRaises(StockInvalidoError):
            DispositivoEcologico("ECO-001", "Cargador solar", -1)

    def test_rechaza_stock_negativo_en_modificacion(self):
        dispositivo = DispositivoEcologico("ECO-001", "Cargador solar", 10)

        with self.assertRaises(StockInvalidoError):
            dispositivo.stock = -5

    def test_conserva_stock_anterior_ante_asignacion_invalida(self):
        dispositivo = DispositivoEcologico("ECO-001", "Cargador solar", 10)

        with self.assertRaises(StockInvalidoError):
            dispositivo.stock = -5

        self.assertEqual(dispositivo.stock, 10)

    def test_rechaza_stock_no_entero(self):
        dispositivo = DispositivoEcologico("ECO-001", "Cargador solar", 10)

        with self.assertRaises(StockInvalidoError):
            dispositivo.stock = 2.5

        self.assertEqual(dispositivo.stock, 10)

    def test_ficha_tecnica_de_clase_base(self):
        dispositivo = DispositivoEcologico("ECO-001", "Cargador solar", 10, 39.9)

        ficha = dispositivo.generar_ficha_tecnica()

        self.assertIn("ECO-001", ficha)
        self.assertIn("Cargador solar", ficha)
        self.assertIn("10", ficha)

    def test_to_dict_incluye_atributos_comunes(self):
        dispositivo = DispositivoEcologico("ECO-001", "Cargador solar", 10, 39.9)

        datos = dispositivo.to_dict()

        self.assertEqual(
            datos,
            {
                "tipo": "DispositivoEcologico",
                "identificador": "ECO-001",
                "nombre": "Cargador solar",
                "precio": 39.9,
                "stock": 10,
            },
        )


class TestPanelSolar(unittest.TestCase):
    """Verifica la herencia, los atributos específicos y el polimorfismo."""

    def setUp(self):
        self.panel = PanelSolar(
            "ECO-003",
            "Panel solar residencial",
            stock=8,
            potencia_watts=450,
            eficiencia=21.5,
            tecnologia="Monocristalino",
            precio=349.99,
        )

    def test_es_instancia_de_dispositivo_ecologico(self):
        self.assertIsInstance(self.panel, DispositivoEcologico)

    def test_hereda_atributos_comunes(self):
        self.assertEqual(self.panel.identificador, "ECO-003")
        self.assertEqual(self.panel.nombre, "Panel solar residencial")
        self.assertEqual(self.panel.stock, 8)

    def test_expone_atributos_especificos(self):
        self.assertEqual(self.panel.potencia_watts, 450)
        self.assertEqual(self.panel.eficiencia, 21.5)
        self.assertEqual(self.panel.tecnologia, "Monocristalino")

    def test_hereda_validacion_de_stock(self):
        with self.assertRaises(StockInvalidoError):
            self.panel.stock = -1

        self.assertEqual(self.panel.stock, 8)

    def test_rechaza_eficiencia_invalida(self):
        with self.assertRaises(ValueError):
            PanelSolar("ECO-004", "Panel inválido", 1, 300, 150)

    def test_sobrescribe_ficha_tecnica(self):
        ficha_base = DispositivoEcologico(
            "ECO-001",
            "Cargador solar",
            10,
        ).generar_ficha_tecnica()
        ficha_panel = self.panel.generar_ficha_tecnica()

        self.assertNotEqual(ficha_base, ficha_panel)
        self.assertIn("450.00 W", ficha_panel)
        self.assertIn("21.50 %", ficha_panel)
        self.assertIn("Monocristalino", ficha_panel)

    def test_polimorfismo_mediante_misma_interfaz(self):
        dispositivos = [
            DispositivoEcologico("ECO-001", "Cargador solar", 10),
            self.panel,
        ]

        fichas = [dispositivo.generar_ficha_tecnica() for dispositivo in dispositivos]

        self.assertEqual(len(fichas), 2)
        self.assertIn("Potencia nominal", fichas[1])
        self.assertNotIn("Potencia nominal", fichas[0])

    def test_to_dict_incluye_atributos_especificos(self):
        datos = self.panel.to_dict()

        self.assertEqual(datos["tipo"], "PanelSolar")
        self.assertEqual(datos["potencia_watts"], 450)
        self.assertEqual(datos["eficiencia"], 21.5)
        self.assertEqual(datos["tecnologia"], "Monocristalino")
        self.assertEqual(datos["stock"], 8)


if __name__ == "__main__":
    unittest.main()
