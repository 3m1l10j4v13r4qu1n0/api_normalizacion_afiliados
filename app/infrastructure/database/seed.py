from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.infrastructure.database.orm_models.dominios_orm import (
    GeneroORM,
    EstadoCivilORM,
    NivelEducativoORM,
    RelacionDependenciaORM,
    EstadoAfiliadoORM,
)


async def cargar_si_vacia(db: AsyncSession, modelo, datos: list):
    
    """Inserta datos solo si la tabla está vacía — evita duplicados"""
    
    resultado = await db.execute(select(modelo))
    
    if resultado.scalars().first() is None:
        for item in datos:
            db.add(item)
        await db.commit()
        print(f"✅ {modelo.__tablename__} cargada")
    else:
        print(f"⏭️  {modelo.__tablename__} ya tiene datos, se omite")


async def cargar_datos_iniciales(db: AsyncSession):

    await cargar_si_vacia(db, GeneroORM, [
        GeneroORM(descripcion="Masculino"),
        GeneroORM(descripcion="Femenino"),
        GeneroORM(descripcion="No binario"),
    ])

    await cargar_si_vacia(db, EstadoCivilORM, [
        EstadoCivilORM(descripcion="Soltero"),
        EstadoCivilORM(descripcion="Casado"),
        EstadoCivilORM(descripcion="Divorciado"),
        EstadoCivilORM(descripcion="Viudo"),
    ])

    await cargar_si_vacia(db, NivelEducativoORM, [
        NivelEducativoORM(descripcion="Primario"),
        NivelEducativoORM(descripcion="Secundario"),
        NivelEducativoORM(descripcion="Terciario"),
        NivelEducativoORM(descripcion="Universitario"),
    ])

    await cargar_si_vacia(db, RelacionDependenciaORM, [
        RelacionDependenciaORM(descripcion="Planta Permanente"),
        RelacionDependenciaORM(descripcion="Planta Transitoria"),
        RelacionDependenciaORM(descripcion="Monotributista"),
    ])

    await cargar_si_vacia(db, EstadoAfiliadoORM, [
        EstadoAfiliadoORM(descripcion="Activo"),
        EstadoAfiliadoORM(descripcion="Inactivo"),
    ])