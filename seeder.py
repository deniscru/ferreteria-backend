from sqlalchemy.orm import Session
from bbdd import engine
from Models.Tipo import Tipo
from Models.Producto import Producto


def seed():
    with Session(engine) as session:
        elec = Tipo(nombre="Electricidad")
        plo = Tipo(nombre="Plomeria")
        ferre = Tipo(nombre="Ferreteria")
        lim = Tipo(nombre="Limpieza")

        session.add_all([elec, plo, ferre, lim])
        session.commit()
        session.close()

    """db.execute(
        "INSERT INTO `tipos` VALUES (1,'Electricidad', 1),(2,'Plomeria', 1),(3,'Ferreteria', 1),(4,'Limpieza', 1);"
    )"""


def productos():
    with Session(engine) as session:
        ferre = session.query(Tipo).get(3)
        elec = session.query(Tipo).get(1)
        plom = session.query(Tipo).get(2)
        lim = session.query(Tipo).get(4)

        p1 = Producto(
            nombre="Martillo",
            nombre_alias="Martillo pico loro",
            descripcion="Martillo para carpinteria",
            medida=None,
            precio_de_compra=12.000,
            precio_de_venta=15.000,
            cant=3,
            imagen="avsevsdvsdfvsdfv",
            tipo_id=3,
            tipo=ferre,
        )
        p2 = Producto(
            nombre="metro",
            nombre_alias="metro amarillo",
            descripcion="metro para medir",
            medida=5,
            precio_de_compra=8.000,
            precio_de_venta=12.000,
            cant=4,
            imagen="sdvedgvcsdcsdcsd",
            tipo_id=3,
            tipo=ferre,
        )
        p3 = Producto(
            nombre="destornillador filip",
            nombre_alias="destornillador plano",
            descripcion="destornillador de punta plana",
            medida=None,
            precio_de_compra=1.000,
            precio_de_venta=2.000,
            cant=6,
            imagen="avsvsdfvsfdv",
            tipo_id=3,
            tipo=ferre,
        )
        p4 = Producto(
            nombre="Codo 90 grados",
            nombre_alias="codo de pvc",
            descripcion="codo de plomeria con angulo de 90 grados",
            medida=None,
            precio_de_compra=1.500,
            precio_de_venta=2.200,
            cant=10,
            imagen="csfsvsf",
            tipo_id=2,
            tipo=plom,
        )
        p5 = Producto(
            nombre="teflon",
            nombre_alias="teplon para rosca",
            descripcion="",
            medida=5,
            precio_de_compra=1.000,
            precio_de_venta=2.100,
            cant=20,
            imagen="sadfcacsdfcfsd",
            tipo_id=2,
            tipo=plom,
        )
        p6 = Producto(
            nombre="caño de luz",
            nombre_alias="caño de luz electrica reforsada",
            descripcion="",
            medida=1.5,
            precio_de_compra=23.750,
            precio_de_venta=25.000,
            cant=20,
            imagen="vsadvcsadcasd",
            tipo_id=1,
            tipo=elec,
        )
        p7 = Producto(
            nombre="toma hembra",
            nombre_alias="toma hembra sin cable",
            descripcion="toma para alargue",
            medida=None,
            precio_de_compra=400,
            precio_de_venta=800,
            cant=23,
            imagen="sadsadcsa",
            tipo_id=1,
            tipo=elec,
        )
        p8 = Producto(
            nombre="cloro",
            nombre_alias="",
            descripcion="",
            medida=None,
            precio_de_compra=5.000,
            precio_de_venta=6.000,
            cant=20,
            imagen="fasdcsadc",
            tipo_id=4,
            tipo=lim,
        )
        p9 = Producto(
            nombre="magistral",
            nombre_alias="",
            descripcion="",
            medida=None,
            precio_de_compra=7.000,
            precio_de_venta=10.000,
            cant=24,
            imagen="ffasdf",
            tipo_id=4,
            tipo=lim,
        )
        p10 = Producto(
            nombre="jabon",
            nombre_alias="jabon de mano",
            descripcion="jabon de mano ceco",
            medida=None,
            precio_de_compra=1.000,
            precio_de_venta=2.300,
            cant=23,
            imagen="csdacasdcas",
            tipo_id=1,
            tipo=elec,
        )
        session.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10])
        session.commit()
        session.close()
