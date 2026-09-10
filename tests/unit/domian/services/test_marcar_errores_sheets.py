"""
Tests de MarcarErroresSheetsUseCase (UC6)

Cubre:
    - Extracción de row_number de los errores
    - Eliminación de duplicados
    - Sin errores → no llama al port
    - Delega en SheetMarkingPort
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.application.use_cases.uc6_marcar_errores_sheets import (
    MarcarErroresSheetsUseCase,
)
from app.domain.models.error_validacion import ErrorValidacion


@pytest.fixture
def marking_port():
    return MagicMock(marcar_filas_con_errores=AsyncMock())


@pytest.fixture
def use_case(marking_port):
    return MarcarErroresSheetsUseCase(marking_port)


def _error(row_number: int) -> ErrorValidacion:
    return ErrorValidacion(
        registro_origen="fila",
        campo="dni",
        descripcion_error="error",
        id_importacion=1,
        row_number=row_number,
    )


class TestMarcarErroresSheets:

    def test_extrae_row_numbers_de_errores(self, use_case, marking_port):
        errores = [_error(2), _error(5), _error(7)]
        asyncio.run(use_case.execute(errores))
        marking_port.marcar_filas_con_errores.assert_called_once_with([2, 5, 7])

    def test_elimina_duplicados(self, use_case, marking_port):
        errores = [_error(2), _error(2), _error(5)]
        asyncio.run(use_case.execute(errores))
        marking_port.marcar_filas_con_errores.assert_called_once_with([2, 5])

    def test_sin_errores_no_llama_al_port(self, use_case, marking_port):
        asyncio.run(use_case.execute([]))
        marking_port.marcar_filas_con_errores.assert_not_called()

    def test_filas_ordenadas(self, use_case, marking_port):
        errores = [_error(5), _error(2), _error(7)]
        asyncio.run(use_case.execute(errores))
        marking_port.marcar_filas_con_errores.assert_called_once_with([2, 5, 7])
