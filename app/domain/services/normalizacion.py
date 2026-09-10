"""
Reglas de normalización
AF-RN08 — Los nombres deben almacenarse en mayúsculas
AF-RN09 — Los textos no deben contener espacios al inicio ni al final
AF-RN10 — Los DNI deben almacenarse sin puntos ni guiones

"""

from datetime import date, datetime


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


def normalizar_fecha(valor: str | date | None) -> date | None:
    """
    Convierte una fecha a `datetime.date`.

    Acepta un `date`/`datetime` ya resuelto (importación manual) o un string
    en formato ISO (`YYYY-MM-DD`) o latino (`d/m/Y`, con o sin hora, como
    llega desde Google Sheets). Si el valor es nulo o no se puede parsear,
    devuelve `None` para que la validación lo reporte como error.
    """
    if valor is None:
        return None
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    texto = str(valor).strip()
    if not texto:
        return None
    formatos = (
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
    )
    for fmt in formatos:
        try:
            return datetime.strptime(texto, fmt).date()
        except ValueError:
            continue
    return None


def normalizar_afiliado(datos: dict) -> dict:
    """
    Aplica todas las reglas de normalización sobre un registro.
    Datos nulos se transforman en valores por defecto cuando corresponda.
    """
    return {
        "apellido": normalizar_nombre(datos.get("apellido")),
        "nombre": normalizar_nombre(datos.get("nombre")),
        "dni": normalizar_dni(datos.get("dni")),
        "email": normalizar_texto(datos.get("email")),
        "telefono": normalizar_texto(datos.get("telefono")),
        "numero_legajo": normalizar_texto(datos.get("numero_legajo")),
        "titulo_obtenido": normalizar_texto(datos.get("titulo_obtenido")),
        # RN9 — valores por defecto para nulos
        "id_estado_afiliado": datos.get("id_estado_afiliado", 1),  # ← 1 = Activo
        "id_genero": datos.get("id_genero"),
        "id_estado_civil": datos.get("id_estado_civil"),
        "id_nivel_educativo": datos.get("id_nivel_educativo"),
        "id_relacion_dependencia": datos.get("id_relacion_dependencia"),
        # Domicilio — se propaga el ID ya resuelto (se persiste con el afiliado)
        "id_domicilio": datos.get("id_domicilio"),
        # Fechas — se normalizan a datetime.date (d/m/Y desde Sheets, ISO desde Pydantic)
        "fecha_nacimiento": normalizar_fecha(datos.get("fecha_nacimiento")),
        "fecha_ingreso": normalizar_fecha(datos.get("fecha_ingreso")),
        "fecha_alta": normalizar_fecha(datos.get("fecha_alta")),
    }
