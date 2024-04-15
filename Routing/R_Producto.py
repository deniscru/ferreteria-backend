from fastapi import APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists, select
from sqlalchemy import update
from pydantic import BaseModel
from bbdd import engine
from Models.Producto import Producto
from Models.Tipo import Tipo
from fastapi.responses import JSONResponse
from datetime import datetime
import paginate

router = APIRouter(
    prefix="/producto",
    tags=["Producto"],
)


class requestProducto(BaseModel):
    nombre: str
    descripcion: str
    precio_de_compra: float
    precio_de_venta: float
    cant: int
    tipo_id: int


class requestProductoPrecio(BaseModel):
    porcentaje: int


class requestBusqueda(BaseModel):
    nombre: str


@router.post("/alta")
def altaProducto(requestData: requestProducto):
    """se va a realizar una carga de un producto"""
    db = Session(engine)
    tipo = db.query(Tipo).get(requestData.tipo_id)
    if not tipo:
        return JSONResponse(
            status_code=404,
            content={"error": f"No se encontro el tipo con id: {id}"},
        )
    producto = Producto(
        requestData.nombre,
        requestData.descripcion,
        requestData.precio_de_compra,
        requestData.precio_de_venta,
        requestData.cant,
        requestData.tipo_id,
        tipo,
        date=datetime.now(),
    )
    # Checkear q no exista un Producto con el mismo nombre
    if db.query(exists().where(Producto.nombre == producto.nombre)).scalar():
        return JSONResponse(
            status_code=400,
            content={
                "error": f"Ya existe el producto con el nombre: {requestData.nombre}"
            },
        )
    db.add(producto)
    db.commit()
    db.close()

    return JSONResponse(
        status_code=200, content={"mensaje": "Menú agregado correctamente"}
    )


@router.post("/eliminarProducto/{id}")
def bajaProducto(id):
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


@router.post("/actualizarProducto/{id}")
def actualizarProducto(id, request: requestProducto):
    """se va a actualizar un producto en particular"""
    db = Session(engine)
    if db.query(
        exists().where(Producto.nombre == request.nombre).where(Producto.id != id)
    ).scalar():
        return JSONResponse(
            status_code=400,
            content={
                "error": f"No se puede editar el producto con el id: {id}, por que ya existe un producto con el mismo nombre"
            },
        )
    stmt = (
        update(Producto)
        .where(Producto.id == id)
        .values(
            nombre=request.nombre,
            descripcion=request.descripcion,
            precio_de_compra=request.precio_de_compra,
            precio_de_venta=request.precio_de_venta,
            cant=request.cant,
        )
    )
    db.execute(stmt)
    db.commit()
    db.close()
    return JSONResponse(
        status_code=200,
        content={"mensaje": "El producto se actualizo correctamente"},
    )


@router.post("/actualizarProductosPrecio/")
def actualizarPrecioProductos(request: requestProductoPrecio):
    """se va a actualizar el precio de cada producto segun el tipo seleccionado"""
    db = Session(engine)
    todos = db.query(Producto).all()
    for producto in todos:
        aumento = producto.precio_de_compra * (request.porcentaje / 100)
        stmt = (
            update(Producto)
            .where(Producto.id == producto.id)
            .values(
                precio_de_venta=producto.precio_de_compra + aumento,
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


@router.get("/{id}")
def obtenerProducto(id):
    """obtener un producto segun su id"""
    db = Session(engine)
    prod = db.query(Producto).get(id)
    db.close()
    if prod:
        return prod
    else:
        return JSONResponse(
            status_code=404,
            content={"error": f"No existe el producto con id: {id}"},
        )


@router.get("/lista/{page}")
def listaProducto(page):
    """obtener todos los productos"""
    db = Session(engine)
    lista_productos = db.query(Producto).filter(Producto.logico == True).all()
    db.close()
    lista_paginada = paginate.Page(lista_productos, page=page, items_per_page=6)
    return {"items": lista_paginada, "total_paginas": lista_paginada.page_count}


@router.get("/listaTipo/{page}/{tipo}")
def listaProductoTipo(page, tipo):
    """obtener todos los productos segun el tipo"""
    print(tipo, page)
    db = Session(engine)
    lista_productos = (
        db.query(Producto)
        .filter(Producto.logico == True)
        .filter(Producto.tipo_id == tipo)
        .all()
    )
    db.close()
    lista_paginada = paginate.Page(lista_productos, page=int(page), items_per_page=6)
    print(lista_paginada)
    return {"items": lista_paginada, "total_paginas": lista_paginada.page_count}


@router.get("/listaBusqueda/{page}/{tipo}")
def buscarProductos(page, tipo, request: requestBusqueda):
    """se va a realizar una busqueda de un producto o productos segun su tipo y nombre"""
    db = Session(engine)
    lista_productos = (
        db.query(Producto)
        .filter(Producto.logico == True)
        .filter(Producto.tipo_id == tipo)
        .filter(Producto.nombre == request.nombre)
        .all()
    )
    db.close()
    lista_paginada = paginate.Page(lista_productos, page=page, items_per_page=6)
    return {"items": lista_paginada, "total_paginas": lista_paginada.page_count}
