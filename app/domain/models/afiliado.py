from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class Afiliado:
    # Datos personales obligatorios
    apellido: str
    nombre: str
    fecha_nacimiento: date
    dni: str
    numero_legajo: str

    # Datos opcionales
    email: str | None = None
    telefono: str | None = None
    fecha_ingreso: date | None = None
    fecha_alta: date | None = None
    titulo_obtenido: str | None = None

    # Relaciones — IDs de entidades de dominio
    id_genero: int | None = None
    id_estado_civil: int | None = None
    id_nivel_educativo: int | None = None
    id_relacion_dependencia: int | None = None
    id_estado_afiliado: int | None = None
    id_domicilio: int | None = None
    id_importacion: int | None = None

    # Marcas temporales — las maneja el sistema
    marca_temporal_creacion: datetime | None = None
    marca_temporal_actualizacion: datetime | None = None

    # Clave primaria — la asigna la BD
    id: int | None = field(default=None)
