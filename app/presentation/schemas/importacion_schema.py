from pydantic import BaseModel, EmailStr
from datetime import date
from typing import List, Optional
# ── ImportRequest — entrada para importación ─────────────────────────

class AfiliadoImportItem(BaseModel):
    """Representa un afiliado dentro del body de importación"""
    apellido         : Optional[str] = None  # ← opcionales para permitir
    nombre           : Optional[str] = None  #   que lleguen datos sucios
    dni              : Optional[str] = None  #   y el dominio los valide
    numero_legajo    : Optional[str] = None
    fecha_nacimiento : Optional[date] = None

    email            : Optional[EmailStr]  = None  
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
    afiliados: List[AfiliadoImportItem]


class AfiliadoCreate(AfiliadoImportItem):
    """
    Entrada para alta manual de un afiliado — UC1a
    Hereda todos los campos de AfiliadoIportItem
    """
    pass


# ── ImportResponse — respuesta de importación ────────────────────────

class ErrorValidacionResponse(BaseModel):
    """Un error de validación de una fila de la importación (AF-RN12)."""
    campo             : str
    descripcion_error : str
    row_number        : int


class ImportResponse(BaseModel):
    """Resumen del proceso de importación — UC1 paso 6"""
    cantidad_registros_procesados : int
    cantidad_registros_validos    : int
    cantidad_errores              : int
    errores                       : list[ErrorValidacionResponse] = []


def import_response_from_importacion(importacion) -> ImportResponse:
    """Proyecta el modelo de dominio Importacion al schema de respuesta."""
    return ImportResponse(
        cantidad_registros_procesados=importacion.cantidad_registros,
        cantidad_registros_validos   =importacion.cantidad_validos,
        cantidad_errores             =importacion.cantidad_errores,
        errores=[
            ErrorValidacionResponse(
                campo            =error.campo,
                descripcion_error=error.descripcion_error,
                row_number       =error.row_number,
            )
            for error in importacion.errores
        ],
    )