"""Rutas principales del proyecto Django."""

from django.urls import include, path

urlpatterns = [
    path("", include("auditoria.urls")),
]
