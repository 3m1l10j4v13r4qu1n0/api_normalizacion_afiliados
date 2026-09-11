"""
Core — Importar Afiliados caso de uso principal (orquestador único)
RF1  — Importar datos desde fuente externa
RF2  — Procesar múltiples registros
RF3  — Validar datos obligatorios
RF4  — Validar formato de datos
RF5  — Detectar duplicados por DNI
RF6  — Registrar errores de validación
RF7  — Normalizar nombres
RF8  — Normalizar formatos de texto
RF9  — Almacenar datos normalizados
AF-RN11 — Registros inválidos no se persisten
AF-RN12 — Errores se registran con referencia a la fila o índice
AF-RN13 — Importación continúa aunque haya errores
"""

from app.domain.models.dominio import Dominio
from app.domain.models.importacion import Importacion
from app.domain.models.input_row import InputRow
from app.domain.ports.afiliado.afiliado_importacion_port import AfiliadoImportacionPort
from app.domain.ports.domicilio_repository_port import DomicilioRepositoryPort
from app.domain.ports.dominio_repository_port import DominioRepositoryPort
from app.domain.ports.error_repository_port import ErrorRepositoryPort
from app.domain.ports.importacion_repository_port import ImportacionRepositoryPort
from app.domain.services.importacion_pipeline import procesar_fila


class ImportarAfiliadoUseCase:
    """
    Core — Orquesta el pipeline completo de importación (UC único).

    Es el caso de uso único para importar afiliados desde cualquier fuente
    (archivo/API, alta manual o Google Sheets). Se apoya en el servicio de
    dominio puro `procesar_fila` para la lógica por fila y delega la
    persistencia en los repositorios (ports).

    Pipeline por fila:
        InputRow.values
            → resolver dominios        (DominioRepositoryPort)
            → resolver domicilio       (DomicilioRepositoryPort)
            → procesar_fila()          (importacion_pipeline: normalizar + validar + dup)
            → save()         si válido (AfiliadoRepositoryPort)
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
        afiliado_repo: AfiliadoImportacionPort,
        importacion_repo: ImportacionRepositoryPort,
        error_repo: ErrorRepositoryPort,
        domicilio_repo: DomicilioRepositoryPort,
        dominio_repo: DominioRepositoryPort,
    ) -> None:
        self._afiliado_repo = afiliado_repo
        self._importacion_repo = importacion_repo
        self._error_repo = error_repo
        self._domicilio_repo = domicilio_repo
        self._dominio_repo = dominio_repo

    async def importar_desde_dicts(self, datos: list[dict]) -> Importacion:
        """
        Importa una lista de registros crudos (UC1a — importación por archivo/API).

        Convertimos cada dict a un InputRow manteniendo el índice real
        (row_number = i + 1) y delegamos en el pipeline.
        """
        rows = [InputRow(row_number=i + 1, values=dato) for i, dato in enumerate(datos)]
        return await self.execute(rows)

    async def agregar_afiliado(self, datos: dict) -> Importacion:
        """
        Alta manual de un único afiliado (UC1b), reutilizando el pipeline completo.

        El registro se envuelve en un InputRow con row_number = 1.
        """
        row = InputRow(row_number=1, values=datos)
        return await self.execute([row])

    async def execute(self, rows: list[InputRow]) -> Importacion:
        """
        Ejecuta el pipeline completo de importación (UC4 — source ya listo del sheet).

        Parameters:
            rows : List[InputRow] — Filas del sheet (SheetLectura.input_rows, UC4a).

        Returns:
            Importacion — Resumen del proceso (totales, errores).
        """

        # Paso 1 — Crear registro de importación en BD
        id_importacion = await self._importacion_repo.crear_importacion(
            cantidad_registros=len(rows)
        )
        importacion = Importacion(
            id=id_importacion,
            cantidad_registros=len(rows),
        )

        # Paso 2 — Obtener DNIs existentes para detectar duplicados (RF5)
        dnis_existentes = await self._afiliado_repo.get_all_dnis()
        dnis_en_lote: set[str] = set()

        # Paso 3 — Procesar cada fila
        for row in rows:
            valores = row.values

            # Paso 3a — Resolver dominios (strings → IDs)
            ids_dominio = {
                "id_genero": await self._dominio_repo.resolver_o_crear(
                    Dominio.GENERO, valores.get("genero")
                ),
                "id_estado_civil": await self._dominio_repo.resolver_o_crear(
                    Dominio.ESTADO_CIVIL, valores.get("estado_civil")
                ),
                "id_nivel_educativo": await self._dominio_repo.resolver_o_crear(
                    Dominio.NIVEL_EDUCATIVO, valores.get("nivel_educativo")
                ),
                "id_relacion_dependencia": await self._dominio_repo.resolver_o_crear(
                    Dominio.RELACION_DEPENDENCIA, valores.get("relacion_dependencia")
                ),
                "id_estado_afiliado": await self._dominio_repo.resolver_o_crear(
                    Dominio.ESTADO_AFILIADO, valores.get("estado_afiliado")
                )
                or 1,
            }

            # Paso 3b — Resolver domicilio
            id_domicilio = await self._domicilio_repo.resolver_o_crear(
                direccion=valores.get("direccion"),
                localidad=valores.get("localidad"),
                provincia=valores.get("provincia"),
                codigo_postal=valores.get("codigo_postal"),
            )

            # Paso 3c — Lógica de dominio pura por fila (normalizar + validar + dup)
            dato_normalizado, errores = procesar_fila(
                valores=valores,
                ids_dominio=ids_dominio,
                id_domicilio=id_domicilio,
                dnis_existentes=dnis_existentes,
                dnis_en_lote=dnis_en_lote,
            )

            if errores:
                # AF-RN07 — El registro debe ser atómico (todo o nada).
                # AF-RN11 — no se persiste
                # AF-RN12 — se registra con referencia a la fila

                for campo, descripcion in errores:
                    await self._error_repo.registrar_error(
                        id_importacion=id_importacion,
                        registro_origen=str(valores),
                        campo=campo,
                        descripcion_error=descripcion,
                        row_number=row.row_number,
                    )
                importacion.registrar_error(
                    campo=errores[0][0],
                    descripcion=errores[0][1],
                    registro_origen=str(valores),
                    row_number=row.row_number,
                )
                # AF-RN13 — continúa con la siguiente fila

            else:
                # RF9 — persistir afiliado válido
                await self._afiliado_repo.save(
                    datos=dato_normalizado,
                    id_importacion=id_importacion,
                )
                dni = dato_normalizado.get("dni")
                if dni:
                    dnis_en_lote.add(dni)

        # Paso 4 — Cerrar importación con resultado final
        await self._importacion_repo.completar_importacion(
            id_importacion=id_importacion,
            cantidad_errores=importacion.cantidad_errores,
        )
        importacion.completar()

        return importacion
