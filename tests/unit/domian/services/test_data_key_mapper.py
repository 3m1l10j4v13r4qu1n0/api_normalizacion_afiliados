"""
Tests de DataKeyMapper

Cubre:
    - set_data(): carga correcta, copia defensiva, data vacía
    - remap(): renombrado, claves ausentes ignoradas, error sin datos
    - get_data(): retorna estado actual
    - flujo completo: set_data → remap → get_data
"""

import pytest

from app.domain.services.data_key_mapper import DataKeyMapper

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mapping():
    return {
        "Apellido/s:": "apellido",
        "Nombre/s:": "nombre",
        "D.N.I:": "dni",
        "Email:": "email",
    }


@pytest.fixture
def mapper(mapping):
    return DataKeyMapper(mapping)


# ---------------------------------------------------------------------------
# set_data()
# ---------------------------------------------------------------------------


class TestSetData:

    def test_carga_datos_correctamente(self, mapper):
        data = {"Apellido/s:": "García"}
        mapper.set_data(data)
        assert mapper.get_data() == {"Apellido/s:": "García"}

    def test_hace_copia_defensiva(self, mapper):
        """Modificar el dict original no debe afectar al mapper."""
        data = {"Apellido/s:": "García"}
        mapper.set_data(data)
        data["Apellido/s:"] = "modificado"
        assert mapper.get_data()["Apellido/s:"] == "García"

    def test_data_none_inicializa_dict_vacio(self, mapper):
        mapper.set_data(None)
        assert mapper.get_data() == {}

    def test_data_vacia_inicializa_dict_vacio(self, mapper):
        mapper.set_data({})
        assert mapper.get_data() == {}

    def test_reemplaza_datos_anteriores(self, mapper):
        mapper.set_data({"Apellido/s:": "García"})
        mapper.set_data({"Nombre/s:": "Juan"})
        assert "Apellido/s:" not in mapper.get_data()
        assert "Nombre/s:" in mapper.get_data()


# ---------------------------------------------------------------------------
# remap()
# ---------------------------------------------------------------------------


class TestRemap:

    def test_renombra_clave_simple(self, mapper):
        mapper.set_data({"Apellido/s:": "García"})
        resultado = mapper.remap()
        assert "apellido" in resultado
        assert resultado["apellido"] == "García"

    def test_renombra_multiples_claves(self, mapper):
        mapper.set_data({"Apellido/s:": "García", "Nombre/s:": "Juan"})
        resultado = mapper.remap()
        assert resultado == {"apellido": "García", "nombre": "Juan"}

    def test_clave_ausente_en_mapping_se_ignora(self, mapper):
        """Una clave del dict que no está en el mapping no aparece en el resultado."""
        mapper.set_data({"Apellido/s:": "García", "Columna Extra": "valor"})
        resultado = mapper.remap()
        assert "columna_extra" not in resultado
        assert "Columna Extra" not in resultado

    def test_clave_del_mapping_ausente_en_data_se_ignora(self, mapper):
        """Una clave del mapping que no está en el dict no genera error."""
        mapper.set_data({"Apellido/s:": "García"})
        resultado = mapper.remap()
        assert "nombre" not in resultado
        assert "dni" not in resultado

    def test_header_original_no_aparece_en_resultado(self, mapper):
        mapper.set_data({"Apellido/s:": "García"})
        resultado = mapper.remap()
        assert "Apellido/s:" not in resultado

    def test_valores_se_preservan(self, mapper):
        mapper.set_data({"D.N.I:": "12345678", "Email:": "test@test.com"})
        resultado = mapper.remap()
        assert resultado["dni"] == "12345678"
        assert resultado["email"] == "test@test.com"

    def test_error_si_no_hay_datos(self, mapper):
        """remap() sin set_data() previo debe lanzar ValueError."""
        with pytest.raises(ValueError, match="set_data()"):
            mapper.remap()

    def test_error_si_data_fue_vaciada(self, mapper):
        """remap() después de set_data({}) debe lanzar ValueError."""
        mapper.set_data({})
        with pytest.raises(ValueError):
            mapper.remap()

    def test_actualiza_estado_interno(self, mapper):
        """Después de remap(), get_data() retorna el dict renombrado."""
        mapper.set_data({"Apellido/s:": "García"})
        mapper.remap()
        assert mapper.get_data() == {"apellido": "García"}


# ---------------------------------------------------------------------------
# Flujo completo
# ---------------------------------------------------------------------------


class TestFlujoCompleto:

    def test_multiples_filas_secuenciales(self, mapper):
        """Procesar múltiples filas en secuencia no genera contaminación entre filas."""
        fila1 = {"Apellido/s:": "García", "Nombre/s:": "Juan"}
        fila2 = {"Apellido/s:": "López", "Nombre/s:": "Ana"}

        mapper.set_data(fila1)
        resultado1 = mapper.remap()

        mapper.set_data(fila2)
        resultado2 = mapper.remap()

        assert resultado1["apellido"] == "García"
        assert resultado2["apellido"] == "López"

    def test_get_data_retorna_ultimo_estado(self, mapper):
        mapper.set_data({"Apellido/s:": "García"})
        mapper.remap()
        assert mapper.get_data() == {"apellido": "García"}

    def test_mapping_completo(self, mapper):
        """Todas las claves del mapping presentes en el dict se renombran."""
        data = {
            "Apellido/s:": "García",
            "Nombre/s:": "Juan",
            "D.N.I:": "12345678",
            "Email:": "juan@test.com",
        }
        mapper.set_data(data)
        resultado = mapper.remap()
        assert resultado == {
            "apellido": "García",
            "nombre": "Juan",
            "dni": "12345678",
            "email": "juan@test.com",
        }
