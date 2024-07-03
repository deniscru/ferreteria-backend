from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from sqlalchemy import update
from Models.Factura import Factura, asociacion_tabla
from Models.Producto import Producto
from bbdd import engine
from pydantic import BaseModel
from datetime import datetime
import paginate

router = APIRouter(prefix="/factura", tags=["Factura"])


class requestFactura(BaseModel):
    productos: list[dict]


# chequeado
@router.post("/altaFactura")
def altaFactura(request: requestFactura):

    db = Session(engine)
    lista = []
    total = 0
    for prod in request.productos:
        producto = db.query(Producto).get(prod["id"])
        if prod["cant"] > producto.cant:
            return JSONResponse(
                status_code=400,
                content={
                    "mensaje": "La cantidad de productos vendido supera al disponible"
                },
            )
        else:
            stmt = (
                update(Producto)
                .where(Producto.id == int(prod["id"]))
                .values(
                    cant=producto.cant - prod["cant"],
                    date=datetime.now().date(),
                )
            )
            db.execute(stmt)
        for i in range(prod["cant"]):
            lista.append(producto)

        total = total + (producto.precio_de_venta * prod["cant"])

    factura = Factura(datetime.now(), total, lista)
    db.add(factura)
    db.commit()
    db.close()
    return JSONResponse(
        status_code=200, content={"mensaje": "Menú agregado correctamente"}
    )


# chequeado
@router.post("/eliminar/{id}")
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
        content={"mensaje": "La factura se elimino correctamente"},
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


# chequeado
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


# chequeado
@router.get("/lista/venta/hoy")
def listaFacturas():
    db = Session(engine)
    lista_facturas = db.query(Factura).filter(Factura.logico == True).all()

    lista_nuevo = []
    for i in lista_facturas:
        if i.fecha_y_hora == datetime.now().date():
            lista_nuevo.append(i)
    db.close()
    return {
        "items": lista_nuevo,
    }


# Chequeado
@router.get("/lista/productos/{id}")
def FacListaProductos(id):
    db = Session(engine)
    facturas = db.query(Factura).filter(Factura.id == id).all()
    lista_productos = (
        db.query(asociacion_tabla)
        .filter(asociacion_tabla.columns.factura_id == id)
        .all()
    )

    if len(lista_productos) == 0:
        return JSONResponse(
            status_code=404,
            content={"error": f"No existe la factura con el id: {id}"},
        )
    prod_cant = {}
    for dato1, dato2 in lista_productos:
        if dato2 in prod_cant.keys():
            prod_cant[dato2] += 1
        else:
            prod_cant[dato2] = 0

    listProductos = facturas[0].listProductos()

    db.close()
    return {"lista": listProductos, "lista_cant": prod_cant}
