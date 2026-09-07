"""
Tests de DataTransformer

Cubre:
    - transform(): row_number base 2, values como dict, claves renombradas,
                   múltiples filas, lista vacía
    - Integración con DataKeyMapper mockeado
"""

import pytest
from unittest.mock import MagicMock
from app.domain.services.data_transformer import DataTransformer
from app.domain.models.input_row import InputRow


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mapping():
    return {
        "Apellido/s:" : "apellido",
        "Nombre/s:"   : "nombre",
        "D.N.I:"      : "dni",
        "Email:"      : "email",
    }

@pytest.fixture
def mapper(mapping):
    """DataKeyMapper real instanciado con el mapping de prueba."""
    from app.domain.services.data_key_mapper import DataKeyMapper
    return DataKeyMapper(mapping)

@pytest.fixture
def transformer(mapper):
    return DataTransformer(mapper)

@pytest.fixture
def mock_mapper():
    """DataKeyMapper mockeado para aislar DataTransformer completamente."""
    m = MagicMock()
    # remap() devuelve el dict que se le pasó a set_data() sin cambios
    m.remap.side_effect = lambda: m._last_data
    m.set_data.side_effect = lambda data: setattr(m, "_last_data", data)
    return m

@pytest.fixture
def transformer_mock(mock_mapper):
    return DataTransformer(mock_mapper)


# ---------------------------------------------------------------------------
# transform() — row_number
# ---------------------------------------------------------------------------

class TestTransformRowNumber:

    def test_primera_fila_row_number_es_2(self, transformer):
        """La primera fila de datos debe tener row_number=2."""
        headers  = ["Apellido/s:"]
        raw_data = [["García"]]
        resultado = transformer.transform(raw_data, headers)
        assert resultado[0].row_number == 2

    def test_segunda_fila_row_number_es_3(self, transformer):
        headers  = ["Apellido/s:"]
        raw_data = [["García"], ["López"]]
        resultado = transformer.transform(raw_data, headers)
        assert resultado[1].row_number == 3

    def test_row_numbers_incrementan_correctamente(self, transformer):
        headers  = ["Apellido/s:"]
        raw_data = [["García"], ["López"], ["Pérez"]]
        resultado = transformer.transform(raw_data, headers)
        assert [r.row_number for r in resultado] == [2, 3, 4]


# ---------------------------------------------------------------------------
# transform() — SheetRow y values
# ---------------------------------------------------------------------------

class TestTransformSheetRow:

    def test_retorna_lista_de_sheet_rows(self, transformer):
        headers  = ["Apellido/s:"]
        raw_data = [["García"]]
        resultado = transformer.transform(raw_data, headers)
        assert all(isinstance(r, InputRow) for r in resultado)

    def test_values_es_dict(self, transformer):
        headers  = ["Apellido/s:"]
        raw_data = [["García"]]
        resultado = transformer.transform(raw_data, headers)
        assert isinstance(resultado[0].values, dict)

    def test_claves_renombradas_por_mapper(self, transformer):
        """Las claves del dict deben ser las del mapping, no los headers originales."""
        headers  = ["Apellido/s:", "Nombre/s:"]
        raw_data = [["García", "Juan"]]
        resultado = transformer.transform(raw_data, headers)
        assert "apellido" in resultado[0].values
        assert "nombre"   in resultado[0].values
        assert "Apellido/s:" not in resultado[0].values

    def test_valores_correctos(self, transformer):
        headers  = ["Apellido/s:", "D.N.I:"]
        raw_data = [["García", "12345678"]]
        resultado = transformer.transform(raw_data, headers)
        assert resultado[0].values["apellido"] == "García"
        assert resultado[0].values["dni"]      == "12345678"

    def test_multiples_filas(self, transformer):
        headers  = ["Apellido/s:", "D.N.I:"]
        raw_data = [
            ["García", "12345678"],
            ["López",  "87654321"],
        ]
        resultado = transformer.transform(raw_data, headers)
        assert len(resultado) == 2
        assert resultado[0].values["apellido"] == "García"
        assert resultado[1].values["apellido"] == "López"

    def test_raw_data_vacia_retorna_lista_vacia(self, transformer):
        resultado = transformer.transform([], ["Apellido/s:"])
        assert resultado == []

    def test_cantidad_resultados_igual_a_raw_data(self, transformer):
        headers  = ["Apellido/s:"]
        raw_data = [["García"], ["López"], ["Pérez"]]
        resultado = transformer.transform(raw_data, headers)
        assert len(resultado) == len(raw_data)


# ---------------------------------------------------------------------------
# transform() — integración con DataKeyMapper mockeado
# ---------------------------------------------------------------------------

class TestTransformConMapperMock:

    def test_set_data_llamado_por_cada_fila(self, transformer_mock, mock_mapper):
        """set_data() debe llamarse una vez por fila."""
        headers  = ["Apellido/s:", "Nombre/s:"]
        raw_data = [["García", "Juan"], ["López", "Ana"]]
        transformer_mock.transform(raw_data, headers)
        assert mock_mapper.set_data.call_count == 2

    def test_remap_llamado_por_cada_fila(self, transformer_mock, mock_mapper):
        """remap() debe llamarse una vez por fila."""
        headers  = ["Apellido/s:"]
        raw_data = [["García"], ["López"]]
        transformer_mock.transform(raw_data, headers)
        assert mock_mapper.remap.call_count == 2

    def test_set_data_recibe_dict_con_headers_originales(self, transformer_mock, mock_mapper):
        """set_data() debe recibir el dict con los headers crudos del Sheet."""
        headers  = ["Apellido/s:", "Nombre/s:"]
        raw_data = [["García", "Juan"]]
        transformer_mock.transform(raw_data, headers)
        mock_mapper.set_data.assert_called_once_with({
            "Apellido/s:" : "García",
            "Nombre/s:"   : "Juan",
        })