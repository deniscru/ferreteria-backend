from __future__ import annotations
from sqlalchemy import Boolean, String, Column, Integer
from typing import List
from bbdd import Base


class Tipo_Material(Base):
    __tablename__ = "tipos_material"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(30))
    logico = Column(Boolean, default=True)

    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
        }
