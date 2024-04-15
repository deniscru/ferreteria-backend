from __future__ import annotations
from sqlalchemy import ForeignKey, Boolean, Integer, Column
from sqlalchemy.orm import relationship
from bbdd import Base


class Plomeria(Base):
    __tablename__ = "plomeria"

    id = Column(Integer, primary_key=True)
    logico = Column(Boolean, default=True)
    tipo_material_id = Column(Integer, ForeignKey("productos.id"))
    tipo_material = relationship("Producto", lazy="joined")

    def __init__(self, material_id, material):
        self.tipo_material = material
        self.tipo_material_id = material_id

    def __repr__(self):
        return {
            "id": self.id,
            "material_id": self.tipo_material_id,
        }
