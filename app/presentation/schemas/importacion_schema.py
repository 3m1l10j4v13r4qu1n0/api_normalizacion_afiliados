from pydantic import BaseModel, EmailStr, field_validator
from datetime import date
from typing import Optional

# ── ImportRequest — entrada para importación ─────────────────────────

class AfiliadoImportItem(BaseModel):
    """Representa un afiliado dentro del body de importación"""
    apellido         : Optional[str] = None  # ← opcionales para permitir
    nombre           : Optional[str] = None  #   que lleguen datos sucios
    dni              : Optional[str] = None  #   y el dominio los valide
    numero_legajo    : Optional[str] = None
    fecha_nacimiento : Optional[date] = None

    email            : Optional[str]  = None  # ← str, no EmailStr
    telefono         : Optional[str]  = None  #   el dominio valida el formato
    fecha_ingreso    : Optional[date] = None
    fecha_alta       : Optional[date] = None
    titulo_obtenido  : Optional[str]  = None

    id_genero               : Optional[int] = None
    id_estado_civil         : Optional[int] = None
    id_nivel_educativo      : Optional[int] = None
    id_relacion_dependencia : Optional[int] = None
    id_estado_afiliado      : Optional[int] = None


class ImportRequest(BaseModel):
    """Body del POST /afiliados/import"""
    afiliados: list[AfiliadoImportItem]


# ── ImportResponse — respuesta de importación ────────────────────────

class ImportResponse(BaseModel):
    """Resumen del proceso de importación — UC1 paso 6"""
    cantidad_registros_procesados : int
    cantidad_registros_validos    : int
    cantidad_errores              : int