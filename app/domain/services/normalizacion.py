"""
Reglas de normalización
AF-RN08 — Los nombres deben almacenarse en mayúsculas
AF-RN09 — Los textos no deben contener espacios al inicio ni al final
AF-RN10 — Los DNI deben almacenarse sin puntos ni guiones

"""


def normalizar_texto(valor: str | None) -> str | None:
    """AF-RN09 — Los textos no deben contener espacios al inicio ni al final"""
    if valor is None:
        return None
    return valor.strip()


def normalizar_nombre(nombre: str | None) -> str | None:
    """
    AF-RN08 — Los nombres deben almacenarse en mayúsculas
    AF-RN09 — Los textos no deben contener espacios al inicio ni al final
    """
    if nombre is None:
        return None
    return nombre.strip().upper()


def normalizar_dni(dni: str | None) -> str | None:
    """
    AF-RN09 — Los textos no deben contener espacios al inicio ni al final
    AF-RN10 — Los DNI deben almacenarse sin puntos ni guiones
    """
    if dni is None:
        return None
    return dni.strip().replace(".", "").replace("-", "")


def normalizar_afiliado(datos: dict) -> dict:
    """
    Aplica todas las reglas de normalización sobre un registro.
    Datos nulos se transforman en valores por defecto cuando corresponda.
    """
    return {
        "apellido"        : normalizar_nombre(datos.get("apellido")),
        "nombre"          : normalizar_nombre(datos.get("nombre")),
        "dni"             : normalizar_dni(datos.get("dni")),
        "email"           : normalizar_texto(datos.get("email")),
        "telefono"        : normalizar_texto(datos.get("telefono")),
        "numero_legajo"   : normalizar_texto(datos.get("numero_legajo")),
        "titulo_obtenido" : normalizar_texto(datos.get("titulo_obtenido")),

        # RN9 — valores por defecto para nulos
        "id_estado_afiliado"      : datos.get("id_estado_afiliado", 1),  # ← 1 = Activo
        "id_genero"               : datos.get("id_genero"),
        "id_estado_civil"         : datos.get("id_estado_civil"),
        "id_nivel_educativo"      : datos.get("id_nivel_educativo"),
        "id_relacion_dependencia" : datos.get("id_relacion_dependencia"),

        # Fechas — sin normalización, se pasan tal cual
        "fecha_nacimiento" : datos.get("fecha_nacimiento"),
        "fecha_ingreso"    : datos.get("fecha_ingreso"),
        "fecha_alta"       : datos.get("fecha_alta"),
    }
