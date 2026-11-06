# EcoTech Solutions — Proyecto Python C3

Desarrollo de tres ejercicios prácticos para **EcoTech Solutions** que cubren
procesamiento de datos, programación orientada a objetos, persistencia,
pruebas automatizadas e integración web con Django.

## Objetivos académicos

- Aplicar sanitización y análisis estadístico de datos con Python.
- Modelar un dominio con encapsulamiento, herencia y polimorfismo.
- Persistir objetos en JSON sin serializar instancias directamente.
- Auditorar un algoritmo con `unittest` y validar entradas.
- Integrar la lógica de negocio con una vista y una plantilla de Django.
- Documentar y verificar cada solución de forma reproducible.

## Tecnologías

- Python 3.14+ (probado con Python 3.15)
- Django 6.1.3 (solo para el ejercicio 3)
- Biblioteca estándar para los ejercicios 1 y 2
- `unittest` como marco de pruebas

## Estructura del repositorio

```text
proyecto_python_C3/
├── README.md
├── .gitignore
├── ejercicio_1_sensores/
│   ├── sensores.py
│   ├── main.py
│   ├── tests/
│   └── README.md
├── ejercicio_2_productos/
│   ├── excepciones.py
│   ├── modelos.py
│   ├── inventario.py
│   ├── main.py
│   ├── catalogo_ecotech.json
│   ├── tests/
│   └── README.md
└── ejercicio_3_auditoria_web/
    ├── manage.py
    ├── requirements.txt
    ├── config/
    ├── auditoria/
    ├── templates/sustentabilidad/panel.html
    └── README.md
```

## Descripción de los ejercicios

| Ejercicio | Contenido | Puntaje |
|---|---|---:|
| [Ejercicio 1](ejercicio_1_sensores/README.md) | Sanitización y análisis estadístico de sensores | 20 |
| [Ejercicio 2](ejercicio_2_productos/README.md) | Productos, excepciones, POO y persistencia JSON | 40 |
| [Ejercicio 3](ejercicio_3_auditoria_web/README.md) | Auditoría con `unittest` e integración web con Django | 40 |

Los tres ejercicios son independientes y pueden ejecutarse por separado.

## Inicio rápido

Desde la raíz del proyecto:

1. Verificar que Python 3.14 o superior esté instalado.
2. Crear y activar un entorno virtual.
3. Instalar Django para el ejercicio 3.
4. Ejecutar las pruebas de cada ejercicio.
5. Ejecutar el ejercicio que se desea revisar.

## Instalación

Los ejercicios 1 y 2 solo requieren Python 3.14 o superior y no necesitan
dependencias externas. Para el ejercicio 3 se necesita Django, por lo que se
recomienda crear un entorno virtual en la raíz:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r ejercicio_3_auditoria_web/requirements.txt
```

## Ejecución

Ejecutar cada comando desde la raíz del proyecto:

```bash
(cd ejercicio_1_sensores && python main.py)
(cd ejercicio_2_productos && python main.py)
(cd ejercicio_3_auditoria_web && python manage.py runserver)
```

El panel de sustentabilidad queda disponible en
<http://127.0.0.1:8000/sustentabilidad/>.

## Pruebas

```bash
# Ejercicio 1
(cd ejercicio_1_sensores && python -m unittest discover -s tests)

# Ejercicio 2
(cd ejercicio_2_productos && python -m unittest discover -s tests)

# Ejercicio 3
(cd ejercicio_3_auditoria_web && python manage.py test)
```

También se pueden ejecutar las pruebas de los ejercicios 1 y 2 desde la raíz:

```bash
python -m unittest discover -s ejercicio_1_sensores/tests
python -m unittest discover -s ejercicio_2_productos/tests
```

El ejercicio 3 debe probarse desde su directorio porque Django necesita cargar
la configuración del proyecto.

## Documentación adicional

Cada directorio de ejercicio incluye un `README.md` con el detalle de sus
requerimientos, arquitectura, API y pruebas.
