"""APi de los tipos, realizacion del GRUD haci la BBDD y funciones de solucitud hacia la BBDD"""

from fastapi import APIRouter
from sqlalchemy.orm import Session
from bbdd import engine
from Models.Tipo import Tipo


router = APIRouter(prefix="/tipo", tags=["Tipo"])


@router.post("/alta")
def alta_tipo():
    """agregar un nuevo tipo"""
    pass


@router.get("/lista")
def lista_tipos():
    """se obtiene una lista de todos los tipos"""
    db = Session(engine)
    todos = db.query(Tipo).all()
    db.commit()
    db.close()
    return {"items": todos}


@router.post("/baja/{id}")
def baja_tipo(id):
    """se realiza una baja logica"""
    pass
