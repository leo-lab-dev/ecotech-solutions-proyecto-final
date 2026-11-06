"""Pruebas de la persistencia JSON del catálogo."""

import json
import tempfile
import unittest
from pathlib import Path

from inventario import GestorInventario
from modelos import DispositivoEcologico, PanelSolar


class TestGestorInventario(unittest.TestCase):
    """Verifica la exportación del catálogo a JSON."""

    def setUp(self):
        self.gestor = GestorInventario()
        self.dispositivos = [
            DispositivoEcologico("ECO-001", "Cargador solar portátil", 25, 39.9),
            DispositivoEcologico("ECO-002", "Batería de respaldo", 12, 129.0),
            PanelSolar(
                "ECO-003",
                "Panel solar residencial",
                stock=8,
                potencia_watts=450,
                eficiencia=21.5,
                tecnologia="Monocristalino",
                precio=349.99,
            ),
        ]
        self.temporal = tempfile.TemporaryDirectory()
        self.ruta = Path(self.temporal.name) / "catalogo_ecotech.json"

    def tearDown(self):
        self.temporal.cleanup()

    def test_crea_el_archivo_de_salida(self):
        self.gestor.guardar_catalogo_json(self.dispositivos, self.ruta)

        self.assertTrue(self.ruta.exists())

    def test_serializa_todos_los_dispositivos(self):
        self.gestor.guardar_catalogo_json(self.dispositivos, self.ruta)

        with self.ruta.open(encoding="utf-8") as archivo:
            datos = json.load(archivo)

        self.assertEqual(len(datos), 3)
        self.assertEqual(datos[0]["identificador"], "ECO-001")
        self.assertEqual(datos[2]["identificador"], "ECO-003")

    def test_incluye_atributos_especificos_del_panel(self):
        self.gestor.guardar_catalogo_json(self.dispositivos, self.ruta)

        with self.ruta.open(encoding="utf-8") as archivo:
            datos = json.load(archivo)

        panel = datos[2]
        self.assertEqual(panel["tipo"], "PanelSolar")
        self.assertEqual(panel["potencia_watts"], 450)
        self.assertEqual(panel["eficiencia"], 21.5)
        self.assertEqual(panel["tecnologia"], "Monocristalino")

    def test_incluye_atributos_comunes(self):
        self.gestor.guardar_catalogo_json(self.dispositivos, self.ruta)

        with self.ruta.open(encoding="utf-8") as archivo:
            datos = json.load(archivo)

        for clave in ("tipo", "identificador", "nombre", "precio", "stock"):
            self.assertIn(clave, datos[0])

    def test_escribe_utf8_sin_escapar_caracteres(self):
        dispositivos = [
            DispositivoEcologico("ECO-004", "Panel eólico pequeño", 3, 199.0),
        ]
        self.gestor.guardar_catalogo_json(dispositivos, self.ruta)

        contenido = self.ruta.read_text(encoding="utf-8")

        self.assertIn("Panel eólico pequeño", contenido)

    def test_crea_directorios_intermedios(self):
        ruta = Path(self.temporal.name) / "datos" / "catalogo.json"

        self.gestor.guardar_catalogo_json(self.dispositivos, ruta)

        self.assertTrue(ruta.exists())

    def test_rechaza_objetos_que_no_son_dispositivos(self):
        with self.assertRaises(TypeError):
            self.gestor.guardar_catalogo_json([{"identificador": "ECO-005"}], self.ruta)

        self.assertFalse(self.ruta.exists())


if __name__ == "__main__":
    unittest.main()
