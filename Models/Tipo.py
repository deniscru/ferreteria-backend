"""Diseño de la tabla relacional de los tipos de los productos"""

from __future__ import annotations
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from bbdd import Base


class Tipo(Base):
    """Tabla del Tipo y sus atributos"""
    __tablename__ = "tipos"

    id:Mapped[int] = mapped_column(primary_key=True, name="id")
    _nombre:Mapped[str] = mapped_column(String(30), name="nombre")
    _logico:Mapped[bool] = mapped_column(Boolean, default=True, name="logico")

    def __init__(self, nombre):
        self.nombre = nombre

    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor):
        self._nombre= valor
    