from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.infrastructure.database.connection import Base


class GeneroORM(Base):
    
    __tablename__ = "generos"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(50), nullable=False, unique=True)

    # Relación inversa — un género puede tener muchos afiliados
    afiliados = relationship("AfiliadoORM", back_populates="genero")


class EstadoCivilORM(Base):
    
    __tablename__ = "estados_civiles"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(50), nullable=False, unique=True)

    afiliados = relationship("AfiliadoORM", back_populates="estado_civil")


class NivelEducativoORM(Base):
    
    __tablename__ = "niveles_educativos"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(100), nullable=False, unique=True)

    afiliados = relationship("AfiliadoORM", back_populates="nivel_educativo")


class RelacionDependenciaORM(Base):
    
    __tablename__ = "relaciones_dependencia"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(100), nullable=False, unique=True)

    afiliados = relationship("AfiliadoORM", back_populates="relacion_dependencia")


class EstadoAfiliadoORM(Base):
    
    __tablename__ = "estados_afiliado"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(50), nullable=False, unique=True)

    afiliados = relationship("AfiliadoORM", back_populates="estado_afiliado")

"""

## Qué hace cada parte

### Son tablas de valores controlados
Guardan valores fijos que no cambian frecuentemente:

generos
  ├── 1 → Masculino
  ├── 2 → Femenino
  └── 3 → No binario

estados_civiles
  ├── 1 → Soltero
  ├── 2 → Casado
  ├── 3 → Divorciado
  └── 4 → Viudo

niveles_educativos
  ├── 1 → Primario
  ├── 2 → Secundario
  ├── 3 → Terciario
  └── 4 → Universitario

relaciones_dependencia
  ├── 1 → Planta Permanente
  ├── 2 → Plata Transitoria
  └── 3 → Monotributista

estados_afiliado
  ├── 1 → Activo
  └── 2 → Inactivo

"""