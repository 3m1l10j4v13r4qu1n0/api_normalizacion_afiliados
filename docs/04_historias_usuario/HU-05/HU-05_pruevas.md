# HU-05: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Importación de hoja con registros válidos e inválidos (Caso Mixto)
- **Dado** una hoja de Google Sheets con 10 filas de datos (8 válidas y 2 con errores).
- **Cuando** el usuario inicia la importación desde Google Sheets.
- **Entonces** el sistema almacena 8 afiliados válidos.
- **Y** registra 2 errores.
- **Y** devuelve `cantidad_registros_procesados = 10`, `cantidad_registros_validos = 8`, `cantidad_errores = 2`.

## Escenario 2: Mapeo de encabezados y conservación de row_number (Caso de Formato)
- **Dado** que la hoja tiene encabezados que difieren de las variables internas.
- **Cuando** el sistema lee el rango.
- **Entonces** los encabezados se mapean a las variables internas.
- **Y** cada fila conserva su `row_number` original.

## Escenario 3: Fila con DNI duplicado (Caso Negativo)
- **Dado** que una fila tiene un DNI ya existente.
- **Cuando** se procesa el registro.
- **Entonces** se registra el error de duplicado.
- **Y** el registro se descarta.
- **Y** el proceso continúa con las filas restantes.

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_importar_desde_sheets_con_validos_e_invalidos()`
- [ ] `test_mapear_encabezados_y_conservar_row_number()`
- [ ] `test_rechazar_dni_duplicado_desde_sheets()`