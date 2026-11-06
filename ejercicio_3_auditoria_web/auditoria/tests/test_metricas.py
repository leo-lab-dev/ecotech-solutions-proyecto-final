"""Pruebas del procesamiento de métricas de consumo."""

import unittest

from auditoria.metricas import obtener_metricas_consumo, obtener_registros_consumo


class TestObtenerMetricasConsumo(unittest.TestCase):
    """Verifica la agregación de consumos y emisiones por planta."""

    def setUp(self):
        self.registros = [
            {"planta": "Planta Norte", "consumo_kwh": 1500},
            {"planta": "Planta Sur", "consumo_kwh": 2500},
            {"planta": "Planta Este", "consumo_kwh": 1000},
        ]

    def test_calcula_emisiones_por_planta(self):
        metricas = obtener_metricas_consumo(self.registros)

        self.assertAlmostEqual(metricas["emisiones_por_planta"]["Planta Norte"], 600.0)
        self.assertAlmostEqual(metricas["emisiones_por_planta"]["Planta Sur"], 1000.0)
        self.assertAlmostEqual(metricas["emisiones_por_planta"]["Planta Este"], 400.0)

    def test_calcula_total_global(self):
        metricas = obtener_metricas_consumo(self.registros)

        self.assertAlmostEqual(metricas["total_emisiones"], 2000.0)

    def test_identifica_planta_de_mayor_consumo(self):
        metricas = obtener_metricas_consumo(self.registros)

        self.assertEqual(metricas["planta_mayor_consumo"], "Planta Sur")
        self.assertAlmostEqual(metricas["consumo_mayor_planta"], 2500.0)

    def test_agrupa_varios_registros_de_la_misma_planta(self):
        registros = [
            {"planta": "Planta Norte", "consumo_kwh": 1000},
            {"planta": "Planta Sur", "consumo_kwh": 1200},
            {"planta": "Planta Norte", "consumo_kwh": 1500},
        ]

        metricas = obtener_metricas_consumo(registros)

        self.assertAlmostEqual(metricas["consumo_mayor_planta"], 2500.0)
        self.assertEqual(metricas["planta_mayor_consumo"], "Planta Norte")
        self.assertAlmostEqual(metricas["emisiones_por_planta"]["Planta Norte"], 1000.0)
        self.assertAlmostEqual(metricas["total_emisiones"], 1480.0)

    def test_historial_vacio_devuelve_valores_neutrales(self):
        metricas = obtener_metricas_consumo([])

        self.assertEqual(metricas["total_emisiones"], 0.0)
        self.assertIsNone(metricas["planta_mayor_consumo"])
        self.assertEqual(metricas["consumo_mayor_planta"], 0.0)
        self.assertEqual(metricas["emisiones_por_planta"], {})

    def test_empate_conserva_la_primera_planta(self):
        registros = [
            {"planta": "Planta Norte", "consumo_kwh": 1000},
            {"planta": "Planta Sur", "consumo_kwh": 1000},
        ]

        metricas = obtener_metricas_consumo(registros)

        self.assertEqual(metricas["planta_mayor_consumo"], "Planta Norte")

    def test_registro_sin_planta_lanza_value_error(self):
        with self.assertRaises(ValueError):
            obtener_metricas_consumo([{"consumo_kwh": 1000}])

    def test_consumo_negativo_lanza_value_error(self):
        with self.assertRaises(ValueError):
            obtener_metricas_consumo([{"planta": "Planta Norte", "consumo_kwh": -1}])

    def test_registros_simulados_son_independientes(self):
        primero = obtener_registros_consumo()
        primero[0]["consumo_kwh"] = 999999

        segundo = obtener_registros_consumo()

        self.assertNotEqual(segundo[0]["consumo_kwh"], 999999)


if __name__ == "__main__":
    unittest.main()
