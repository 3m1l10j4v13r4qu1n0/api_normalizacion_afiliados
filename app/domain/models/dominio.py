from enum import Enum


class Dominio(Enum):
    """
    Valores controlados del dominio (AF-RN17).

    Representa las tablas de valores controlados del sistema. El dominio
    solo conoce estos identificadores abstractos; el adapter de
    infraestructura los mapea internamente a sus tablas ORM concretas.

    Esto mantiene al dominio libre de cualquier dependencia de framework.
    """

    GENERO = "GENERO"
    ESTADO_CIVIL = "ESTADO_CIVIL"
    NIVEL_EDUCATIVO = "NIVEL_EDUCATIVO"
    RELACION_DEPENDENCIA = "RELACION_DEPENDENCIA"
    ESTADO_AFILIADO = "ESTADO_AFILIADO"
