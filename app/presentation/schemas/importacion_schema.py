from datetime import date

from pydantic import BaseModel, EmailStr

# ── ImportRequest — entrada para importación ─────────────────────────


class AfiliadoImportItem(BaseModel):
    """Representa un afiliado dentro del body de importación"""

    apellido: str | None = None  # ← opcionales para permitir
    nombre: str | None = None  #   que lleguen datos sucios
    dni: str | None = None  #   y el dominio los valide
    numero_legajo: str | None = None
    fecha_nacimiento: date | None = None

    email: EmailStr | None = None
    telefono: str | None = None  #   el dominio valida el formato
    fecha_ingreso: date | None = None
    fecha_alta: date | None = None
    titulo_obtenido: str | None = None

    id_genero: int | None = None
    id_estado_civil: int | None = None
    id_nivel_educativo: int | None = None
    id_relacion_dependencia: int | None = None
    id_estado_afiliado: int | None = None


class ImportRequest(BaseModel):
    """Body del POST /afiliados/import"""

    afiliados: list[AfiliadoImportItem]


class AfiliadoCreate(AfiliadoImportItem):
    """
    Entrada para alta manual de un afiliado — UC1a
    Hereda todos los campos de AfiliadoIportItem
    """


# ── ImportResponse — respuesta de importación ────────────────────────


class ErrorValidacionResponse(BaseModel):
    """Un error de validación de una fila de la importación (AF-RN12)."""

    campo: str
    descripcion_error: str
    row_number: int


class ImportResponse(BaseModel):
    """Resumen del proceso de importación — UC1 paso 6"""

    cantidad_registros_procesados: int
    cantidad_registros_validos: int
    cantidad_errores: int
    errores: list[ErrorValidacionResponse] = []


def import_response_from_importacion(importacion) -> ImportResponse:
    """Proyecta el modelo de dominio Importacion al schema de respuesta."""
    return ImportResponse(
        cantidad_registros_procesados=importacion.cantidad_registros,
        cantidad_registros_validos=importacion.cantidad_validos,
        cantidad_errores=importacion.cantidad_errores,
        errores=[
            ErrorValidacionResponse(
                campo=error.campo,
                descripcion_error=error.descripcion_error,
                row_number=error.row_number,
            )
            for error in importacion.errores
        ],
    )


# ── ExportResponse — respuesta de exportación (HU-08) ──────────────


class ExportResponse(BaseModel):
    """Resumen del proceso de exportación — UC8"""

    cantidad_registros_procesados: int
    mensaje: str
