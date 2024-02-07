from __future__ import annotations
from sqlalchemy import String, ForeignKey, Boolean, Column, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import LONGTEXT
from bbdd import Base


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(300))
    nombre_alias = Column(String(300))
    descripcion = Column(String(300))
    medida = Column(String(20))
    precio_de_compra = Column(Float)
    precio_de_venta = Column(Float)
    cant = Column(Integer)
    logico = Column(Boolean, default=True)
    imagen = Column(LONGTEXT)
    tipo_id = Column(Integer, ForeignKey("tipos.id"))
    tipo = relationship("Tipo", lazy="joined")

    def __init__(
        self,
        nombre,
        nombre_alias,
        descripcion,
        medida,
        precio_de_compra,
        precio_de_venta,
        cant,
        imagen,
        tipo_id,
        tipo,
    ):
        self.nombre = nombre
        self.nombre_alias = nombre_alias
        self.descripcion = descripcion
        self.medida = medida
        self.precio_de_compra = precio_de_compra
        self.precio_de_venta = precio_de_venta
        self.cant = cant
        self.imagen = imagen
        self.tipo_id = tipo_id
        self.tipo = tipo

    def __repr__(self):
        return {"id": self.id, "nombre": self.nombre, "descripcion": self.descripcion}
