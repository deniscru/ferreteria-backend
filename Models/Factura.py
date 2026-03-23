"""Diseño de la tabla relacional de la Factura y su asociacion con la tabla de producto"""

from sqlalchemy import String, Table, Column, ForeignKey, Boolean, Integer, DateTime
from sqlalchemy.orm import relationship
from bbdd import Base

asociacion_tabla = Table(
    "asociacion_tabla",
    Base.metadata,
    Column("factura_id", ForeignKey("facturas.id")),
    Column("producto_id", ForeignKey("productos.id")),
)


class Factura(Base):
    """Tabla de una Factura de productos"""

    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True)
    total = Column(String(30))
    logico = Column(Boolean, default=True)
    fecha_y_hora = Column(DateTime)
    productos = relationship("Producto", secondary=asociacion_tabla, lazy="joined")

    def __init__(self, fecha_y_hora, total, productos):
        self.fecha_y_hora = fecha_y_hora
        self.total = total
        self.productos = productos

    def __dict__(self):
        return {"id": self.id, "fecha_y_hora": self.fecha_y_hora, "total": self.total}
    
    def __repr__(self):
        string="id: "+ self.id+ " fecha_y_hora:" +self.fecha_y_hora+ " total:" +self.total
        return string

    def __str__(self):
        return "Nombre:" + self.total

    def listProductos(self):
        """Devuelve una lista de productos"""

        return self.productos
