"""
UC1 — Importar Afiliados
RF1  — Importar datos desde fuente externa
RF2  — Procesar múltiples registros
RF3  — Validar datos obligatorios
RF4  — Validar formato de datos
RF5  — Detectar duplicados por DNI
RF6  — Registrar errores de validación
RF7  — Normalizar nombres
RF8  — Normalizar formatos de texto
RF9  — Almacenar datos normalizados
RN11 — Registros inválidos no se persisten
RN12 — Errores se registran
RN13 — Importación continúa aunque haya errores
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.domain.models.importacion import Importacion
from app.domain.models.error_validacion import ErrorValidacion
from app.domain.rules.validacion import validar_afiliado, validar_dni_duplicado
from app.domain.rules.normalizacion import normalizar_afiliado
from app.domain.exceptions import ImportacionError

from app.infrastructure.database.orm_models import (
    AfiliadoORM,
    ImportacionORM,
    ErrorValidacionORM,
)


async def importar_afiliados(
    db: AsyncSession,
    registros: list[dict]
) -> Importacion:
    """
    UC1 — Flujo principal completo
    Recibe lista de dicts, valida, normaliza y almacena.
    Retorna resumen del proceso.
    """

    # Paso 1 — Crear registro de importación
    importacion_orm = ImportacionORM(
        cantidad_registros = len(registros),
        cantidad_errores   = 0,
        estado             = "pendiente"
    )
    db.add(importacion_orm)
    await db.flush()  # ← obtiene el id sin hacer commit

    # Modelo de dominio para coordinar el proceso
    importacion = Importacion(
        cantidad_registros = len(registros),
        id                 = importacion_orm.id
    )

    # Paso 2 — Obtener DNIs existentes en la BD para detectar duplicados
    # RF5 — Detectar registros duplicados
    resultado = await db.execute(select(AfiliadoORM.dni))
    dnis_existentes = set(resultado.scalars().all())

    # DNIs procesados en esta importación — detecta duplicados dentro del mismo lote
    dnis_en_lote: set[str] = set()

    # Paso 3 — Procesar cada registro
    for registro in registros:

        # UC1 Paso 4 — Normalizar primero
        dato_normalizado = normalizar_afiliado(registro)

        # UC1 Paso 3 — Validar campos obligatorios y formato
        errores = validar_afiliado(dato_normalizado)

        # Validar DNI duplicado en BD — flujo alternativo 3b
        dni = dato_normalizado.get("dni")
        if dni and not errores:
            try:
                validar_dni_duplicado(dni, dnis_existentes | dnis_en_lote)
            except Exception as e:
                errores.append(("dni", str(e)))

        if errores:
            # RN11 — no se persiste
            # RN12 — se registra el error
            for campo, descripcion in errores:
                error_orm = ErrorValidacionORM(
                    registro_origen   = str(registro),
                    campo             = campo,
                    descripcion_error = descripcion,
                    id_importacion    = importacion_orm.id
                )
                db.add(error_orm)
                importacion.registrar_error(campo, descripcion, str(registro))

        else:
            # UC1 Paso 5 — Almacenar registro válido
            afiliado_orm = AfiliadoORM(
                apellido                = dato_normalizado.get("apellido"),
                nombre                  = dato_normalizado.get("nombre"),
                dni                     = dato_normalizado.get("dni"),
                email                   = dato_normalizado.get("email"),
                telefono                = dato_normalizado.get("telefono"),
                numero_legajo           = dato_normalizado.get("numero_legajo"),
                fecha_nacimiento        = dato_normalizado.get("fecha_nacimiento"),
                fecha_ingreso           = dato_normalizado.get("fecha_ingreso"),
                fecha_alta              = dato_normalizado.get("fecha_alta"),
                titulo_obtenido         = dato_normalizado.get("titulo_obtenido"),
                id_genero               = dato_normalizado.get("id_genero"),
                id_estado_civil         = dato_normalizado.get("id_estado_civil"),
                id_nivel_educativo      = dato_normalizado.get("id_nivel_educativo"),
                id_relacion_dependencia = dato_normalizado.get("id_relacion_dependencia"),
                id_estado_afiliado      = dato_normalizado.get("id_estado_afiliado", 1),
                id_importacion          = importacion_orm.id
            )
            db.add(afiliado_orm)
            dnis_en_lote.add(dni)  # ← registra en el lote actual

    # Paso 4 — Actualizar importación con resultados finales
    importacion_orm.cantidad_errores = importacion.cantidad_errores
    importacion_orm.estado           = "completada"
    importacion.completar()

    await db.flush()

    return importacion