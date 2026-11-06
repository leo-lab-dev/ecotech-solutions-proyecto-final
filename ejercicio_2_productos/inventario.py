"""Persistencia del catálogo de dispositivos en formato JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

try:  # Importación como paquete desde la raíz del repositorio.
    from .modelos import DispositivoEcologico
except ImportError:  # Ejecución desde el directorio del ejercicio.
    from modelos import DispositivoEcologico


class GestorInventario:
    """Gestiona la persistencia del catálogo de dispositivos."""

    def guardar_catalogo_json(
        self,
        lista_dispositivos: Iterable[DispositivoEcologico],
        ruta_archivo: str | Path,
    ) -> Path:
        """Serializa los dispositivos y los guarda en un archivo JSON.

        Args:
            lista_dispositivos: Dispositivos que se desean persistir.
            ruta_archivo: Ruta del archivo de destino.

        Returns:
            La ruta del archivo escrito.

        Raises:
            TypeError: si algún elemento no es un dispositivo del catálogo.
            OSError: si no es posible escribir el archivo.
        """
        datos = []
        for dispositivo in lista_dispositivos:
            if not isinstance(dispositivo, DispositivoEcologico):
                raise TypeError(
                    "Solo se pueden guardar instancias de DispositivoEcologico"
                )
            datos.append(dispositivo.to_dict())

        ruta = Path(ruta_archivo)
        ruta.parent.mkdir(parents=True, exist_ok=True)

        try:
            with ruta.open("w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=2)
        except OSError as error:
            raise OSError(f"No se pudo guardar el catálogo en {ruta}: {error}") from error

        return ruta
