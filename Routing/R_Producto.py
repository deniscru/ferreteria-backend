"""APi de los productos, realizacion del GRUD haci la BBDD,
     y funciones de solucitud hacia la BBDD"""

from datetime import datetime
import paginate
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from sqlalchemy import update
from pydantic import BaseModel
from bbdd import engine
from Models.Producto import Producto
from Models.Tipo import Tipo


router = APIRouter(
    prefix="/producto",
    tags=["Producto"],
)

class RequestProducto(BaseModel):
    """Formato de datos que vamos a recibir por un producto"""
    nombre: str
    descripcion: str
    precio_de_compra: float
    precio_de_venta: float
    cant: int
    tipo_id: int


class RequestProductoEdit(BaseModel):
    """Formato de datos que vamos a recibir por un producto para editarlos"""
    id: int
    nombre: str
    descripcion: str
    precio_de_compra: float
    precio_de_venta: float
    cant: int
    tipo_id: int


class RequestProductoPrecio(BaseModel):
    """Formato de datos que vamos a recibir para aumentar el precio de un producto"""
    porcentaje: int
    lista: list[int]


class RequestBusqueda(BaseModel):
    """Formato de datos para recibir un nombre de producto y generar una busqueda de ella """
    nombre: str

#pasarlo a un archivo nuevo de metodos helper
def paginacion_de_lista(lista, page=1):
    for prod in lista:
        prod.date = prod.date.date()
    lista_paginada = paginate.Page(lista, page=page, items_per_page=10)
    return {
        "items": lista_paginada,
        "total_paginas": lista_paginada.page_count,
        "siguiente": lista_paginada.next_page,
        "anterior": lista_paginada.previous_page,
        "actual": page,
    }

# ultimo chequeo realizado es el: 26/3/2026
@router.post("/alta")
def alta_producto(request: RequestProducto):
    """se va a realizar una carga de un producto"""
    db = Session(engine)
    tipo = db.query(Tipo).get(request.tipo_id)
    if not tipo:
        return JSONResponse(
            status_code=404,
            content={"error": f"No se encontro el tipo con id: {id}"},
        )
    producto = Producto(
        request.nombre,
        request.descripcion,
        request.precio_de_compra,
        request.precio_de_venta,
        request.cant,
        request.tipo_id,
        tipo,
        date=datetime.now(),
    )
    # Checkear q no exista un Producto con el mismo nombre
    if db.query(exists().where(Producto._nombre == producto.nombre)).scalar():
        return JSONResponse(
            status_code=400,
            content={
                "error": f"Ya existe el producto con el nombre: {request.nombre}"
            },
        )
    db.add(producto)
    db.commit()
    db.close()

    return JSONResponse(
        status_code=200, content={"mensaje": "Producto agregado correctamente"}
    )


# chequeado
@router.post("/eliminarProducto/{id}")
def baja_producto(id):
    """se va a realizar una baja logica"""
    db = Session(engine)
    if not db.query(exists().where(Producto.id == id)).scalar():
        return JSONResponse(
            status_code=400,
            content={"error": f"No existe un producto con el id: {id}"},
        )
    stmt = update(Producto).where(Producto.id == id).values(logico=False)
    db.execute(stmt)
    db.commit()
    db.close()
    return JSONResponse(
        status_code=200,
        content={"mensaje": "El producto se elimino correctamente"},
    )


# realizar ultimo chequeo, pasar el producto par actualizar en formulario
@router.post("/actualizar/data/campos/{ida}")
def actualizar_producto_campos(ida, request: RequestProducto):
    """se va a actualizar un producto en particular"""
    db = Session(engine)
    if db.query(
        exists().where(Producto._nombre == request.nombre).where(Producto.id != ida)
    ).scalar():
        return JSONResponse(
            status_code=400,
            content={
                "error": f"No se puede editar el producto con el id: {ida},"+
                        " por que ya existe un producto con el mismo nombre"
            },
        )
    stmt = (
        update(Producto)
        .where(Producto.id == ida)
        .values(
            _nombre=request.nombre,
            _descripcion=request.descripcion,
            _precio_de_compra=request.precio_de_compra,
            _precio_de_venta=request.precio_de_venta,
            _cant=request.cant,
            _tipo_id=request.tipo_id,
        )
    )
    db.execute(stmt)
    db.commit()
    db.close()
    return JSONResponse(
        status_code=200,
        content={"mensaje": "El producto se actualizo correctamente"},
    )


# chequeado
@router.post("/actualizar/data")
def actualizar_precio_productos(request: RequestProductoPrecio):
    """ se va a actualizar el precio de los productos 
        que se pasan por lista segun el porcentaje deseado"""
    db = Session(engine)
    #debo chequear si las id de la lista existen en la BD 
    for producto in request.lista:
        prod = db.query(Producto).get(int(producto))
        aumento = (prod.precio_de_compra * int(request.porcentaje)) / 100
        if int(producto) == int(prod.id):
            stmt = (
                update(Producto)
                .where(Producto.id == int(producto))
                .values(
                    _precio_de_venta=prod.precio_de_compra + aumento,
                    _date=datetime.now(),
                )
            )
            db.execute(stmt)
    db.commit()
    db.close()
    return JSONResponse(
        status_code=200,
        content={
            "mensaje": "El listado de productos se actualizo correctamente el precio"
        },
    )


# chequeado, queda un detalle en el componente del front
@router.get("/{idp}")
def obtener_producto(idp):
    """obtener un producto segun su id"""
    db = Session(engine)
    prod = db.query(Producto).get(idp)
    db.close()
    if prod:
        return prod
    else:
        return JSONResponse(
            status_code=404,
            content={"error": f"No existe el producto con id: {idp}"},
        )


# chequeado
@router.get("/lista/{page}")
def lista_producto(page):
    """obtener todos los productos paginados sin filtro"""
    db = Session(engine)
    lista_productos = db.query(Producto).filter(bool(Producto.logico)).all()
    db.close()
    return paginacion_de_lista(lista_productos, page)


# Chequeado
@router.get("/lista/Tipo/{page}/{tipo}")
def lista_producto_tipo(page, tipo):
    """obtener todos los productos segun el tipo"""
    db = Session(engine)
    lista_productos = (
        db.query(Producto)
        .filter(bool(Producto.logico))
        .filter(Producto._tipo_id == tipo)
        .all()
    )
    db.close()
    return paginacion_de_lista(lista_productos, page=int(page))


# Chequeado
@router.get("/lista/NombreOCodigo/{page}/{dato}")
def lista_producto_nombre(page, dato):
    """obtener todos los productos segun el tipo segun el nombre"""
    db = Session(engine)
    if not dato.isdigit():
        lista_productos = (
            db.query(Producto)
            .filter(bool(Producto.logico))
            .filter(Producto._nombre.like("%" + dato + "%"))
            .all()
        )
    else:
        lista_productos = (
            db.query(Producto)
            .filter(bool(Producto.logico))
            .filter(Producto.id == dato)
            .all()
        )
    db.close()
    if (len(lista_productos)==0):
        return JSONResponse(
            status_code=400,
            content={
                "error": f"No se encontraron productos con el nombre: {dato}"
            })
    return paginacion_de_lista(lista_productos, page=int(page))


# Chequeado
@router.get("/lista/TipoYNombreOCodigo/{page}/{tipo}/{dato}")
def lista_prod_tipo_nombre(page, tipo, dato):
    """obtener todos los productos segun el tipo y nombre"""
    db = Session(engine)
    if not dato.isdigit():
        lista_productos = (
            db.query(Producto)
            .filter(bool(Producto.logico))
            .filter(Producto._tipo_id == tipo)
            .filter(Producto._nombre.like("%" + dato + "%"))
            .all()
        )
    else:
        lista_productos = (
            db.query(Producto)
            .filter(bool(Producto.logico))
            .filter(Producto._tipo_id == tipo)
            .filter(Producto.id == dato)
            .all()
        )
    db.close()
    return paginacion_de_lista(lista_productos, page=int(page))


# realizar ultimo chequeo, agregar paginacion
@router.get("/lista/preciosTipo/{tipo}")
def obtenerlista_preciostipo(tipo):
    """obtener todos los productos segun el tipo para la imcrementacion de los productos"""
    db = Session(engine)
    lista_productos = (
        db.query(Producto)
        .filter(bool(Producto.logico))
        .filter(Producto._tipo_id == tipo)
        .all()
    )
    db.close()
    for prod in lista_productos:
        prod.date = prod.date.date()
    return {
        "items": lista_productos,
    }


# realizar ultimo chequeo, agregar paginacion
@router.get("/lista/precios/todos/increm")
def obtener_lista_precios():
    """obtener todos los productos sin paginacion para la seccion de incremenracion de precio"""
    db = Session(engine)
    lista_productos = db.query(Producto).filter(bool(Producto.logico)).all()
    db.close()
    for prod in lista_productos:
        prod.date = prod.date.date()
    return {
        "items": lista_productos,
    }
