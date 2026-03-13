from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.database.connection import Base


class ProvinciaORM(Base):
    __tablename__ = "provincias"

    id     = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)

    localidades = relationship("LocalidadORM", back_populates="provincia")


class LocalidadORM(Base):
    __tablename__ = "localidades"

    id     = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

    id_provincia = Column(Integer, ForeignKey("provincias.id"), nullable=False)

    provincia  = relationship("ProvinciaORM", back_populates="localidades")
    domicilios = relationship("DomicilioORM", back_populates="localidad")


class DomicilioORM(Base):
    __tablename__ = "domicilios"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    direccion      = Column(String(255), nullable=True)
    codigo_postal  = Column(String(20), nullable=True)

    id_localidad = Column(Integer, ForeignKey("localidades.id"), nullable=True)

    localidad = relationship("LocalidadORM", back_populates="domicilios")
    afiliado  = relationship("AfiliadoORM", back_populates="domicilio")