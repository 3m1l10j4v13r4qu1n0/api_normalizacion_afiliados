from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.infrastructure.sheets.sheets_interface import ISheetsClient
from app.infrastructure.sheets.sheets_client import GspreadSheetsClient
from app.infrastructure.database.orm_models import AfiliadoORM
from app.domain.models.importacion import Importacion
from app.domain.exceptions import SincronizacionError
from app.application.services.importacion_service import importar_afiliados


async def importar_desde_sheets(
    db: AsyncSession,
    cliente: ISheetsClient = None          # ← recibe la interfaz, no la implementación
) -> Importacion:
    """UC4 — Importar desde Google Sheets"""

    if cliente is None:
        cliente = GspreadSheetsClient()    # ← implementación por defecto

    registros_crudos = cliente.get_all_records()

    if not registros_crudos:
        return Importacion(cantidad_registros=0)

    return await importar_afiliados(db=db, registros=registros_crudos)


async def exportar_a_sheets(
    db: AsyncSession,
    cliente: ISheetsClient = None          # ← recibe la interfaz
) -> dict:
    """UC6 — Exportar afiliados activos a Google Sheets"""

    if cliente is None:
        cliente = GspreadSheetsClient()

    resultado = await db.execute(
        select(AfiliadoORM).where(AfiliadoORM.id_estado_afiliado == 1)
    )
    afiliados = resultado.scalars().all()

    if not afiliados:
        return {
            "mensaje"              : "No hay afiliados activos para sincronizar",
            "cantidad_sincronizados": 0
        }

    encabezados = [
        "apellido", "nombre", "dni", "email", "telefono",
        "numero_legajo", "fecha_nacimiento", "fecha_ingreso",
        "fecha_alta", "titulo_obtenido", "id_genero",
        "id_estado_civil", "id_nivel_educativo",
        "id_relacion_dependencia", "id_estado_afiliado"
    ]

    filas         = [encabezados]
    sincronizados = 0
    errores       = 0

    for afiliado in afiliados:
        try:
            fila = [
                afiliado.apellido                                          or "",
                afiliado.nombre                                            or "",
                afiliado.dni                                               or "",
                afiliado.email                                             or "",
                afiliado.telefono                                          or "",
                afiliado.numero_legajo                                     or "",
                str(afiliado.fecha_nacimiento)                             or "",
                str(afiliado.fecha_ingreso)  if afiliado.fecha_ingreso    else "",
                str(afiliado.fecha_alta)     if afiliado.fecha_alta       else "",
                afiliado.titulo_obtenido                                   or "",
                afiliado.id_genero                                         or "",
                afiliado.id_estado_civil                                   or "",
                afiliado.id_nivel_educativo                                or "",
                afiliado.id_relacion_dependencia                           or "",
                afiliado.id_estado_afiliado                                or "",
            ]
            filas.append(fila)
            sincronizados += 1
        except Exception:
            errores += 1
            continue

    # Limpiar y escribir
    cliente.clear_range("A1")
    cliente.write_range("A1", filas)

    return {
        "mensaje"              : "Sincronización completada",
        "cantidad_sincronizados": sincronizados,
        "cantidad_errores"     : errores
    }