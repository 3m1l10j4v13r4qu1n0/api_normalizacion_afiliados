from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ports.afiliado.afiliado_importacion_port import AfiliadoImportacionPort
from app.infrastructure.database.orm_models.afiliado_orm import AfiliadoORM


class AfiliadoImportacionRepository(AfiliadoImportacionPort):
    """
    Implementación del repositorio de afiliados para el pipeline de importación.
    Solo implementa AfiliadoImportacionPort — no puede consultar ni actualizar.
    La sesión se inyecta desde el contenedor de dependencias.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all_dnis(self) -> set[str]:
        """
        Retorna todos los DNIs registrados en la BD.
        Usado para validar duplicados antes de persistir (RN1, RN2, RF5).
        """
        resultado = await self._session.execute(select(AfiliadoORM.dni))
        return set(resultado.scalars().all())

    async def save(self, datos: dict, id_importacion: int) -> None:
        """
        Persiste un afiliado validado y normalizado.
        El domicilio (id_domicilio) ya debe estar resuelto en datos
        antes de llamar a este método.

        Parameters:
            datos          : dict — Salida de normalizar_afiliado() con
                                    IDs de dominio ya resueltos.
            id_importacion : int  — ID de la importación a la que pertenece.
        """
        afiliado = AfiliadoORM(
            apellido=datos.get("apellido"),
            nombre=datos.get("nombre"),
            dni=datos.get("dni"),
            email=datos.get("email"),
            telefono=datos.get("telefono"),
            numero_legajo=datos.get("numero_legajo"),
            fecha_nacimiento=datos.get("fecha_nacimiento"),
            fecha_ingreso=datos.get("fecha_ingreso"),
            fecha_alta=datos.get("fecha_alta"),
            titulo_obtenido=datos.get("titulo_obtenido"),
            id_genero=datos.get("id_genero"),
            id_estado_civil=datos.get("id_estado_civil"),
            id_nivel_educativo=datos.get("id_nivel_educativo"),
            id_relacion_dependencia=datos.get("id_relacion_dependencia"),
            id_estado_afiliado=datos.get("id_estado_afiliado", 1),
            id_domicilio=datos.get("id_domicilio"),
            id_importacion=id_importacion,
        )
        self._session.add(afiliado)
        await self._session.flush()
