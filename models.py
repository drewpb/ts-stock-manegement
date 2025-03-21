from sqlalchemy import Column, Integer, String, Float
import db

class Producto(db.Base):  # Con Base, mapeamos nuestra clase con la base de datos
    ### Escribimos aquí la configuracion del ORM:
    __tablename__ = "producto"  # Minúscula y singular
    # Para garantizar que el valor de la clave primaria, sea unico y nunca se reutilice por cada tabla:
    __table_args__ = {"sqlite_autoincrement": True}
    # Y aquí configurar las columnas:
    id = Column(Integer, primary_key=True)  # Automáticamente se convierte en autoincremental
    nombre = Column(String(200), nullable=False, default="Desconocido")
    categoria = Column(String(60), nullable=False)  # No puede haber nulos
    precio = Column(Float, default=False)  # Si no pongo edad, escribe un -1
    stock = Column(Integer, nullable=False, default="-1")

    ### ---------------------------------------------------------------------------

    def __init__(self, nombre, categoria, precio, stock):
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock

    def __str__(self):
        return f"Producto {self.id} | {self.categoria}: {self.stock}u de {self.nombre} a {self.precio}€/u |"
