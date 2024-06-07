from fastapi import APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
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


class requestProductoEdit(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio_de_compra: float
    precio_de_venta: float
    cant: int
    tipo_id: int


class requestProductoPrecio(BaseModel):
    porcentaje: str
    lista: list[int]


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


@router.post("/actualizar/data/campos/{id}")
def actualizarProductoCampos(id, request: requestProducto):
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
            tipo_id=request.tipo_id,
        )
    )
    db.execute(stmt)
    db.commit()
    db.close()
    return JSONResponse(
        status_code=200,
        content={"mensaje": "El producto se actualizo correctamente"},
    )


@router.post("/actualizar/data")
def actualizarPrecioProductos(request: requestProductoPrecio):
    """se va a actualizar el precio de los productos que se pasan por lista segun el porcentaje deseado"""
    db = Session(engine)

    for prodSelec in request.lista:
        producto = db.query(Producto).get(int(prodSelec))
        aumento = (producto.precio_de_compra * int(request.porcentaje)) / 100
        if int(prodSelec) == int(producto.id):
            stmt = (
                update(Producto)
                .where(Producto.id == int(prodSelec))
                .values(
                    precio_de_venta=producto.precio_de_compra + aumento,
                    date=datetime.now(),
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
    """obtener todos los productos paginados sin filtro"""
    db = Session(engine)
    lista_productos = db.query(Producto).filter(Producto.logico == True).all()
    db.close()
    lista_paginada = paginate.Page(lista_productos, page=page, items_per_page=6)
    print("listado normal")
    return {
        "items": lista_paginada,
        "total_paginas": lista_paginada.page_count,
        "siguiente": lista_paginada.next_page,
        "anterior": lista_paginada.previous_page,
        "actual": page,
    }


@router.get("/lista/Tipo/{page}/{tipo}")
def listaProductoTipo(page, tipo):
    """obtener todos los productos segun el tipo"""
    db = Session(engine)
    lista_productos = (
        db.query(Producto)
        .filter(Producto.logico == True)
        .filter(Producto.tipo_id == tipo)
        .all()
    )
    print("filtro por tipo")
    db.close()
    lista_paginada = paginate.Page(lista_productos, page=int(page), items_per_page=6)

    return {
        "items": lista_paginada,
        "total_paginas": lista_paginada.page_count,
        "siguiente": lista_paginada.next_page,
        "anterior": lista_paginada.previous_page,
        "actual": page,
    }


@router.get("/lista/Nombre/{page}/{nombre}")
def listaProductoNombre(page, nombre):
    """obtener todos los productos segun el tipo segun el nombre"""
    db = Session(engine)
    lista_productos = (
        db.query(Producto)
        .filter(Producto.logico == True)
        .filter(Producto.nombre.like("%" + nombre + "%"))
        .all()
    )
    db.close()
    lista_paginada = paginate.Page(lista_productos, page=int(page), items_per_page=6)
    print("filtro por nombre")

    return {
        "items": lista_paginada,
        "total_paginas": lista_paginada.page_count,
        "siguiente": lista_paginada.next_page,
        "anterior": lista_paginada.previous_page,
        "actual": page,
    }


@router.get("/lista/TipoYNombre/{page}/{tipo}/{nombre}")
def listaProductoTipoYNombre(page, tipo, nombre):
    """obtener todos los productos segun el tipo y nombre"""
    db = Session(engine)
    lista_productos = (
        db.query(Producto)
        .filter(Producto.logico == True)
        .filter(Producto.tipo_id == tipo)
        .filter(Producto.nombre.like("%" + nombre + "%"))
        .all()
    )
    db.close()
    lista_paginada = paginate.Page(lista_productos, page=int(page), items_per_page=6)
    print("filtro por tipo y nombre")

    return {
        "items": lista_paginada,
        "total_paginas": lista_paginada.page_count,
        "siguiente": lista_paginada.next_page,
        "anterior": lista_paginada.previous_page,
        "actual": page,
    }


@router.get("/lista/preciosTipo/{tipo}")
def obtenerlistaPreciosTipo(tipo):
    """obtener todos los productos segun el tipo para la imcrementacion de los productos"""
    db = Session(engine)
    lista_productos = (
        db.query(Producto)
        .filter(Producto.logico == True)
        .filter(Producto.tipo_id == tipo)
        .all()
    )
    db.close()
    for prod in lista_productos:
        prod.date = prod.date.date()
    return {
        "items": lista_productos,
    }


@router.get("/lista/precios/todos/increm")
def obtenerListaPrecios():
    """obtener todos los productos sin paginacion para la seccion de incremenracion de precio"""
    db = Session(engine)
    lista_productos = db.query(Producto).filter(Producto.logico == True).all()
    db.close()
    for prod in lista_productos:
        prod.date = prod.date.date()
    return {
        "items": lista_productos,
    }
