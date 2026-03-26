"""Diseño de la tabla relacional de los tipos de material que se presentan"""

from __future__ import annotations
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from bbdd import Base


class TipoMaterial(Base):
    """Tabla del tipo del material y sus atributos"""

    __tablename__ = "tipos_material"

    _id: Mapped[int] = mapped_column(name="id", primary_key=True)
    _nombre:Mapped[str] = mapped_column(String(30), name="nombre")
    _logico:Mapped[bool] = mapped_column(name="logico", default=True)

    def __init__(self, nombre):
        self.nombre = nombre

    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor):
        self._nombre =valor
