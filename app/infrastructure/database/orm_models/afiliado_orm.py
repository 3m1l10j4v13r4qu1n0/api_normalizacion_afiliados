from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.connection import Base


class AfiliadoORM(Base):
    
    __tablename__ = "afiliados"

    # Clave primaria
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Datos personales
    apellido         = Column(String(100), nullable=False)
    nombre           = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    dni              = Column(String(20), unique=True, nullable=False)
    email            = Column(String(255), unique=True, nullable=True)
    telefono         = Column(String(50), nullable=True)
    numero_legajo    = Column(String(50), unique=True, nullable=False)
    fecha_ingreso    = Column(Date, nullable=True)
    fecha_alta       = Column(Date, nullable=True)
    titulo_obtenido  = Column(String(255), nullable=True)  # opcional

    # Marcas temporales — se gestionan automáticamente
    marca_temporal_creacion     = Column(DateTime, server_default=func.now(), nullable=False)
    marca_temporal_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Claves foráneas — relaciones con entidades de dominio
    id_genero               = Column(Integer, ForeignKey("generos.id"), nullable=True)
    id_estado_civil         = Column(Integer, ForeignKey("estados_civiles.id"), nullable=True)
    id_nivel_educativo      = Column(Integer, ForeignKey("niveles_educativos.id"), nullable=True)
    id_relacion_dependencia = Column(Integer, ForeignKey("relaciones_dependencia.id"), nullable=True)
    id_estado_afiliado      = Column(Integer, ForeignKey("estados_afiliado.id"), nullable=False)
    id_domicilio            = Column(Integer, ForeignKey("domicilios.id"), nullable=True)
    id_importacion          = Column(Integer, ForeignKey("importaciones.id"), nullable=True)

    # Relaciones ORM — permiten navegar entre entidades
    genero               = relationship("GeneroORM")
    estado_civil         = relationship("EstadoCivilORM")
    nivel_educativo      = relationship("NivelEducativoORM")
    relacion_dependencia = relationship("RelacionDependenciaORM")
    estado_afiliado      = relationship("EstadoAfiliadoORM")
    domicilio            = relationship("DomicilioORM", back_populates="afiliado")
    importacion          = relationship("ImportacionORM", back_populates="afiliados")


"""

## Qué hace cada parte

### Columnas con restricciones

dni           → unique=True   — no pueden existir dos iguales
email         → unique=True   — no pueden existir dos iguales
numero_legajo → unique=True   — no pueden existir dos iguales
apellido      → nullable=False — obligatorio
nombre        → nullable=False — obligatorio
titulo_obtenido → nullable=True — opcional según el modelo

"""