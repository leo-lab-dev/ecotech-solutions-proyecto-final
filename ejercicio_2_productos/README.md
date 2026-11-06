# Ejercicio 2 — Modelo de Productos, Excepciones y Persistencia

## Objetivo

Administrar el catálogo de dispositivos ecológicos de EcoTech Solutions
aplicando encapsulamiento, herencia, polimorfismo, excepciones personalizadas y
persistencia en JSON.

## Requerimientos implementados

- Excepción de dominio `StockInvalidoError`.
- Clase base `DispositivoEcologico` con identificador, nombre, precio y stock.
- Stock encapsulado en `__stock`, accesible mediante `@property` y validado en
  cada asignación por su setter.
- El stock anterior se conserva si una asignación es rechazada.
- Clase `PanelSolar` que hereda de `DispositivoEcologico` y añade potencia,
  eficiencia y tecnología.
- Polimorfismo real: ambas clases implementan `generar_ficha_tecnica()` con
  comportamientos distintos, sin comprobaciones externas de tipo.
- Serialización mediante `to_dict()`, extendida con `super()` en `PanelSolar`.
- `GestorInventario.guardar_catalogo_json()` escribe UTF-8 con indentación y
  crea directorios intermedios si hacen falta.
- Manejo controlado de errores de escritura (`OSError`) y de objetos no válidos
  (`TypeError`).

## Arquitectura

| Archivo | Responsabilidad |
|---|---|
| `excepciones.py` | Excepción `StockInvalidoError` |
| `modelos.py` | `DispositivoEcologico`, `PanelSolar` y serialización |
| `inventario.py` | Persistencia del catálogo en JSON |
| `main.py` | Demostración del dominio y de la exportación |
| `catalogo_ecotech.json` | Catálogo persistido |

## Instalación

No se requieren dependencias externas. Es suficiente con Python 3.14 o
superior.

## API principal

### `DispositivoEcologico(identificador, nombre, stock, precio=0.0)`

```python
dispositivo = DispositivoEcologico("ECO-001", "Cargador solar", 10)
dispositivo.stock = -5  # StockInvalidoError
dispositivo.stock       # 10 (se conserva el valor válido)
```

### `PanelSolar(...)`

```python
panel = PanelSolar(
    "ECO-003",
    "Panel solar residencial 450W",
    stock=8,
    potencia_watts=450,
    eficiencia=21.5,
    tecnologia="Monocristalino",
    precio=349.99,
)
```

### `GestorInventario.guardar_catalogo_json(lista, ruta)`

```python
gestor = GestorInventario()
gestor.guardar_catalogo_json(dispositivos, "catalogo_ecotech.json")
```

Cada elemento serializado mantiene una estructura coherente:

```json
{
  "tipo": "PanelSolar",
  "identificador": "ECO-003",
  "nombre": "Panel solar residencial 450W",
  "precio": 349.99,
  "stock": 8,
  "potencia_watts": 450.0,
  "eficiencia": 21.5,
  "tecnologia": "Monocristalino"
}
```

## Ejecución

```bash
cd ejercicio_2_productos
python main.py
```

El programa muestra las fichas técnicas, intenta asignar un stock negativo,
captura `StockInvalidoError`, verifica que el stock válido se conserva y exporta
el catálogo a `catalogo_ecotech.json`.

## Datos de prueba

Las pruebas usan `tempfile.TemporaryDirectory()` para no sobrescribir el
`catalogo_ecotech.json` versionado. El archivo del repositorio contiene el
catálogo generado por `main.py` y puede regenerarse ejecutando el programa.

## Ejecución desde la raíz

Si se está ubicado en la raíz del proyecto, también puede ejecutarse con:

```bash
python ejercicio_2_productos/main.py
```

## Pruebas

```bash
cd ejercicio_2_productos
python -m unittest discover -s tests
```

Se verifican instanciación, herencia, encapsulamiento, validaciones, ficha
técnica polimórfica, serialización, creación del archivo y lectura del JSON.
