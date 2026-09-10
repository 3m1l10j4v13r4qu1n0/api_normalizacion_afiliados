"""
Tests de ExportarAfiliadosSheetsUseCase (UC8)

Cubre:
    - Exportación exitosa con afiliados activos
    - Afiliados ordenados alfabéticamente
    - Edad calculada correctamente
    - Sin afiliados activos → AfiliadoNoEncontradoError
    - Delega en SheetExportPort
"""

import asyncio
from datetime import UTC, date, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.application.use_cases.uc8_exportar_afiliados_sheets import (
    ExportarAfiliadosSheetsUseCase,
    calcular_edad,
)
from app.domain.exceptions import AfiliadoNoEncontradoError


class AfiliadoFake:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


@pytest.fixture
def query_repo():
    return MagicMock(obtener_activos=AsyncMock())


@pytest.fixture
def export_port():
    return MagicMock(exportar_tabla=AsyncMock())


@pytest.fixture
def use_case(query_repo, export_port):
    return ExportarAfiliadosSheetsUseCase(query_repo, export_port)


def _afiliado(
    nombre="Juan",
    apellido="Garcia",
    fecha_nacimiento=date(1990, 5, 15),
    dni="12345678",
    numero_legajo="L001",
    email="juan@test.com",
):
    return AfiliadoFake(
        nombre=nombre,
        apellido=apellido,
        fecha_nacimiento=fecha_nacimiento,
        dni=dni,
        numero_legajo=numero_legajo,
        email=email,
    )


class TestCalcularEdad:

    def test_edad_basica(self):
        assert calcular_edad(date(2000, 1, 1)) > 0

    def test_edad_cumpleanios_futuro(self):
        hoy = datetime.now(tz=UTC).date()
        futuro = date(hoy.year - 25, hoy.month + 1 if hoy.month < 12 else 1, 1)
        assert calcular_edad(futuro) == 24


class TestExportarAfiliadosSheets:

    def test_exporta_afiliados_activos(self, use_case, query_repo, export_port):
        query_repo.obtener_activos.return_value = [_afiliado()]
        asyncio.run(use_case.execute())
        export_port.exportar_tabla.assert_called_once()

    def test_ordena_alfabeticamente(self, use_case, query_repo, export_port):
        query_repo.obtener_activos.return_value = [
            _afiliado(nombre="Carlos", apellido="Zulu"),
            _afiliado(nombre="Ana", apellido="Alvarez"),
            _afiliado(nombre="Beatriz", apellido="Borges"),
        ]
        asyncio.run(use_case.execute())
        args = export_port.exportar_tabla.call_args
        filas = args.kwargs.get("filas") or args[0][2]
        nombres = [f.nombre_apellido for f in filas]
        assert nombres == ["Alvarez, Ana", "Borges, Beatriz", "Zulu, Carlos"]

    def test_sin_afiliados_lanza_excepcion(self, use_case, query_repo):
        query_repo.obtener_activos.return_value = []
        with pytest.raises(AfiliadoNoEncontradoError):
            asyncio.run(use_case.execute())

    def test_retorna_cantidad_correcta(self, use_case, query_repo, export_port):
        query_repo.obtener_activos.return_value = [
            _afiliado(),
            _afiliado(dni="99999999"),
        ]
        cantidad = asyncio.run(use_case.execute())
        assert cantidad == 2

    def test_email_opcional_no_falla(self, use_case, query_repo, export_port):
        query_repo.obtener_activos.return_value = [_afiliado(email=None)]
        asyncio.run(use_case.execute())
        export_port.exportar_tabla.assert_called_once()
