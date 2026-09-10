"""
Reglas de validación
AF-RN01 — DNI único en el sistema
AF-RN02 — No afiliados duplicados
AF-RN03 — DNI solo valores numéricos
AF-RN04 — Email con formato válido
AF-RN05 — Campos obligatorios no pueden estar vacíos
AF-RN06 — El afiliado debe tener un estado definido
RF4     — Validar formato de datos
RF5     — Detectar duplicados por DNI
AF-RN11 — Registros inválidos no se persisten
AF-RN12 — Errores se registran con referencia a fila/índice
AF-RN13 — Importación continúa aunque haya errores
"""

from email_validator import EmailNotValidError, validate_email

from app.domain.exceptions import DatoInvalidoError


def validar_nombre(nombre: str | None) -> None:
    """AF-RN05 — Los campos obligatorios no pueden estar vacíos"""
    if not nombre or not nombre.strip():
        raise DatoInvalidoError("El nombre es obligatorio")


def validar_apellido(apellido: str | None) -> None:
    """AF-RN05 — Los campos obligatorios no pueden estar vacíos"""
    if not apellido or not apellido.strip():
        raise DatoInvalidoError("El apellido es obligatorio")


def validar_dni(dni: str | None) -> None:
    """
    AF-RN05 — Los campos obligatorios no pueden estar vacíos
    AF-RN03 — El DNI debe contener solo valores numéricos
    """
    if not dni or not dni.strip():
        raise DatoInvalidoError("El DNI es obligatorio")

    dni_limpio = dni.strip().replace(".", "").replace("-", "")
    if not dni_limpio.isdigit():
        raise DatoInvalidoError("El DNI debe contener solo valores numéricos")


def validar_dni_duplicado(dni: str, dnis_existentes: set[str]) -> None:
    """
    RF5     — Detectar registros duplicados por DNI
    AF-RN01 — El DNI debe ser único en el sistema
    AF-RN02 — No se deben almacenar afiliados duplicados
    """
    if dni in dnis_existentes:
        raise DatoInvalidoError(f"El DNI '{dni}' ya existe en el sistema")


def validar_estado_afiliado(id_estado_afiliado: int | None) -> None:
    """AF-RN06 — El afiliado debe tener un estado definido"""
    if id_estado_afiliado is None:
        raise DatoInvalidoError("El estado del afiliado es obligatorio")


def validar_fecha_nacimiento(fecha_nacimiento) -> None:
    """AF-RN05 — La fecha de nacimiento no pueden estar vacías"""
    if fecha_nacimiento is None:
        raise DatoInvalidoError("La fecha de nacimiento es obligatoria")


def validar_email(email: str | None) -> None:
    """
    AF-RN04 — El email debe tener un formato válido
    RF4     — Validar formato de datos
    """
    if email is None:
        return  # ← opcional, se permite nulo

    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError as e:
        raise DatoInvalidoError(f"El email '{email}' no es válido: {e!s}")


def validar_afiliado(datos: dict) -> list[tuple[str, str]]:
    """
    Aplica todas las validaciones sobre un registro.
    Retorna lista de tuplas (campo, error).
    Lista vacía significa registro válido.
    RN11, RN12, RN13
    """
    errores = []

    validaciones = [
        ("nombre", lambda: validar_nombre(datos.get("nombre"))),
        ("apellido", lambda: validar_apellido(datos.get("apellido"))),
        ("dni", lambda: validar_dni(datos.get("dni"))),
        ("email", lambda: validar_email(datos.get("email"))),
        (
            "fecha_nacimiento",
            lambda: validar_fecha_nacimiento(datos.get("fecha_nacimiento")),
        ),
        (
            "id_estado_afiliado",
            lambda: validar_estado_afiliado(datos.get("id_estado_afiliado")),
        ),
    ]

    for campo, validar in validaciones:
        try:
            validar()
        except DatoInvalidoError as e:
            errores.append((campo, str(e)))  # ← RN12 registra el error

    return errores  # ← RN13 devuelve sin detener el proceso
