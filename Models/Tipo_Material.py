"""Diseño de la tabla relacional de los tipos de material que se presentan"""

from __future__ import annotations
from sqlalchemy import Boolean, String, Column, Integer
from bbdd import Base


class TipoMaterial(Base):
    """Tabla del tipo del material y sus atributos"""

    __tablename__ = "tipos_material"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(30))
    logico = Column(Boolean, default=True)

    def __init__(self, nombre):
        self.nombre = nombre

    def __dict__(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
        }
    
    def __repr__(self):
        string= "ID:"+self.id+" Nombre:"+self.nombre
        return string
