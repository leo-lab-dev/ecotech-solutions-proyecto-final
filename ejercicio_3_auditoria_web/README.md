# Ejercicio 3 — Auditoría con Tests Unitarios e Integración Web

## Objetivo

Auditar el cálculo de emisiones de carbono industriales, procesar métricas por
planta e integrarlas en un panel web desarrollado con Django.

## Requerimientos implementados

- `calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4)` con factor
  predeterminado `0.4`, validación de consumos y factores negativos mediante
  `ValueError` y retorno numérico `float`. Las emisiones se expresan en
  kilogramos de CO₂.
- `TestCalculoEmisiones(unittest.TestCase)` con los casos nominal, factor
  personalizado, consumo cero, consumo negativo y precisión.
- `obtener_metricas_consumo(registros)` con cálculo de emisiones, total global,
  agrupación por planta, identificación de la planta de mayor **consumo** y
  manejo de historiales vacíos y empates.
- `vista_panel_sustentabilidad(request)` que obtiene los registros, invoca el
  procesamiento y renderiza `sustentabilidad/panel.html`.
- Rutas registradas en `config/urls.py` y `auditoria/urls.py`.
- Plantilla con HTML semántico, tarjetas, tabla y mensaje para historial vacío,
  sin cálculos de negocio.
- Estilos en `static/sustentabilidad/panel.css`, cargados con `{% static %}`;
  el template no contiene bloques `<style>`.
- Protección CSRF activa mediante `CsrfViewMiddleware`.
- Pruebas de métricas y de integración de la vista.

## Arquitectura

| Archivo | Responsabilidad |
|---|---|
| `auditoria/emisiones.py` | Cálculo puro de emisiones (independiente de Django) |
| `auditoria/metricas.py` | Procesamiento y agregación de métricas |
| `auditoria/views.py` | Coordinación de la solicitud y el contexto |
| `auditoria/urls.py` | Ruta `/sustentabilidad/` |
| `config/` | Configuración del proyecto Django |
| `templates/sustentabilidad/panel.html` | Estructura semántica de las métricas |
| `static/sustentabilidad/panel.css` | Estilos del panel, separados del HTML |
| `auditoria/tests/` | Pruebas unitarias y de integración |

## API principal

### `calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4)`

```python
calcular_emisiones_carbono(100)        # 40.0
calcular_emisiones_carbono(100, 0.5)   # 50.0
calcular_emisiones_carbono(-10)        # ValueError
```

### `obtener_metricas_consumo(registros)`

```python
{
    "total_emisiones": 2000.0,
    "planta_mayor_consumo": "Planta Sur",
    "consumo_mayor_planta": 2500.0,
    "emisiones_por_planta": {
        "Planta Norte": 800.0,
        "Planta Sur": 1000.0,
        "Planta Este": 400.0,
    },
}
```

Para un historial vacío devuelve `total_emisiones` y `consumo_mayor_planta` en
`0.0`, `planta_mayor_consumo` en `None` y `emisiones_por_planta` vacío. En caso
de empate se conserva la primera planta encontrada.

## Datos utilizados por el panel

El panel utiliza un historial de consumos simulado definido en
`auditoria/metricas.py`; no depende de una base de datos ni de servicios
externos. Para modificar los datos que aparecen en el panel se debe actualizar
`REGISTROS_CONSUMO_SIMULADOS`. La función `obtener_registros_consumo()` entrega
copias de los registros para evitar modificaciones accidentales del historial
original.

## Instalación

```bash
cd ejercicio_3_auditoria_web
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

Desde el directorio `ejercicio_3_auditoria_web`:

```bash
python manage.py runserver
```

Panel disponible en <http://127.0.0.1:8000/sustentabilidad/>.

Con `DEBUG=True`, Django sirve los archivos estáticos automáticamente. Para un
despliegue con `DEBUG=False`, ejecutar `python manage.py collectstatic` y
publicar el directorio de estáticos con el servidor web correspondiente.

## Pruebas

```bash
cd ejercicio_3_auditoria_web
python manage.py test
```

- `test_emisiones.py`: clase `TestCalculoEmisiones` basada en `unittest`.
- `test_metricas.py`: agregación, totales, mayor consumo, vacío y empates.
- `test_views.py`: respuesta 200, plantilla, contexto y caso sin registros.
