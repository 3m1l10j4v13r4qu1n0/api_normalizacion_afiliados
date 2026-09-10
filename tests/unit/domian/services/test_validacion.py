"""
Tests de validacion.py

Cubre:
    - validar_nombre()
    - validar_apellido()
    - validar_dni()
    - validar_dni_duplicado()
    - validar_estado_afiliado()
    - validar_email()
    - validar_afiliado() — orquestador completo
"""

import pytest

from app.domain.exceptions import DatoInvalidoError
from app.domain.services.validacion import (
    validar_afiliado,
    validar_apellido,
    validar_dni,
    validar_dni_duplicado,
    validar_email,
    validar_estado_afiliado,
    validar_nombre,
)

# ---------------------------------------------------------------------------
# validar_nombre()
# ---------------------------------------------------------------------------


class TestValidarNombre:

    def test_nombre_valido(self):
        validar_nombre("Juan")  # no lanza

    def test_nombre_none_lanza_error(self):
        with pytest.raises(DatoInvalidoError, match="obligatorio"):
            validar_nombre(None)

    def test_nombre_vacio_lanza_error(self):
        with pytest.raises(DatoInvalidoError, match="obligatorio"):
            validar_nombre("")

    def test_nombre_solo_espacios_lanza_error(self):
        with pytest.raises(DatoInvalidoError, match="obligatorio"):
            validar_nombre("   ")

    def test_nombre_con_espacios_es_valido(self):
        validar_nombre("  Juan  ")  # strip lo limpia, no lanza


# ---------------------------------------------------------------------------
# validar_apellido()
# ---------------------------------------------------------------------------


class TestValidarApellido:

    def test_apellido_valido(self):
        validar_apellido("García")

    def test_apellido_none_lanza_error(self):
        with pytest.raises(DatoInvalidoError, match="obligatorio"):
            validar_apellido(None)

    def test_apellido_vacio_lanza_error(self):
        with pytest.raises(DatoInvalidoError, match="obligatorio"):
            validar_apellido("")

    def test_apellido_solo_espacios_lanza_error(self):
        with pytest.raises(DatoInvalidoError, match="obligatorio"):
            validar_apellido("   ")


# ---------------------------------------------------------------------------
# validar_dni()
# ---------------------------------------------------------------------------


class TestValidarDni:

    def test_dni_valido(self):
        validar_dni("12345678")

    def test_dni_con_puntos_es_valido(self):
        """Los puntos se limpian antes de validar."""
        validar_dni("12.345.678")

    def test_dni_con_guiones_es_valido(self):
        validar_dni("12-345-678")

    def test_dni_none_lanza_error(self):
        with pytest.raises(DatoInvalidoError, match="obligatorio"):
            validar_dni(None)

    def test_dni_vacio_lanza_error(self):
        with pytest.raises(DatoInvalidoError, match="obligatorio"):
            validar_dni("")

    def test_dni_solo_espacios_lanza_error(self):
        with pytest.raises(DatoInvalidoError, match="obligatorio"):
            validar_dni("   ")

    def test_dni_con_letras_lanza_error(self):
        with pytest.raises(DatoInvalidoError, match="numéricos"):
            validar_dni("ABC12345")

    def test_dni_alfanumerico_lanza_error(self):
        with pytest.raises(DatoInvalidoError, match="numéricos"):
            validar_dni("123ABC78")


# ---------------------------------------------------------------------------
# validar_dni_duplicado()
# ---------------------------------------------------------------------------


class TestValidarDniDuplicado:

    def test_dni_no_duplicado_no_lanza(self):
        validar_dni_duplicado("12345678", {"99999999", "88888888"})

    def test_dni_duplicado_lanza_error(self):
        with pytest.raises(DatoInvalidoError, match="ya existe"):
            validar_dni_duplicado("12345678", {"12345678", "99999999"})

    def test_set_vacio_no_lanza(self):
        validar_dni_duplicado("12345678", set())

    def test_mensaje_incluye_el_dni(self):
        with pytest.raises(DatoInvalidoError, match="12345678"):
            validar_dni_duplicado("12345678", {"12345678"})


# ---------------------------------------------------------------------------
# validar_estado_afiliado()
# ---------------------------------------------------------------------------


class TestValidarEstadoAfiliado:

    def test_estado_valido(self):
        validar_estado_afiliado(1)

    def test_estado_none_lanza_error(self):
        with pytest.raises(DatoInvalidoError, match="obligatorio"):
            validar_estado_afiliado(None)

    def test_estado_cero_es_valido(self):
        """0 es un entero válido, no es None."""
        validar_estado_afiliado(0)


# ---------------------------------------------------------------------------
# validar_email()
# ---------------------------------------------------------------------------


class TestValidarEmail:

    def test_email_valido(self):
        validar_email("juan@test.com")

    def test_email_none_no_lanza(self):
        """Email es opcional — None se permite."""
        validar_email(None)

    def test_email_sin_arroba_lanza_error(self):
        with pytest.raises(DatoInvalidoError, match="no es válido"):
            validar_email("juantest.com")

    def test_email_sin_dominio_lanza_error(self):
        with pytest.raises(DatoInvalidoError, match="no es válido"):
            validar_email("juan@")

    def test_email_sin_usuario_lanza_error(self):
        with pytest.raises(DatoInvalidoError, match="no es válido"):
            validar_email("@test.com")

    def test_mensaje_incluye_el_email(self):
        with pytest.raises(DatoInvalidoError, match="juantest.com"):
            validar_email("juantest.com")


# ---------------------------------------------------------------------------
# validar_afiliado() — orquestador
# ---------------------------------------------------------------------------


class TestValidarAfiliado:

    @pytest.fixture
    def datos_validos(self):
        return {
            "nombre": "Juan",
            "apellido": "García",
            "dni": "12345678",
            "email": "juan@test.com",
            "id_estado_afiliado": 1,
        }

    def test_registro_valido_retorna_lista_vacia(self, datos_validos):
        """RN13 — lista vacía significa registro válido."""
        errores = validar_afiliado(datos_validos)
        assert errores == []

    def test_retorna_lista_de_tuplas(self, datos_validos):
        datos_validos["nombre"] = None
        errores = validar_afiliado(datos_validos)
        assert isinstance(errores, list)
        assert all(isinstance(e, tuple) and len(e) == 2 for e in errores)

    def test_error_incluye_campo_correcto(self, datos_validos):
        datos_validos["nombre"] = None
        errores = validar_afiliado(datos_validos)
        campos = [e[0] for e in errores]
        assert "nombre" in campos

    def test_continua_aunque_haya_errores(self, datos_validos):
        """RN13 — si nombre y dni fallan, se registran ambos errores."""
        datos_validos["nombre"] = None
        datos_validos["dni"] = None
        errores = validar_afiliado(datos_validos)
        campos = [e[0] for e in errores]
        assert "nombre" in campos
        assert "dni" in campos

    def test_multiples_errores_todos_registrados(self, datos_validos):
        """RN12 — todos los errores se registran, no solo el primero."""
        datos_validos["nombre"] = None
        datos_validos["apellido"] = None
        datos_validos["dni"] = None
        datos_validos["id_estado_afiliado"] = None
        errores = validar_afiliado(datos_validos)
        assert len(errores) == 4

    def test_email_none_no_genera_error(self, datos_validos):
        """Email es opcional — None no debe generar error."""
        datos_validos["email"] = None
        errores = validar_afiliado(datos_validos)
        assert errores == []

    def test_email_invalido_genera_error(self, datos_validos):
        datos_validos["email"] = "no_es_email"
        errores = validar_afiliado(datos_validos)
        campos = [e[0] for e in errores]
        assert "email" in campos

    def test_dni_con_letras_genera_error(self, datos_validos):
        datos_validos["dni"] = "ABC123"
        errores = validar_afiliado(datos_validos)
        campos = [e[0] for e in errores]
        assert "dni" in campos

    def test_datos_completamente_vacios(self):
        """Todos los campos obligatorios ausentes generan sus errores."""
        errores = validar_afiliado({})
        campos = [e[0] for e in errores]
        assert "nombre" in campos
        assert "apellido" in campos
        assert "dni" in campos
        assert "id_estado_afiliado" in campos
