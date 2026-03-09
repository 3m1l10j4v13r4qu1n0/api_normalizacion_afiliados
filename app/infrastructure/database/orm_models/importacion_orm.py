from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.connection import Base


class ImportacionORM(Base):
    __tablename__ = "importaciones"

    # Clave primaria
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Datos del proceso de importación
    fecha_importacion   = Column(DateTime, server_default=func.now(), nullable=False)
    cantidad_registros  = Column(Integer, nullable=False, default=0)
    cantidad_errores    = Column(Integer, nullable=False, default=0)
    estado              = Column(String(50), nullable=False, default="pendiente")

    # Relaciones inversas
    afiliados           = relationship("AfiliadoORM", back_populates="importacion")
    errores_validacion  = relationship("ErrorValidacionORM", back_populates="importacion")