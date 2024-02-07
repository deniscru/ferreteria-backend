from fastapi import APIRouter
from sqlalchemy.orm import Session
from Models.Factura import Factura
from bbdd import engine

router = APIRouter(prefix="/factura", tags=["Factura"])


@router.post("/altaFactura")
def altaFactura():
    pass


@router.post("/editar/{id}")
def bajaFactura(id):
    pass


@router.get("/calcularGanancia")
def calcularGanancia():
    pass
