from app.domain.models.input_row import InputRow
from app.domain.ports.sheet_data_port import SheetDataPort
from app.domain.services.data_transformer import DataTransformer


class ImportSheetUseCase:
    """
    Caso de uso UC4a: importar y transformar datos desde Google Sheets.

    Orquesta el pipeline:
        SheetDataPort   →  datos crudos (List[InputRow])
        DataTransformer →  List[InputRow] con claves pytónicas

    Depende de puertos e interfaces, no de implementaciones concretas.

    Attributes:
        _sheet_port  : SheetDataPort   — puerto de lectura del Sheet.
        _transformer : DataTransformer — transformador inyectado.

    Example:
        from app.domain.models.mapping import mapping
        from app.domain.services.data_key_mapper import DataKeyMapper
        from app.domain.services.data_transformer import DataTransformer
        from infrastructure.google.google_sheets_adapter import GoogleSheetsAdapter
        from infrastructure.google.gspread_client import GspreadSheetsClient

        client      = GspreadSheetsClient()
        adapter     = GoogleSheetsAdapter(client)
        mapper      = DataKeyMapper(mapping)
        transformer = DataTransformer(mapper)

        use_case    = ImportSheetUseCase(adapter, transformer)
        sheet_rows  = await use_case.execute("Respuestas!A1:Z")
    """

    def __init__(
        self,
        sheet_port: SheetDataPort,
        transformer: DataTransformer,
    ) -> None:
        self._sheet_port = sheet_port
        self._transformer = transformer

    async def execute(self, range_name: str) -> list[InputRow]:
        """
        Ejecuta UC4a: lee el Sheet y devuelve los datos como List[InputRow].

        Parameters:
            range_name : str — Rango de Sheets a leer (ej: "Respuestas!A1:Z").

        Returns:
            List[InputRow] — Una entrada por fila, con claves pytónicas
                             y row_number real del Sheet (base 2).

        Raises:
            ValueError — si el Sheet no devuelve datos.
        """
        list_sheet_rows = await self._sheet_port.fetch_rows(range_name)

        if not list_sheet_rows or not list_sheet_rows.values:
            raise ValueError(f"No se encontraron datos en el rango '{range_name}'.")

        raw = list_sheet_rows.values
        headers = raw[0]
        raw_data = raw[1:]

        return self._transformer.transform(raw_data=raw_data, headers=headers)
