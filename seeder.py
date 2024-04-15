from sqlalchemy.orm import Session
from bbdd import engine
from Models.Tipo import Tipo
from Models.Producto import Producto
from Models.Tipo_Material import Tipo_Material
from datetime import datetime


def add_tipos():
    with Session(engine) as session:
        t1 = Tipo(nombre="Electricidad")
        t2 = Tipo(nombre="Plomeria")
        t3 = Tipo(nombre="Ferreteria")
        t4 = Tipo(nombre="Limpieza")

        session.add_all([t1, t2, t3, t4])
        session.commit()
        session.close()

    """db.execute(
        "INSERT INTO `tipos` VALUES (1,'Electricidad', 1),(2,'Plomeria', 1),(3,'Ferreteria', 1),(4,'Limpieza', 1);"
    )"""


def add_tipos_material():
    with Session(engine) as session:
        t1 = Tipo_Material(nombre="politileno")
        t2 = Tipo_Material(nombre="termo fusion")
        t3 = Tipo_Material(nombre="polipropileno o pp")
        t4 = Tipo_Material(nombre="PVP")
        t5 = Tipo_Material(nombre="awaduc")
    session.add_all([t1, t2, t3, t4, t5])
    session.commit()
    session.close()


def add_productos():
    with Session(engine) as session:
        ferre = session.query(Tipo).get(3)
        elec = session.query(Tipo).get(1)
        plom = session.query(Tipo).get(2)
        lim = session.query(Tipo).get(4)

        p1 = Producto(
            nombre="Martillo",
            descripcion="Martillo para carpinteria",
            precio_de_compra=12.000,
            precio_de_venta=15.000,
            cant=3,
            tipo_id=3,
            tipo=ferre,
            date=datetime.now(),
        )
        p2 = Producto(
            nombre="metro",
            descripcion="metro para medir",
            precio_de_compra=8.000,
            precio_de_venta=12.000,
            cant=4,
            tipo_id=3,
            tipo=ferre,
            date=datetime.now(),
        )
        p3 = Producto(
            nombre="destornillador filip",
            descripcion="destornillador de punta plana",
            precio_de_compra=1.000,
            precio_de_venta=2.000,
            cant=6,
            tipo_id=3,
            tipo=ferre,
            date=datetime.now(),
        )
        p4 = Producto(
            nombre="Codo 90 grados",
            descripcion="codo de plomeria con angulo de 90 grados",
            precio_de_compra=1.500,
            precio_de_venta=2.200,
            cant=10,
            tipo_id=2,
            tipo=plom,
            date=datetime.now(),
        )
        p5 = Producto(
            nombre="teflon",
            descripcion="",
            precio_de_compra=1.000,
            precio_de_venta=2.100,
            cant=20,
            tipo_id=2,
            tipo=plom,
            date=datetime.now(),
        )
        p6 = Producto(
            nombre="caño de luz",
            descripcion="",
            precio_de_compra=23.750,
            precio_de_venta=25.000,
            cant=20,
            tipo_id=1,
            tipo=elec,
            date=datetime.now(),
        )
        p7 = Producto(
            nombre="toma hembra",
            descripcion="toma para alargue",
            precio_de_compra=400,
            precio_de_venta=800,
            cant=23,
            tipo_id=1,
            tipo=elec,
            date=datetime.now(),
        )
        p8 = Producto(
            nombre="cloro",
            descripcion="",
            precio_de_compra=5.000,
            precio_de_venta=6.000,
            cant=20,
            tipo_id=4,
            tipo=lim,
            date=datetime.now(),
        )
        p9 = Producto(
            nombre="magistral",
            descripcion="",
            precio_de_compra=7.000,
            precio_de_venta=10.000,
            cant=24,
            tipo_id=4,
            tipo=lim,
            date=datetime.now(),
        )
        p10 = Producto(
            nombre="jabon",
            descripcion="jabon de mano ceco",
            precio_de_compra=1.000,
            precio_de_venta=2.300,
            cant=23,
            tipo_id=1,
            tipo=elec,
            date=datetime.now(),
        )
        session.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10])
        session.commit()
        session.close()
