"""Generamos el acceso a la bese de datos y declaramos la base y creamos"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = "mysql://root:1999.Denis@localhost:3306/ferreteria"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

Base = declarative_base()
from Models import *
Base.metadata.create_all(engine)
