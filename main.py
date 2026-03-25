"""Archivo de configuracion del sistema"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Routing import R_Producto, R_Tipo, Factura
from seeder import add_tipos # add_productos, add_tipos_material, ferreteria 
#from seeder import eliminar_tablas

tags_metadata = []

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
#eliminar_tablas()
add_tipos()
#add_tipos_material()
#add_productos()
#ferreteria()
