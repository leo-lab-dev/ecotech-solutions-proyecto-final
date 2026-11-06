"""Pruebas de normalización y resumen de sensores."""

import unittest

from sensores import (
    UBICACION_DESCONOCIDA,
    generar_resumen_sensores,
    limpiar_registro_sensor,
)


class TestLimpiarRegistroSensor(unittest.TestCase):
    """Verifica la sanitización de registros crudos."""

    def test_normaliza_identificador(self):
        registro = {
            "sensor_id": "  SENSOR-001  ",
            "temperatura": "24.5C",
            "ubicacion": "Planta Norte",
        }

        resultado = limpiar_registro_sensor(registro)

        self.assertEqual(resultado["sensor_id"], "SENSOR-001")

    def test_convierte_temperatura_con_sufijo_c(self):
        registro = {
            "sensor_id": "SENSOR-001",
            "temperatura": "24.5C",
            "ubicacion": "Planta Norte",
        }

        resultado = limpiar_registro_sensor(registro)

        self.assertIsInstance(resultado["temperatura"], float)
        self.assertAlmostEqual(resultado["temperatura"], 24.5)

    def test_convierte_temperatura_con_espacios_y_simbolo(self):
        registro = {
            "sensor_id": "SENSOR-002",
            "temperatura": "  35.2 °C ",
            "ubicacion": "Planta Sur",
        }

        resultado = limpiar_registro_sensor(registro)

        self.assertAlmostEqual(resultado["temperatura"], 35.2)

    def test_ubicacion_ausente_usa_valor_predeterminado(self):
        registro = {"sensor_id": "SENSOR-003", "temperatura": "20"}

        resultado = limpiar_registro_sensor(registro)

        self.assertEqual(resultado["ubicacion"], UBICACION_DESCONOCIDA)

    def test_ubicacion_vacia_usa_valor_predeterminado(self):
        registro = {
            "sensor_id": "SENSOR-003",
            "temperatura": "20",
            "ubicacion": "   ",
        }

        resultado = limpiar_registro_sensor(registro)

        self.assertEqual(resultado["ubicacion"], UBICACION_DESCONOCIDA)

    def test_normaliza_espacios_de_la_ubicacion(self):
        registro = {
            "sensor_id": "SENSOR-004",
            "temperatura": "20",
            "ubicacion": "  Planta   Norte ",
        }

        resultado = limpiar_registro_sensor(registro)

        self.assertEqual(resultado["ubicacion"], "Planta Norte")

    def test_no_modifica_diccionario_original(self):
        registro = {
            "sensor_id": " SENSOR-001 ",
            "temperatura": "24.5C",
            "ubicacion": "Planta Norte",
        }
        copia = registro.copy()

        limpiar_registro_sensor(registro)

        self.assertEqual(registro, copia)
        self.assertEqual(registro["temperatura"], "24.5C")

    def test_temperatura_invalida_lanza_value_error(self):
        registro = {"sensor_id": "SENSOR-005", "temperatura": "caliente"}

        with self.assertRaises(ValueError):
            limpiar_registro_sensor(registro)

    def test_temperatura_ausente_lanza_value_error(self):
        registro = {"sensor_id": "SENSOR-006"}

        with self.assertRaises(ValueError):
            limpiar_registro_sensor(registro)

    def test_registro_no_diccionario_lanza_type_error(self):
        with self.assertRaises(TypeError):
            limpiar_registro_sensor(["sensor_id", "temperatura"])


class TestGenerarResumenSensores(unittest.TestCase):
    """Verifica el cálculo de alertas y del promedio global."""

    def setUp(self):
        self.sensores = [
            {
                "sensor_id": "SENSOR-001",
                "temperatura": 24.5,
                "ubicacion": "Planta Norte",
            },
            {
                "sensor_id": "SENSOR-002",
                "temperatura": 35.2,
                "ubicacion": "Planta Sur",
            },
        ]

    def test_identifica_sensores_en_alerta(self):
        alertas, _ = generar_resumen_sensores(self.sensores, 30)

        self.assertEqual(alertas, ["SENSOR-002"])

    def test_temperatura_igual_al_umbral_no_genera_alerta(self):
        sensores = [
            {
                "sensor_id": "SENSOR-003",
                "temperatura": 30.0,
                "ubicacion": "Planta Este",
            }
        ]

        alertas, _ = generar_resumen_sensores(sensores, 30)

        self.assertEqual(alertas, [])

    def test_calcula_promedio_global(self):
        _, promedio = generar_resumen_sensores(self.sensores, 30)

        self.assertAlmostEqual(promedio, 29.85)

    def test_coleccion_vacia_devuelve_promedio_cero(self):
        alertas, promedio = generar_resumen_sensores([], 30)

        self.assertEqual(alertas, [])
        self.assertEqual(promedio, 0.0)

    def test_retorna_una_tupla(self):
        resultado = generar_resumen_sensores(self.sensores, 30)

        self.assertIsInstance(resultado, tuple)
        self.assertEqual(len(resultado), 2)


if __name__ == "__main__":
    unittest.main()
