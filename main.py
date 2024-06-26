from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Models import *
from bbdd import engine, Base
from seeder import add_productos, add_tipos, add_tipos_material, ferreteria
from Routing import R_Producto, R_Tipo, Factura

tags_metadata = []
# Base.metadata.create_all(engine)

app = FastAPI()
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(R_Producto.router)
app.include_router(R_Tipo.router)
app.include_router(Factura.router)
# add_tipos()
# add_tipos_material()
# add_productos()
# ferreteria()
