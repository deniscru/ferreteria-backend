"""APi de la factura, realizacion del GRUD haci la base de datos, 
y funciones de solucitud hacia la BBDD"""

from datetime import datetime
import paginate
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import func, select, update
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from pydantic import BaseModel
from Models.Factura import Factura, asociacion_tabla
from Models.Producto import Producto
from bbdd import engine


router = APIRouter(prefix="/factura", tags=["Factura"])


class RequestFactura(BaseModel):
    """Estructura de datos de los datos a recibir"""
    productos: list[dict]


# chequeado
@router.post("/altaFactura")
def alta_factura(request: RequestFactura):
    """Api del alta de una factura a la base de datos"""

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
def eliminar_factura(id):
    """Elimina una factura de la BBDD con el ID recibido"""
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
def obtener_facturaid(id):
    """Realiza un busqueda de una factura por el ID recibido y en caso de encontrarlo, 
        devuelve los datos del mismo"""
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
def lista_facturas(page):
    """Devuelve una lista de facturas paginada"""
    db = Session(engine)
    lista_facturas = db.query(Factura).filter(bool(Factura.logico)).all()
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
def lista_facturas_hoy():
    """Devuelve una lista de todas las facturas realizadas en el dia de hoy, sin paginacion"""
    db = Session(engine)
    lista_facturas = db.query(Factura).filter(bool(Factura.logico)).all() #Chequear si el true es necesario

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
def fac_lista_productos(id):
    """Devuelve una lista de todos los productos de una factura realizada"""
    db = Session(engine)

    consulta_aux = (
        select(
            Producto.nombre,
            Producto.precio_de_venta,
            Producto.precio_de_compra,
            asociacion_tabla.columns.producto_id, 
            func.count(asociacion_tabla.columns.producto_id),
        )
        .join_from(Producto, asociacion_tabla)
        .where(asociacion_tabla.columns.factura_id == id)
        .group_by(asociacion_tabla.columns.producto_id)
    )

    facturas = db.execute(consulta_aux)
    lista = []
    for nombre, pr_venta, pr_compra, idp, cant in facturas:
        lista.append(
            {
                "nombre": nombre,
                "prVenta": pr_venta,
                "prCompra": pr_compra,
                "id": idp,
                "cant": cant,
            }
        )
    db.close()
    return {"lista": lista}
