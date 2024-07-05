from sqlalchemy import (
    func,
    String,
    Table,
    Column,
    ForeignKey,
    Boolean,
    Integer,
    DateTime,
)
from sqlalchemy.orm import Mapped, relationship
from bbdd import Base

asociacion_tabla = Table(
    "asociacion_tabla",
    Base.metadata,
    Column("factura_id", ForeignKey("facturas.id")),
    Column("producto_id", ForeignKey("productos.id")),
)


class Factura(Base):
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

    def __repr__(self):
        return {"id": self.id, "fecha_y_hora": self.fecha_y_hora, "total": self.total}

    def __str__(self):
        return "Nombre:" + self.total

    def listProductos(self):
        return self.productos
