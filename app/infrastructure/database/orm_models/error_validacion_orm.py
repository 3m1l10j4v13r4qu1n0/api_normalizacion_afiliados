from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.connection import Base


class ErrorValidacionORM(Base):
    
    __tablename__ = "errores_validacion"

    # Clave primaria
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Datos del error
    registro_origen  = Column(String(500), nullable=False)  # ← fila original que falló
    campo            = Column(String(100), nullable=False)   # ← qué campo tiene el error
    descripcion_error = Column(String(500), nullable=False)  # ← por qué falló
    fecha_error      = Column(DateTime, server_default=func.now(), nullable=False)

    # Clave foránea — a qué importación pertenece este error
    id_importacion = Column(Integer, ForeignKey("importaciones.id"), nullable=False)

    # Relación ORM
    importacion = relationship("ImportacionORM", back_populates="errores_validacion")