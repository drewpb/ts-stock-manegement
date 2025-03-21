from sqlalchemy import create_engine, __version__
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

""" EN EL TERMINAL, EJECUTAR:
    sqlite3 database/tareas.db
    .help  # Para ver todas las cosas que se pueden hacer
"""

# Creamos motor DB y su ubicación
engine = create_engine("sqlite:///database/productos.db",
                       # Argumentos extras a revisar con la conexion de BBDD:
                       connect_args={"check_same_thread": False})  # 'thread:hilo'

# Creamos la sesión para realizar transacciones
Session = sessionmaker(bind=engine)
session = Session()

# Creamos la clase Base para que mapee la info de las clases en las que hereda y vincular su info a tablas de la BBDD
Base = declarative_base()
