"""
Tests de normalizacion.py
Ubicación: tests/unit/domain/services/test_normalizacion.py

Cubre:
    - normalizar_texto()
    - normalizar_nombre()
    - normalizar_dni()
    - normalizar_afiliado() — orquestador completo
"""

import pytest
from datetime import date
from app.domain.services.normalizacion import (
    normalizar_texto,
    normalizar_nombre,
    normalizar_dni,
    normalizar_afiliado,
)


# ---------------------------------------------------------------------------
# normalizar_texto()
# ---------------------------------------------------------------------------

class TestNormalizarTexto:

    def test_elimina_espacios_inicio(self):
        assert normalizar_texto("  valor") == "valor"

    def test_elimina_espacios_final(self):
        assert normalizar_texto("valor  ") == "valor"

    def test_elimina_espacios_ambos_lados(self):
        assert normalizar_texto("  valor  ") == "valor"

    def test_none_retorna_none(self):
        assert normalizar_texto(None) is None

    def test_texto_sin_espacios_no_cambia(self):
        assert normalizar_texto("valor") == "valor"

    def test_texto_vacio_retorna_vacio(self):
        assert normalizar_texto("") == ""


# ---------------------------------------------------------------------------
# normalizar_nombre()
# ---------------------------------------------------------------------------

class TestNormalizarNombre:

    def test_convierte_a_mayusculas(self):
        """RN7 — nombres en mayúsculas."""
        assert normalizar_nombre("juan") == "JUAN"

    def test_elimina_espacios(self):
        """RN8 — sin espacios al inicio ni al final."""
        assert normalizar_nombre("  juan  ") == "JUAN"

    def test_mayusculas_y_sin_espacios(self):
        assert normalizar_nombre("  juan garcía  ") == "JUAN GARCÍA"

    def test_none_retorna_none(self):
        assert normalizar_nombre(None) is None

    def test_ya_en_mayusculas_no_cambia(self):
        assert normalizar_nombre("JUAN") == "JUAN"

    def test_mixto_convierte_todo(self):
        assert normalizar_nombre("JuAn GaRcÍa") == "JUAN GARCÍA"


# ---------------------------------------------------------------------------
# normalizar_dni()
# ---------------------------------------------------------------------------

class TestNormalizarDni:

    def test_elimina_puntos(self):
        """RN10 — DNI sin puntos."""
        assert normalizar_dni("12.345.678") == "12345678"

    def test_elimina_guiones(self):
        """RN10 — DNI sin guiones."""
        assert normalizar_dni("12-345-678") == "12345678"

    def test_elimina_puntos_y_guiones(self):
        assert normalizar_dni("12.345-678") == "12345678"

    def test_elimina_espacios(self):
        """RN8 — sin espacios."""
        assert normalizar_dni("  12345678  ") == "12345678"

    def test_none_retorna_none(self):
        assert normalizar_dni(None) is None

    def test_dni_limpio_no_cambia(self):
        assert normalizar_dni("12345678") == "12345678"


# ---------------------------------------------------------------------------
# normalizar_afiliado() — orquestador
# ---------------------------------------------------------------------------

class TestNormalizarAfiliado:

    @pytest.fixture
    def datos_completos(self):
        return {
            "apellido"               : "  garcía  ",
            "nombre"                 : "  juan  ",
            "dni"                    : "12.345.678",
            "email"                  : "  juan@test.com  ",
            "telefono"               : "  1234567890  ",
            "numero_legajo"          : "  L001  ",
            "titulo_obtenido"        : "  Licenciado  ",
            "id_estado_afiliado"     : 1,
            "id_genero"              : 2,
            "id_estado_civil"        : 1,
            "id_nivel_educativo"     : 4,
            "id_relacion_dependencia": 1,
            "fecha_nacimiento"       : date(1990, 5, 20),
            "fecha_ingreso"          : date(2020, 1, 1),
            "fecha_alta"             : date(2020, 1, 1),
        }

    def test_apellido_en_mayusculas_sin_espacios(self, datos_completos):
        resultado = normalizar_afiliado(datos_completos)
        assert resultado["apellido"] == "GARCÍA"

    def test_nombre_en_mayusculas_sin_espacios(self, datos_completos):
        resultado = normalizar_afiliado(datos_completos)
        assert resultado["nombre"] == "JUAN"

    def test_dni_sin_puntos(self, datos_completos):
        resultado = normalizar_afiliado(datos_completos)
        assert resultado["dni"] == "12345678"

    def test_email_sin_espacios(self, datos_completos):
        resultado = normalizar_afiliado(datos_completos)
        assert resultado["email"] == "juan@test.com"

    def test_telefono_sin_espacios(self, datos_completos):
        resultado = normalizar_afiliado(datos_completos)
        assert resultado["telefono"] == "1234567890"

    def test_numero_legajo_sin_espacios(self, datos_completos):
        resultado = normalizar_afiliado(datos_completos)
        assert resultado["numero_legajo"] == "L001"

    def test_ids_se_preservan(self, datos_completos):
        resultado = normalizar_afiliado(datos_completos)
        assert resultado["id_genero"]               == 2
        assert resultado["id_estado_civil"]         == 1
        assert resultado["id_nivel_educativo"]      == 4
        assert resultado["id_relacion_dependencia"] == 1

    def test_fechas_se_preservan_sin_cambios(self, datos_completos):
        """Las fechas se pasan tal cual, sin normalización."""
        resultado = normalizar_afiliado(datos_completos)
        assert resultado["fecha_nacimiento"] == date(1990, 5, 20)
        assert resultado["fecha_ingreso"]    == date(2020, 1, 1)
        assert resultado["fecha_alta"]       == date(2020, 1, 1)

    def test_id_estado_afiliado_default_1_si_ausente(self):
        """RN9 — si id_estado_afiliado no viene, se usa 1 (Activo) por defecto."""
        resultado = normalizar_afiliado({})
        assert resultado["id_estado_afiliado"] == 1

    def test_id_estado_afiliado_se_preserva_si_viene(self, datos_completos):
        datos_completos["id_estado_afiliado"] = 2
        resultado = normalizar_afiliado(datos_completos)
        assert resultado["id_estado_afiliado"] == 2

    def test_campos_opcionales_none_retornan_none(self):
        """RN9 — campos opcionales ausentes retornan None."""
        resultado = normalizar_afiliado({})
        assert resultado["id_genero"]               is None
        assert resultado["id_estado_civil"]         is None
        assert resultado["id_nivel_educativo"]      is None
        assert resultado["id_relacion_dependencia"] is None
        assert resultado["fecha_nacimiento"]        is None
        assert resultado["fecha_ingreso"]           is None
        assert resultado["fecha_alta"]              is None

    def test_retorna_todas_las_claves_esperadas(self):
        """El dict resultante siempre tiene las mismas claves."""
        resultado = normalizar_afiliado({})
        claves_esperadas = {
            "apellido", "nombre", "dni", "email", "telefono",
            "numero_legajo", "titulo_obtenido", "id_estado_afiliado",
            "id_genero", "id_estado_civil", "id_nivel_educativo",
            "id_relacion_dependencia", "fecha_nacimiento",
            "fecha_ingreso", "fecha_alta",
        }
        assert set(resultado.keys()) == claves_esperadas