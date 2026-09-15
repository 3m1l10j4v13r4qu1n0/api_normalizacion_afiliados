"""
Tests de ActualizarHojaPendientesUseCase (UC6)

Cubre:
    - Agrupa errores por fila y construye las pendientes con su motivo
    - Mapea row_number real del Sheet (base 2) al índice de valores_crudos
    - Sin errores → guarda solo encabezados (hoja refleja "sin pendientes")
    - Delega en SheetCorreccionPort
    - No captura errores del port (el "no interrumpe" lo resuelve el router)
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.application.use_cases.uc6_actualizar_hoja_pendientes import (
    ActualizarHojaPendientesUseCase,
)
from app.domain.exceptions import SincronizacionError
from app.domain.models.error_validacion import ErrorValidacion


@pytest.fixture
def correccion_port():
    return MagicMock(guardar_pendientes=AsyncMock())


@pytest.fixture
def use_case(correccion_port):
    return ActualizarHojaPendientesUseCase(correccion_port)


def _error(row_number: int, campo: str = "dni", descripcion: str = "inválido"):
    return ErrorValidacion(
        registro_origen="fila",
        campo=campo,
        descripcion_error=descripcion,
        id_importacion=1,
        row_number=row_number,
    )


class TestActualizarHojaPendientes:

    def test_vuelca_filas_con_error_y_motivo(self, use_case, correccion_port):
        errores = [_error(2), _error(2, "email", "mal formato"), _error(5)]
        valores = [["Ana", "1"], ["Luis", "2"], ["Paz", "3"], ["Rosa", "4"]]

        asyncio.run(use_case.execute(["nombre", "dni"], valores, errores))

        correccion_port.guardar_pendientes.assert_called_once_with(
            ["nombre", "dni", "motivo del error"],
            [
                ["Ana", "1", "dni: inválido; email: mal formato"],
                ["Rosa", "4", "dni: inválido"],
            ],
        )

    def test_fila_fuera_de_rango_queda_vacia(self, use_case, correccion_port):
        errores = [_error(99)]
        valores = [["Ana", "1"]]

        asyncio.run(use_case.execute(["nombre", "dni"], valores, errores))

        _, filas = correccion_port.guardar_pendientes.call_args.args
        assert filas == [["dni: inválido"]]

    def test_sin_errores_guarda_solo_encabezados(self, use_case, correccion_port):
        asyncio.run(use_case.execute(["nombre", "dni"], [["Ana", "1"]], []))

        correccion_port.guardar_pendientes.assert_called_once_with(
            ["nombre", "dni", "motivo del error"],
            [],
        )

    def test_no_captura_error_del_port(self, use_case, correccion_port):
        correccion_port.guardar_pendientes.side_effect = SincronizacionError(
            "no se pudo actualizar"
        )
        with pytest.raises(SincronizacionError):
            asyncio.run(use_case.execute(["nombre"], [["Ana"]], [_error(2)]))
