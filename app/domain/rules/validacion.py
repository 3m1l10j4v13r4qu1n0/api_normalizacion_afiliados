"""
Reglas de validación
RN1  — DNI único en el sistema
RN2  — No afiliados duplicados
RN3  — DNI solo valores numéricos
RN4  — Nombre obligatorio
RN5  — DNI obligatorio
RN6  — Estado definido
RF4  — Validar formato de datos
RF5  — Detectar duplicados por DNI
RN11 — Registros inválidos no se persisten
RN12 — Errores de validación se registran
RN13 — Importación continúa aunque haya errores
"""

from email_validator import validate_email, EmailNotValidError
from app.domain.exceptions import DatoInvalidoError


def validar_nombre(nombre: str | None) -> None:
    """RN4 — El nombre es obligatorio"""
    if not nombre or not nombre.strip():
        raise DatoInvalidoError("El nombre es obligatorio")


def validar_apellido(apellido: str | None) -> None:
    """RN4 — El apellido es obligatorio"""
    if not apellido or not apellido.strip():
        raise DatoInvalidoError("El apellido es obligatorio")


def validar_dni(dni: str | None) -> None:
    """
    RN5 — El DNI es obligatorio
    RN3 — El DNI debe contener solo valores numéricos
    """
    if not dni or not dni.strip():
        raise DatoInvalidoError("El DNI es obligatorio")

    dni_limpio = dni.strip().replace(".", "").replace("-", "")
    if not dni_limpio.isdigit():
        raise DatoInvalidoError("El DNI debe contener solo valores numéricos")


def validar_dni_duplicado(dni: str, dnis_existentes: set[str]) -> None:
    """
    RF5 — Detectar registros duplicados por DNI
    RN1 — DNI único en el sistema
    RN2 — No afiliados duplicados
    """
    if dni in dnis_existentes:
        raise DatoInvalidoError(f"El DNI '{dni}' ya existe en el sistema")


def validar_estado_afiliado(id_estado_afiliado: int | None) -> None:
    """RN6 — El afiliado debe tener un estado definido"""
    if id_estado_afiliado is None:
        raise DatoInvalidoError("El estado del afiliado es obligatorio")


def validar_email(email: str | None) -> None:
    """RF4 — Validar formato del email"""
    if email is None:
        return  # ← opcional, se permite nulo

    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError as e:
        raise DatoInvalidoError(f"El email '{email}' no es válido: {str(e)}")


def validar_afiliado(datos: dict) -> list[tuple[str, str]]:
    """
    Aplica todas las validaciones sobre un registro.
    Retorna lista de tuplas (campo, error).
    Lista vacía significa registro válido.
    RN11, RN12, RN13
    """
    errores = []

    validaciones = [
        ("nombre",             lambda: validar_nombre(datos.get("nombre"))),
        ("apellido",           lambda: validar_apellido(datos.get("apellido"))),
        ("dni",                lambda: validar_dni(datos.get("dni"))),
        ("email",              lambda: validar_email(datos.get("email"))),
        ("id_estado_afiliado", lambda: validar_estado_afiliado(datos.get("id_estado_afiliado"))),
    ]

    for campo, validar in validaciones:
        try:
            validar()
        except DatoInvalidoError as e:
            errores.append((campo, str(e)))  # ← RN12 registra el error

    return errores  # ← RN13 devuelve sin detener el proceso


