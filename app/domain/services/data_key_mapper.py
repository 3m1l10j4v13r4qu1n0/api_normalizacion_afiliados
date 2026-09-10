from typing import Any


class DataKeyMapper:
    """
    Renombra las claves de un diccionario según un mapeo definido.

    Procesa un dict por vez (una fila / InputRow.values a la vez).
    Claves del dict que no estén en el mapping se ignoran silenciosamente.

    Attributes:
        _mapping : Dict[str, str] — {clave_original: clave_nueva}
        _data    : Dict[str, Any] — datos de la fila actual

    Example:
        mapper = DataKeyMapper(mapping)
        for row in rows:
            mapper.set_data(ow.values)
            renamed = mapper.remap()
    """

    def __init__(self, mapping: dict[str, str]) -> None:
        self._mapping: dict[str, str] = mapping
        self._data: dict[str, Any] = {}

    def set_data(self, data: dict[str, Any]) -> None:
        """Carga los datos de la fila a procesar."""
        self._data = data.copy() if data else {}

    def remap(self) -> dict[str, Any]:
        """
        Renombra las claves de _data según _mapping.

        - Claves presentes en el mapping  → se renombran.
        - Claves ausentes en el mapping   → se ignoran.

        Returns:
            Dict[str, Any] — nuevo dict con claves renombradas.

        Raises:
            ValueError — si se llama sin haber cargado datos con set_data().
        """
        if not self._data:
            raise ValueError("No hay datos para procesar. Llamá a set_data() primero.")

        self._data = {
            new_key: self._data[original_key]
            for original_key, new_key in self._mapping.items()
            if original_key in self._data
        }
        return self._data

    def get_data(self) -> dict[str, Any]:
        """Retorna el estado actual de _data."""
        return self._data
