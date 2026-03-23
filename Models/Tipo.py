"""Diseño de la tabla relacional de los tipos de los productos"""

from __future__ import annotations
from sqlalchemy import Boolean, String, Column, Integer
from bbdd import Base


class Tipo(Base):
    """Tabla del Tipo y sus atributos"""
    __tablename__ = "tipos"

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
        string= "id: "+self.id+" Nombre:"+self.nombre
        return string
