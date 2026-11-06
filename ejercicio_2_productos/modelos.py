"""Modelos del catálogo de dispositivos ecológicos de EcoTech Solutions."""

from __future__ import annotations

from typing import Any

try:  # Importación como paquete desde la raíz del repositorio.
    from .excepciones import StockInvalidoError
except ImportError:  # Ejecución desde el directorio del ejercicio.
    from excepciones import StockInvalidoError


class DispositivoEcologico:
    """Dispositivo ecológico con stock encapsulado y validado.

    Attributes:
        identificador: Código único del producto.
        nombre: Nombre comercial del producto.
        precio: Precio unitario en la moneda del catálogo.
        stock: Unidades disponibles; siempre un entero no negativo.
    """

    def __init__(
        self,
        identificador: str,
        nombre: str,
        stock: int,
        precio: float = 0.0,
    ) -> None:
        self.identificador = str(identificador).strip()
        self.nombre = str(nombre).strip()
        self.precio = float(precio)
        self.__stock = 0
        self.stock = stock

    @property
    def stock(self) -> int:
        """Cantidad de unidades disponibles."""
        return self.__stock

    @stock.setter
    def stock(self, valor: int) -> None:
        """Valida y asigna el stock, conservando el valor previo si falla.

        Raises:
            StockInvalidoError: si el valor no es un entero o es negativo.
        """
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise StockInvalidoError("El stock debe ser un número entero")

        if valor < 0:
            raise StockInvalidoError("El stock no puede ser negativo")

        self.__stock = valor

    def generar_ficha_tecnica(self) -> str:
        """Devuelve la ficha técnica general del dispositivo."""
        return (
            "Ficha técnica\n"
            f"Identificador: {self.identificador}\n"
            f"Nombre: {self.nombre}\n"
            f"Stock disponible: {self.stock}\n"
            f"Precio: ${self.precio:.2f}"
        )

    def to_dict(self) -> dict[str, Any]:
        """Serializa los atributos comunes a una estructura compatible con JSON."""
        return {
            "tipo": type(self).__name__,
            "identificador": self.identificador,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
        }


class PanelSolar(DispositivoEcologico):
    """Panel solar con atributos específicos de generación energética.

    Attributes:
        potencia_watts: Potencia nominal del panel en vatios.
        eficiencia: Eficiencia energética expresada en porcentaje (0 a 100).
        tecnologia: Tecnología de fabricación del panel.
    """

    def __init__(
        self,
        identificador: str,
        nombre: str,
        stock: int,
        potencia_watts: float,
        eficiencia: float,
        tecnologia: str = "Monocristalino",
        precio: float = 0.0,
    ) -> None:
        super().__init__(identificador, nombre, stock, precio)

        self.potencia_watts = float(potencia_watts)

        eficiencia = float(eficiencia)
        if not 0 < eficiencia <= 100:
            raise ValueError("La eficiencia debe estar entre 0 y 100")
        self.eficiencia = eficiencia

        self.tecnologia = str(tecnologia).strip()

    def generar_ficha_tecnica(self) -> str:
        """Devuelve la ficha técnica con los datos específicos del panel solar."""
        return (
            f"{super().generar_ficha_tecnica()}\n"
            f"Potencia nominal: {self.potencia_watts:.2f} W\n"
            f"Eficiencia energética: {self.eficiencia:.2f} %\n"
            f"Tecnología: {self.tecnologia}"
        )

    def to_dict(self) -> dict[str, Any]:
        """Serializa los atributos comunes y los específicos del panel solar."""
        datos = super().to_dict()
        datos.update(
            {
                "potencia_watts": self.potencia_watts,
                "eficiencia": self.eficiencia,
                "tecnologia": self.tecnologia,
            }
        )
        return datos
