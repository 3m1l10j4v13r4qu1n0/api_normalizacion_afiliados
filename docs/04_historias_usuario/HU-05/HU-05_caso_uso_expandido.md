# HU-05: Caso de Uso Expandido (Importar desde Google Sheets)

**Actor Principal**: Usuario Administrativo
**Precondición**: La hoja de Google Sheets existe, tiene el formato esperado y la API tiene credenciales de acceso configuradas.

## Flujo Principal (Éxito)
1. El usuario inicia la importación mediante `POST /sync/sheets/import`.
2. El sistema se conecta a Google Sheets usando las credenciales configuradas (UC4a).
3. El sistema lee el rango especificado y separa encabezados de las filas de datos.
4. El sistema mapea los encabezados a variables internas del sistema.
5. El sistema construye los registros (`InputRow`) conservando el `row_number` original y descartando filas vacías.
6. El sistema valida y normaliza cada registro.
7. El sistema almacena los registros válidos y registra los errores.
8. El sistema devuelve el resumen del proceso.

## Flujo Alternativo 1: Registro con DNI duplicado
1. El sistema detecta que el DNI de una fila ya existe.
2. El sistema registra el error como "DNI duplicado" y descarta el registro.
3. El proceso continúa con las filas restantes.

## Flujo Alternativo 2: Hoja vacía
1. El sistema detecta que no hay filas de datos en el rango.
2. El sistema lanza una excepción de validación o devuelve un resumen con `cantidad_registros_procesados = 0`.

## Flujo Alternativo 3: Error de conexión con Google Sheets
1. El sistema no puede obtener los datos del rango.
2. Se lanza un error de sincronización.
3. El sistema responde con un error HTTP correspondiente.

## Excepciones
- Error de autenticación con Google Sheets → `503 Service Unavailable`.
- La hoja no existe o no es accesible → `404 Not Found`.
- Error de conexión con la base de datos → `500 Internal Server Error`.

## Postcondición
- Los registros válidos quedan almacenados en la base de datos.
- Los errores quedan registrados con su `row_number`.