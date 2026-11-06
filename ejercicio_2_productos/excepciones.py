"""Excepciones específicas del dominio del catálogo EcoTech."""


class StockInvalidoError(Exception):
    """Se lanza cuando se intenta asignar un stock inválido."""
