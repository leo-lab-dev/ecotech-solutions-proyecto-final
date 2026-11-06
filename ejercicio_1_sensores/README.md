# Ejercicio 1 — Sanitización y Análisis Estadístico de Sensores

## Objetivo

Normalizar lecturas térmicas provenientes de microcontroladores y generar un reporte estadístico consolidado, separando la limpieza de registros del procesamiento estadístico.

## Requerimientos implementados

- Eliminación de espacios sobrantes en identificadores y ubicaciones.
- Conversión de temperaturas a `float`, quitando sufijos como `C` o `°C`.
- Valor predeterminado `"Ubicación desconocida"` cuando la ubicación falta o
  está vacía.
- Registro original intacto: la función devuelve un diccionario nuevo.
- Error controlado (`ValueError`) ante temperaturas ausentes o inválidas.
- `TypeError` cuando el registro no es un diccionario.
- Identificación de sensores cuya temperatura **supera estrictamente** el umbral.
- Promedio global de temperaturas y `0.0` para colecciones vacías.

## Arquitectura

| Archivo | Responsabilidad |
|---|---|
| `sensores.py` | Normalización y análisis estadístico |
| `main.py` | Demostración del flujo completo |
| `tests/test_sensores.py` | Pruebas automatizadas con `unittest` |

## Instalación

No se requieren dependencias externas. Es suficiente con Python 3.14 o
superior.

## API principal

### `limpiar_registro_sensor(registro_raw)`

```python
{
    "sensor_id": " SENSOR-001 ",
    "temperatura": "24.5C",
    "ubicacion": "Planta Norte",
}
```

devuelve:

```python
{
    "sensor_id": "SENSOR-001",
    "temperatura": 24.5,
    "ubicacion": "Planta Norte",
}
```

### `generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura)`

```python
sensores = [
    {"sensor_id": "SENSOR-001", "temperatura": 24.5, "ubicacion": "Planta Norte"},
    {"sensor_id": "SENSOR-002", "temperatura": 35.2, "ubicacion": "Planta Sur"},
]

generar_resumen_sensores(sensores, 30)
# (["SENSOR-002"], 29.85)
```

## Ejecución

```bash
cd ejercicio_1_sensores
python main.py
```

Salida esperada (resumida):

```text
REPORTE DE SENSORES - ECOTECH SOLUTIONS
Sensores procesados: 4
Promedio global de temperatura: 27.36 °C
Umbral utilizado: 30.00 °C
Sensores en alerta: SENSOR-002, SENSOR-003
```

## Datos de prueba

Los registros de ejemplo de `main.py` incluyen temperaturas con sufijos, espacios, una ubicación ausente y valores numéricos válidos. Las pruebas cubren además temperaturas inválidas, ubicaciones vacías y colecciones vacías.

## Ejecución desde la raíz

Si se está ubicado en la raíz del proyecto, también puede ejecutarse con:

```bash
python ejercicio_1_sensores/main.py
```

## Pruebas

```bash
cd ejercicio_1_sensores
python -m unittest discover -s tests
```

Las pruebas no dependen de archivos externos ni de servicios.
