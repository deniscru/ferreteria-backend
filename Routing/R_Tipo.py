from bbdd import engine
from fastapi import APIRouter
from sqlalchemy.orm import Session
from Models.Tipo import Tipo

router = APIRouter(prefix="/tipo", tags=["Tipo"])


@router.post("/alta")
def altaTipo():
    """agregar un nuevo tipo"""
    pass


@router.get("/lista")
def listaTipos():
    """se obtiene una lista de todos los tipos"""
    db = Session(engine)
    todos = db.query(Tipo).all()
    db.commit()
    db.close()
    return {"items": todos}


@router.post("/baja/{id}")
def bajaTipo(id):
    """se realiza una baja logica"""
    pass
