from datetime import date

from pydantic import BaseModel, EmailStr, field_validator

# ── Schema base — campos comunes ─────────────────────────────────────


class AfiliadoBase(BaseModel):
    apellido: str
    nombre: str
    dni: str
    numero_legajo: str
    fecha_nacimiento: date

    # Opcionales
    email: EmailStr | None = None  # ← EmailStr valida formato
    telefono: str | None = None
    fecha_ingreso: date | None = None
    fecha_alta: date | None = None
    titulo_obtenido: str | None = None

    # Relaciones — valores controlados
    id_genero: int | None = None
    id_estado_civil: int | None = None
    id_nivel_educativo: int | None = None
    id_relacion_dependencia: int | None = None
    id_estado_afiliado: int | None = None


# ── AfiliadoUpdate — entrada para actualización ──────────────────────


class AfiliadoUpdate(BaseModel):
    """
    Todos los campos opcionales — UC3
    Solo se actualizan los campos que lleguen
    """

    apellido: str | None = None
    nombre: str | None = None
    dni: str | None = None
    numero_legajo: str | None = None
    fecha_nacimiento: date | None = None
    email: EmailStr | None = None  # ← EmailStr valida formato
    telefono: str | None = None
    fecha_ingreso: date | None = None
    fecha_alta: date | None = None
    titulo_obtenido: str | None = None

    id_genero: int | None = None
    id_estado_civil: int | None = None
    id_nivel_educativo: int | None = None
    id_relacion_dependencia: int | None = None
    id_estado_afiliado: int | None = None

    @field_validator("nombre", "apellido")
    @classmethod
    def no_vacio(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("El campo no puede estar vacío")
        return v


# ── AfiliadoResponse — salida hacia el cliente ───────────────────────


class AfiliadoResponse(BaseModel):
    """
    Datos que recibe el cliente
    Filtra campos internos — nunca expone datos sensibles
    """

    id: int
    apellido: str
    nombre: str
    dni: str
    numero_legajo: str
    fecha_nacimiento: date
    email: str | None = None
    telefono: str | None = None
    fecha_ingreso: date | None = None
    fecha_alta: date | None = None
    titulo_obtenido: str | None = None

    id_genero: int | None = None
    id_estado_civil: int | None = None
    id_nivel_educativo: int | None = None
    id_relacion_dependencia: int | None = None
    id_estado_afiliado: int | None = None

    class Config:
        from_attributes = True  # ← convierte AfiliadoORM a este schema
