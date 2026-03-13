"""
UC2  — Consultar Afiliados
UC3  — Actualizar Afiliado
UC5  — Dar de baja Afiliado
RF10 — Permitir consultar afiliados
RF11 — Permitir consultar afiliado por identificador
RF12 — Permitir actualizar datos de afiliados
RF13 — Permitir dar de baja afiliados
RN16 — Baja lógica, marcando estado como inactivo
RN14 — Solo se sincronizan afiliados válidos
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.domain.exceptions import (
    AfiliadoNoEncontradoError,
    EmailDuplicadoError,
    DatoInvalidoError,
)
from app.domain.rules.validacion import validar_email
from app.domain.rules.normalizacion import normalizar_afiliado
from app.infrastructure.database.orm_models import AfiliadoORM


# ── UC2 — Consultar Afiliados ────────────────────────────────────────

async def listar_afiliados(db: AsyncSession) -> list[AfiliadoORM]:
    """
    UC2 — Obtiene todos los afiliados almacenados
    RF10 — Permitir consultar afiliados
    """
    resultado = await db.execute(select(AfiliadoORM))
    return resultado.scalars().all()


async def obtener_afiliado_por_id(
    db: AsyncSession,
    afiliado_id: int
) -> AfiliadoORM:
    """
    UC2 — Obtiene un afiliado por su ID
    RF11 — Permitir consultar afiliado por identificador
    """
    afiliado = await db.get(AfiliadoORM, afiliado_id)
    if not afiliado:
        raise AfiliadoNoEncontradoError(afiliado_id)
    return afiliado


# ── UC3 — Actualizar Afiliado ────────────────────────────────────────

async def actualizar_afiliado(
    db: AsyncSession,
    afiliado_id: int,
    datos: dict
) -> AfiliadoORM:
    """
    UC3 — Actualiza los datos de un afiliado existente
    RF12 — Permitir actualizar datos de afiliados
    """

    # Paso 1 — Verificar que existe
    afiliado = await db.get(AfiliadoORM, afiliado_id)
    if not afiliado:
        raise AfiliadoNoEncontradoError(afiliado_id)

    # Paso 2 — Normalizar datos entrantes
    datos_normalizados = normalizar_afiliado(datos)

    # Paso 3 — Validar email si viene en la actualización
    if datos_normalizados.get("email"):
        validar_email(datos_normalizados["email"])

        # Verificar que el email no esté en uso por otro afiliado
        resultado = await db.execute(
            select(AfiliadoORM).where(
                AfiliadoORM.email == datos_normalizados["email"],
                AfiliadoORM.id    != afiliado_id          # ← excluye al mismo afiliado
            )
        )
        existente = resultado.scalars().first()
        if existente:
            raise EmailDuplicadoError(datos_normalizados["email"])

    # Paso 4 — Aplicar solo los campos que llegaron
    campos_actualizables = [
        "apellido", "nombre", "email", "telefono",
        "fecha_nacimiento", "fecha_ingreso", "fecha_alta",
        "titulo_obtenido", "numero_legajo",
        "id_genero", "id_estado_civil", "id_nivel_educativo",
        "id_relacion_dependencia", "id_estado_afiliado",
    ]

    for campo in campos_actualizables:
        valor = datos_normalizados.get(campo)
        if valor is not None:                  # ← solo actualiza campos que llegaron
            setattr(afiliado, campo, valor)

    await db.flush()
    return afiliado


# ── UC5 — Dar de baja Afiliado ───────────────────────────────────────

async def dar_baja_afiliado(
    db: AsyncSession,
    afiliado_id: int
) -> AfiliadoORM:
    """
    UC5  — Baja lógica del afiliado
    RF13 — Permitir dar de baja afiliados
    RN16 — Baja lógica marcando estado como inactivo
    """

    # Paso 1 — Verificar que existe
    afiliado = await db.get(AfiliadoORM, afiliado_id)
    if not afiliado:
        raise AfiliadoNoEncontradoError(afiliado_id)

    # Paso 2 — Marcar como inactivo — id 2 = Inactivo (seed)
    afiliado.id_estado_afiliado = 2   # ← RN16 baja lógica

    await db.flush()
    return afiliado