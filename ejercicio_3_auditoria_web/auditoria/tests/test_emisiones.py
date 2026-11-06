"""Pruebas unitarias del cálculo de emisiones de carbono."""

import unittest

from auditoria.emisiones import calcular_emisiones_carbono


class TestCalculoEmisiones(unittest.TestCase):
    """Verifica el algoritmo de cálculo de emisiones."""

    def test_consumo_nominal_usa_factor_predeterminado(self):
        resultado = calcular_emisiones_carbono(100)

        self.assertAlmostEqual(resultado, 40.0)

    def test_factor_de_emision_personalizado(self):
        resultado = calcular_emisiones_carbono(100, 0.5)

        self.assertAlmostEqual(resultado, 50.0)

    def test_consumo_cero_devuelve_cero(self):
        resultado = calcular_emisiones_carbono(0)

        self.assertEqual(resultado, 0.0)

    def test_consumo_negativo_lanza_value_error(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-10)

    def test_precision_del_resultado(self):
        resultado = calcular_emisiones_carbono(123.45, 0.37)

        self.assertAlmostEqual(resultado, 45.6765)

    def test_retorna_un_valor_numerico(self):
        resultado = calcular_emisiones_carbono(10)

        self.assertIsInstance(resultado, float)

    def test_consumo_no_numerico_lanza_value_error(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono("100")

    def test_factor_negativo_lanza_value_error(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(100, -0.4)


if __name__ == "__main__":
    unittest.main()
