from typing import Dict, List, Any, Optional
from domain.models.sheet_row import SheetRow
from .data_key_mapper import DataKeyMapper


class DataTransformer:
    """
    Orquesta el pipeline de transformación de datos crudos de Google Sheets
    en una lista de SheetRow con claves pytónicas.

    Pipeline interno:
        raw_data (List[List])
            → dicts con headers originales  
            → dicts con claves renombradas  (DataKeyMapper — inyectado)
            → List[SheetRow]                (modelo de dominio)

    El mapping específico del Sheet vive fuera de esta clase,
    en la capa de infraestructura (mapping.py), y se inyecta
    a través del DataKeyMapper.

    Attributes:
        _mapper : DataKeyMapper — renombrador de claves inyectado.

    Example:
        from infrastructure.sheets.mapping import mapping
        from infrastructure.sheets.data_key_mapper import DataKeyMapper

        mapper      = DataKeyMapper(mapping)
        transformer = DataTransformer(mapper)

        raw         = sheets_client.get_values("Respuestas!A1:Z")
        sheet_rows  = transformer.transform(raw_data=raw[1:], headers=raw[0])
    """

    def __init__(self, mapper: DataKeyMapper) -> None:
        self._mapper = mapper

    def transform(
        self,
        raw_data: List[List[Any]],
        headers:  List[str],
    ) -> List[SheetRow]:
        """
        Transforma los datos crudos del Sheet en una lista de SheetRow.

        Pasos internos:
            1. Combina cada fila con los headers → dict con claves originales.
            2. Pasa el dict por DataKeyMapper    → dict con claves pytónicas.
            3. Envuelve el resultado en SheetRow con row_number real del Sheet.

        Parameters:
            raw_data : List[List[Any]] — Filas de datos sin el header (raw[1:]).
            headers  : List[str]       — Headers crudos del Sheet     (raw[0]).

        Returns:
            List[SheetRow] — Una entrada por fila, row_number base 2
                             (coincide con el número real de fila en Sheets).
        """
        sheet_rows: List[SheetRow] = []

        for index, row in enumerate(raw_data):
            raw_dict = dict(zip(headers, row))

            self._mapper.set_data(raw_dict)
            renamed = self._mapper.remap()

            sheet_rows.append(
                SheetRow(
                    row_number=index + 2,   # +2: base 1 del Sheet + fila de header
                    values=renamed,
                )
            )

        return sheet_rows