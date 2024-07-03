from __future__ import annotations
from sqlalchemy import String, ForeignKey, Boolean, Column, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import LONGTEXT
from bbdd import Base


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(300))
    descripcion = Column(String(300))
    precio_de_compra = Column(Float)
    precio_de_venta = Column(Float)
    cant = Column(Integer)
    logico = Column(Boolean, default=True)
    date = Column(DateTime)
    tipo_id = Column(Integer, ForeignKey("tipos.id"))
    tipo = relationship("Tipo", lazy="joined")

    def __init__(
        self,
        nombre,
        descripcion,
        precio_de_compra,
        precio_de_venta,
        cant,
        tipo_id,
        tipo,
        date,
    ):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_de_compra = precio_de_compra
        self.precio_de_venta = precio_de_venta
        self.cant = cant
        self.tipo_id = tipo_id
        self.tipo = tipo
        self.date = date

    def __repr__(self):
        return {"id": self.id, "nombre": self.nombre, "descripcion": self.descripcion}

    def __str__(self):
        return "Nombre: " + self.nombre
