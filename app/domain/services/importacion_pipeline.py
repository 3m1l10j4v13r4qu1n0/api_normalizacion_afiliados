"""
Servicio de dominio puro del pipeline de importación.

Encapsula la lógica por fila (normalización + validación + detección de
duplicados por DNI) de la importación de afiliados. Es un servicio del
dominio: NO conoce repositorios, ORMs ni frameworks; recibe los datos ya
resueltos (IDs de valores controlados y domicilio) y retorna qué se debe
persistir o qué errores reportar.

Reglas cubiertas:
    RF3     — Validar datos obligatorios
    RF4     — Validar formato de datos
    RF5     — Detectar duplicados por DNI
    RF7     — Normalizar nombres
    RF8     — Normalizar formatos de texto
    AF-RN11 — Registros inválidos no se persisten
    AF-RN12 — Errores se registran con referencia a la fila
    AF-RN13 — Importación continúa aunque haya errores
"""

from app.domain.services.normalizacion import normalizar_afiliado
from app.domain.services.validacion import validar_afiliado, validar_dni_duplicado


def procesar_fila(
    valores        : dict,
    ids_dominio    : dict,
    id_domicilio   : int | None,
    dnis_existentes: set[str],
    dnis_en_lote   : set[str],
) -> tuple[dict, list[tuple[str, str]]]:
    """
    Procesa una única fila del lote: normaliza, valida y verifica
    duplicados por DNI.

    Parameters:
        valores         : dict  — Datos crudos de la fila (valores de InputRow).
        ids_dominio     : dict  — IDs resueltos de valores controlados
                                  (id_genero, id_estado_civil, id_nivel_educativo,
                                   id_relacion_dependencia, id_estado_afiliado).
        id_domicilio    : int   — ID del domicilio resuelto (puede ser None).
        dnis_existentes : set   — DNIs ya presentes en el sistema (RF5/RF1-RN0).
        dnis_en_lote    : set   — DNIs ya aceptados en este mismo lote.

    Returns:
        tuple[dict, list[tuple[str, str]]] — (dato_normalizado, errores).
        Si errores está vacío el registro es válido y `dato_normalizado`
        puede persistirse.
    """
    dato_normalizado = normalizar_afiliado({
        **valores,
        "id_genero"              : ids_dominio.get("id_genero"),
        "id_estado_civil"        : ids_dominio.get("id_estado_civil"),
        "id_nivel_educativo"     : ids_dominio.get("id_nivel_educativo"),
        "id_relacion_dependencia": ids_dominio.get("id_relacion_dependencia"),
        "id_estado_afiliado"     : ids_dominio.get("id_estado_afiliado") or 1,
        "id_domicilio"           : id_domicilio,
    })

    errores = validar_afiliado(dato_normalizado)

    dni = dato_normalizado.get("dni")
    if dni and not errores:
        try:
            validar_dni_duplicado(dni, dnis_existentes | dnis_en_lote)
        except Exception as e:
            errores.append(("dni", str(e)))

    return dato_normalizado, errores
