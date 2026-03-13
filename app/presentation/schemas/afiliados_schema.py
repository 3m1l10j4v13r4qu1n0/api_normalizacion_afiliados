from pydantic import BaseModel, EmailStr, field_validator
from datetime import date
from typing import Optional


# ── Schema base — campos comunes ─────────────────────────────────────

class AfiliadoBase(BaseModel):
    apellido         : str
    nombre           : str
    dni              : str
    numero_legajo    : str
    fecha_nacimiento : date

    # Opcionales
    email            : Optional[EmailStr] = None  # ← EmailStr valida formato
    telefono         : Optional[str]      = None
    fecha_ingreso    : Optional[date]     = None
    fecha_alta       : Optional[date]     = None
    titulo_obtenido  : Optional[str]      = None

    # Relaciones — valores controlados
    id_genero               : Optional[int] = None
    id_estado_civil         : Optional[int] = None
    id_nivel_educativo      : Optional[int] = None
    id_relacion_dependencia : Optional[int] = None
    id_estado_afiliado      : Optional[int] = None


# ── AfiliadoUpdate — entrada para actualización ──────────────────────

class AfiliadoUpdate(BaseModel):
    """
    Todos los campos opcionales — UC3
    Solo se actualizan los campos que lleguen
    """
    apellido         : Optional[str]      = None
    nombre           : Optional[str]      = None
    dni              : Optional[str]      = None
    numero_legajo    : Optional[str]      = None
    fecha_nacimiento : Optional[date]     = None
    email            : Optional[EmailStr] = None  # ← EmailStr valida formato
    telefono         : Optional[str]      = None
    fecha_ingreso    : Optional[date]     = None
    fecha_alta       : Optional[date]     = None
    titulo_obtenido  : Optional[str]      = None

    id_genero               : Optional[int] = None
    id_estado_civil         : Optional[int] = None
    id_nivel_educativo      : Optional[int] = None
    id_relacion_dependencia : Optional[int] = None
    id_estado_afiliado      : Optional[int] = None

    @field_validator("nombre", "apellido")
    @classmethod
    def no_vacio(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("El campo no puede estar vacío")
        return v


# ── AfiliadoResponse — salida hacia el cliente ───────────────────────

class AfiliadoResponse(BaseModel):
    """
    Datos que recibe el cliente
    Filtra campos internos — nunca expone datos sensibles
    """
    id               : int
    apellido         : str
    nombre           : str
    dni              : str
    numero_legajo    : str
    fecha_nacimiento : date
    email            : Optional[str] = None
    telefono         : Optional[str] = None
    fecha_ingreso    : Optional[date] = None
    fecha_alta       : Optional[date] = None
    titulo_obtenido  : Optional[str] = None

    id_genero               : Optional[int] = None
    id_estado_civil         : Optional[int] = None
    id_nivel_educativo      : Optional[int] = None
    id_relacion_dependencia : Optional[int] = None
    id_estado_afiliado      : Optional[int] = None

    class Config:
        from_attributes = True  # ← convierte AfiliadoORM a este schema