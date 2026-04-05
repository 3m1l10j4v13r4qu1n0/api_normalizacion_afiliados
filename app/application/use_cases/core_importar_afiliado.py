"""
Core — Importar Afiliados caso de uso principal (core)
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

from app.domain.models.importacion import Importacion
from app.domain.models.input_row import InputRow
from app.domain.ports.afiliado.afiliado_importacion_port import AfiliadoImportacionPort
from app.domain.ports.importacion_repository_port import ImportacionRepositoryPort
from app.domain.ports.error_repository_port import ErrorRepositoryPort
from app.domain.ports.domicilio_repository_port import DomicilioRepositoryPort
from app.domain.ports.dominio_repository_port import DominioRepositoryPort
from app.domain.services.validacion import validar_afiliado, validar_dni_duplicado
from app.domain.services.normalizacion import normalizar_afiliado
from app.infrastructure.database.orm_models.dominios_orm import (
    GeneroORM,
    EstadoCivilORM,
    NivelEducativoORM,
    RelacionDependenciaORM,
    EstadoAfiliadoORM,
)


class ImportarAfiliadoUseCase:
    """
    Core — Orquesta el pipeline completo de importación.

    Pipeline por fila:
        InputRow.values
            → resolver dominios        (DominioRepositoryPort)
            → resolver domicilio       (DomicilioRepositoryPort)
            → normalizar_afiliado()    (RN7, RN8, RN9, RN10)
            → validar_afiliado()       (RF3, RF4)
            → validar_dni_duplicado()  (RN1, RN2, RF5)
            → save()        si válido  (AfiliadoRepositoryPort)
            → registrar_error() si no  (ErrorRepositoryPort)

    Attributes:
        _afiliado_repo    : AfiliadoRepositoryPort
        _importacion_repo : ImportacionRepositoryPort
        _error_repo       : ErrorRepositoryPort
        _domicilio_repo   : DomicilioRepositoryPort
        _dominio_repo     : DominioRepositoryPort
    """

    def __init__(
        self,
        afiliado_repo   : AfiliadoImportacionPort,
        importacion_repo: ImportacionRepositoryPort,
        error_repo      : ErrorRepositoryPort,
        domicilio_repo  : DomicilioRepositoryPort,
        dominio_repo    : DominioRepositoryPort,
    ) -> None:
        self._afiliado_repo    = afiliado_repo
        self._importacion_repo = importacion_repo
        self._error_repo       = error_repo
        self._domicilio_repo   = domicilio_repo
        self._dominio_repo     = dominio_repo

    async def execute(self, rows: list[InputRow]) -> Importacion:
        """
        Ejecuta el pipeline completo de importación.

        Parameters:
            rows : List[InputRow] — Salida de ImportSheetUseCase.execute().

        Returns:
            Importacion — Resumen del proceso (totales, errores).
        """

        # Paso 1 — Crear registro de importación en BD
        id_importacion = await self._importacion_repo.crear_importacion(
            cantidad_registros=len(rows)
        )
        importacion = Importacion(
            id                =id_importacion,
            cantidad_registros=len(rows),
        )

        # Paso 2 — Obtener DNIs existentes para detectar duplicados (RF5)
        dnis_existentes = await self._afiliado_repo.get_all_dnis()
        dnis_en_lote: set[str] = set()

        # Paso 3 — Procesar cada fila
        for row in rows:
            valores = row.values

            # Paso 3a — Resolver dominios (strings → IDs)
            id_genero               = await self._dominio_repo.resolver_o_crear(GeneroORM,               valores.get("genero"))
            id_estado_civil         = await self._dominio_repo.resolver_o_crear(EstadoCivilORM,          valores.get("estado_civil"))
            id_nivel_educativo      = await self._dominio_repo.resolver_o_crear(NivelEducativoORM,       valores.get("nivel_educativo"))
            id_relacion_dependencia = await self._dominio_repo.resolver_o_crear(RelacionDependenciaORM,  valores.get("relacion_dependencia"))
            id_estado_afiliado      = await self._dominio_repo.resolver_o_crear(EstadoAfiliadoORM,       valores.get("estado_afiliado")) or 1

            # Paso 3b — Resolver domicilio
            id_domicilio = await self._domicilio_repo.resolver_o_crear(
                direccion    =valores.get("direccion"),
                localidad    =valores.get("localidad"),
                provincia    =valores.get("provincia"),
                codigo_postal=valores.get("codigo_postal"),
            )

            # Paso 3c — Normalizar con IDs ya resueltos
            dato_normalizado = normalizar_afiliado({
                **valores,
                "id_genero"              : id_genero,
                "id_estado_civil"        : id_estado_civil,
                "id_nivel_educativo"     : id_nivel_educativo,
                "id_relacion_dependencia": id_relacion_dependencia,
                "id_estado_afiliado"     : id_estado_afiliado,
                "id_domicilio"           : id_domicilio,
            })

            # Paso 3d — Validar campos obligatorios y formato (RF3, RF4)
            errores = validar_afiliado(dato_normalizado)

            # Paso 3e — Validar duplicados solo si pasó validaciones previas
            dni = dato_normalizado.get("dni")
            if dni and not errores:
                try:
                    validar_dni_duplicado(dni, dnis_existentes | dnis_en_lote)
                except Exception as e:
                    errores.append(("dni", str(e)))

            if errores:
                # RN11 — no se persiste
                # RN12 — se registra cada error
                
                for campo, descripcion in errores:
                    await self._error_repo.registrar_error(
                        id_importacion    = id_importacion,
                        registro_origen  =str(valores),
                        campo            =campo,
                        descripcion_error=descripcion,
                        row_number        = row.row_number
                    )
                importacion.registrar_error(
                    campo      =errores[0][0],
                    descripcion=errores[0][1],
                    origen     =str(valores),
                )
                # RN13 — continúa con la siguiente fila

            else:
                # RF9 — persistir afiliado válido
                await self._afiliado_repo.save(
                    datos         = dato_normalizado,
                    id_importacion = id_importacion,
                )
                dnis_en_lote.add(dni)

        # Paso 4 — Cerrar importación con resultado final
        await self._importacion_repo.completar_importacion(
            id_importacion  = id_importacion,
            cantidad_errores = importacion.cantidad_errores,
            
        )
        importacion.completar()

        return importacion