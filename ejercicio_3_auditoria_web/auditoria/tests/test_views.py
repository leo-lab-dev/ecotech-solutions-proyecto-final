"""Pruebas de integración de la vista del panel de sustentabilidad."""

from unittest.mock import patch

from django.contrib.staticfiles import finders
from django.test import TestCase
from django.urls import reverse

from auditoria.metricas import obtener_metricas_consumo


class TestVistaPanelSustentabilidad(TestCase):
    """Verifica la respuesta HTTP, la plantilla y el contexto de la vista."""

    def test_respuesta_http_exitosa(self):
        respuesta = self.client.get(reverse("auditoria:panel_sustentabilidad"))

        self.assertEqual(respuesta.status_code, 200)

    def test_renderiza_la_plantilla_correcta(self):
        respuesta = self.client.get(reverse("auditoria:panel_sustentabilidad"))

        self.assertTemplateUsed(respuesta, "sustentabilidad/panel.html")

    def test_contexto_contiene_las_metricas(self):
        respuesta = self.client.get(reverse("auditoria:panel_sustentabilidad"))

        self.assertIn("metricas", respuesta.context)
        metricas = respuesta.context["metricas"]
        self.assertIn("total_emisiones", metricas)
        self.assertIn("planta_mayor_consumo", metricas)
        self.assertIn("consumo_mayor_planta", metricas)
        self.assertIn("emisiones_por_planta", metricas)

    def test_contexto_coincide_con_el_procesamiento(self):
        registros = [
            {"planta": "Planta Norte", "consumo_kwh": 1500},
            {"planta": "Planta Sur", "consumo_kwh": 2500},
        ]

        with patch(
            "auditoria.views.obtener_registros_consumo",
            return_value=registros,
        ):
            respuesta = self.client.get(reverse("auditoria:panel_sustentabilidad"))

        esperado = obtener_metricas_consumo(registros)
        self.assertEqual(respuesta.context["metricas"], esperado)

    def test_maneja_historial_vacio(self):
        with patch("auditoria.views.obtener_registros_consumo", return_value=[]):
            respuesta = self.client.get(reverse("auditoria:panel_sustentabilidad"))

        self.assertEqual(respuesta.status_code, 200)
        metricas = respuesta.context["metricas"]
        self.assertEqual(metricas["total_emisiones"], 0.0)
        self.assertIsNone(metricas["planta_mayor_consumo"])
        self.assertContains(respuesta, "No hay registros de consumo disponibles")

    def test_muestra_las_metricas_en_el_html(self):
        respuesta = self.client.get(reverse("auditoria:panel_sustentabilidad"))

        self.assertContains(respuesta, "Panel de Sustentabilidad")
        self.assertContains(respuesta, "Total global de emisiones")
        self.assertContains(respuesta, "Emisiones por planta")

    def test_referencia_hoja_de_estilos_externa(self):
        respuesta = self.client.get(reverse("auditoria:panel_sustentabilidad"))

        self.assertContains(respuesta, "sustentabilidad/panel.css")
        self.assertNotContains(respuesta, "<style")

    def test_hoja_de_estilos_es_localizable(self):
        self.assertIsNotNone(finders.find("sustentabilidad/panel.css"))


if __name__ == "__main__":
    import unittest

    unittest.main()
