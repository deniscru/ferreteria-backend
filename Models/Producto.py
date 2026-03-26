"""Diseño de la tabla relacional de los Productos"""

from __future__ import annotations
from datetime import datetime
from sqlalchemy import String, ForeignKey, Boolean, Column, Integer, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from bbdd import Base


class Producto(Base):
    """Tabla de los Productos y sus atributos"""

    __tablename__ = "productos"

    _id:Mapped[int] = mapped_column(primary_key=True, name="id")
    _nombre:Mapped[str] = mapped_column(String(300), name="nombre")
    _descripcion:Mapped[str] = mapped_column(String(300), name="descripcion")
    _precio_de_compra:Mapped[float] = mapped_column(name="precio_de_compra", default=0)
    _precio_de_venta:Mapped[float] = mapped_column(name="precio_de_venta", default=0)
    _cant:Mapped[int] = mapped_column(name="cant", default=0)
    _logico:Mapped[bool] = mapped_column(default=True, name="logico")
    _date:Mapped[datetime] = mapped_column(DateTime, name="date")
    _tipo_id:Mapped[int] = mapped_column(ForeignKey("tipos.id"), name="tipo_id")
    _tipo = relationship("Tipo", lazy="joined")

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

    @property
    def nombre(self):
        return self._nombre
    
    @property
    def descripcion(self):
        return self._descripcion
    
    @property
    def precio_de_compra(self):
        return self._precio_de_compra
    
    @property
    def precio_de_venta(self):
        return self._precio_de_venta
    
    @property
    def cant(self):
        return self._cant
    
    @property
    def logico(self):
        return self._logico
    
    @property
    def date(self):
        return self._date
    
    @property
    def tipo_id(self):
        return self._tipo_id
    
    @property
    def tipo(self):
        """Probar si anda correctamente"""
        return self._tipo
    
    @nombre.setter
    def nombre(self, valor):
        self._nombre=valor

    @descripcion.setter
    def descripcion(self, valor):
        self._descripcion=valor

    @precio_de_compra.setter
    def precio_de_compra(self, valor_compra):
        self._precio_de_compra=valor_compra

    @precio_de_venta.setter
    def precio_de_venta(self, valor_venta):
        self._precio_de_venta=valor_venta

    @cant.setter
    def cant(self, cant):
        self._cant=cant

    @logico.setter
    def logico(self, logico):
        self._logico= logico

    @date.setter
    def date(self, valor):
        self._date= valor

    @tipo_id.setter
    def tipo_id(self, tipo_id):
        self._tipo_id= tipo_id

    @tipo.setter
    def tipo(self, tipo):
        self._tipo=tipo