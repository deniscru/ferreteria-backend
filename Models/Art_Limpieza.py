from __future__ import annotations
from sqlalchemy import DateTime, ForeignKey, Boolean, Column, Float, Integer
from sqlalchemy.orm import relationship
from bbdd import Base


class Art_Limpieza(Base):
    __tablename__ = "art_limpieza"

    id = Column(Integer, primary_key=True)
    pr_venta_1litro = Column(Float)
    pr_venta_2litros = Column(Float)
    pr_venta_5litros = Column(Float)
    logico = Column(Boolean, default=True)
    date = Column(DateTime)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    producto = relationship("Producto", lazy="joined")

    def __init__(self, p_1litro, p_2litro, p_5litro, date, prod_id, prod):
        self.pr_venta_1litro = p_1litro
        self.pr_venta_2litros = p_2litro
        self.pr_venta_5litros = p_5litro
        self.date = date
        self.producto = prod
        self.producto_id = prod_id

    def __repr__(self):
        return {
            "id": self.id,
            "1litro": self.pr_venta_1litro,
            "2litros": self.pr_venta_2litros,
            "5litros": self.pr_venta_5litros,
        }
