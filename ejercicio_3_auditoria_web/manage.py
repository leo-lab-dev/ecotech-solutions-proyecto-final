#!/usr/bin/env python
"""Utilidad de línea de comandos para tareas administrativas de Django."""

import os
import sys


def main() -> None:
    """Ejecuta los comandos administrativos de Django."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as error:
        raise ImportError(
            "Django no está instalado. Activá el entorno virtual e instalá "
            "las dependencias de requirements.txt."
        ) from error

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
