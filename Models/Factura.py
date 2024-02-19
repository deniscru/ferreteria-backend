from datetime import datetime
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

print("se ejecutp")

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
    productos = relationship("Producto", secondary=asociacion_tabla, lazy="joined")

    def __init__(self, fecha_y_hora, total, producto_id):
        self.fecha_y_hora = fecha_y_hora
        self.total = total
        self.producto_id = producto_id

    def __repr__(self):
        return {
            "id": self.id,
            "fecha_y_hora": self.fecha_y_hora,
            "total": self.total,
        }