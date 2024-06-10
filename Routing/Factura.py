from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from sqlalchemy import update
from Models.Factura import Factura
from bbdd import engine
from pydantic import BaseModel
from datetime import datetime
import paginate

router = APIRouter(prefix="/factura", tags=["Factura"])


class requestFactura(BaseModel):
    total: float
    productos: dict


def calcularTotal(productos):
    total = 0
    for producto in productos:
        total = total + producto.precio_de_venta
    return total


# probar si anda
@router.post("/altaFactura")
def altaFactura(request: requestFactura):
    total = calcularTotal(request.productos)
    db = Session(engine)
    factura = Factura(datetime.now(), total, request.productos)
    db.add(factura)
    db.commit()
    db.close()
    return JSONResponse(
        status_code=200, content={"mensaje": "Menú agregado correctamente"}
    )


# probar si anda
@router.post("/eliminarFactura/{id}")
def eliminarFactura(id):
    db = Session(engine)
    if not db.query(exists().where(Factura.id == id)).scalar():
        return JSONResponse(
            status_code=400,
            content={"error": f"No existe la Factura con el id: {id}"},
        )
    stmt = update(Factura).where(Factura.id == id).values(logico=False)
    db.execute(stmt)
    db.commit()
    db.close()
    return JSONResponse(
        status_code=200,
        content={"mensaje": "El producto se elimino correctamente"},
    )


# probar si anda
@router.get("/{id}")
def obtenerFacturaId(id):
    db = Session(engine)
    factura = db.query(Factura).get(id)
    db.close()
    if factura:
        return factura
    else:
        return JSONResponse(
            status_code=404,
            content={"error": f"No existe el producto con id: {id}"},
        )


# probar si anda
@router.get("/lista/{page}")
def listaFacturas(page):
    db = Session(engine)
    lista_facturas = db.query(Factura).filter(Factura.logico == True).all()
    db.close()
    lista_paginada = paginate.Page(lista_facturas, page=page, items_per_page=10)
    return {
        "items": lista_paginada,
        "total_paginas": lista_paginada.page_count,
        "siguiente": lista_paginada.next_page,
        "anterior": lista_paginada.previous_page,
        "actual": page,
    }
