from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional


@dataclass
class Afiliado:
    # Datos personales obligatorios
    apellido         : str
    nombre           : str
    fecha_nacimiento : date
    dni              : str
    numero_legajo    : str

    # Datos opcionales
    email            : Optional[str] = None
    telefono         : Optional[str] = None
    fecha_ingreso    : Optional[date] = None
    fecha_alta       : Optional[date] = None
    titulo_obtenido  : Optional[str] = None

    # Relaciones — IDs de entidades de dominio
    id_genero               : Optional[int] = None
    id_estado_civil         : Optional[int] = None
    id_nivel_educativo      : Optional[int] = None
    id_relacion_dependencia : Optional[int] = None
    id_estado_afiliado      : Optional[int] = None
    id_domicilio            : Optional[int] = None
    id_importacion          : Optional[int] = None

    # Marcas temporales — las maneja el sistema
    marca_temporal_creacion      : Optional[datetime] = None
    marca_temporal_actualizacion : Optional[datetime] = None

    # Clave primaria — la asigna la BD
    id : Optional[int] = field(default=None)