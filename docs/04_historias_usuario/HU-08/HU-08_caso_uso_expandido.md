# HU-08: Caso de Uso Expandido (Generar tabla de afiliados en Sheets)

**Actor Principal**: Usuario Administrativo
**Precondición**: Existen afiliados almacenados en la base de datos y la API tiene credenciales de acceso a Google Sheets configuradas.

## Flujo Principal (Éxito)
1. El usuario inicia la generación de la tabla mediante `POST /sync/sheets/export`.
2. El sistema obtiene los afiliados activos desde la base de datos.
3. El sistema ordena los afiliados alfabéticamente por nombre y apellido.
4. El sistema calcula la edad de cada afiliado a partir de su fecha de nacimiento.
5. El sistema construye la estructura de la tabla (Nombre y Apellido, Edad, Datos relevantes).
6. El sistema se conecta a Google Sheets con las credenciales configuradas.
7. El sistema verifica si la hoja existe:
   - Si no existe, la crea.
   - Si existe, la limpia o actualiza.
8. El sistema inserta los datos respetando el orden definido.
9. Google Sheets confirma la escritura.
10. El sistema devuelve la confirmación con la cantidad de registros procesados.

## Flujo Alternativo 1: No hay afiliados activos
1. El sistema detecta que no hay afiliados activos.
2. El sistema devuelve una respuesta indicando que no hay datos para exportar.

## Flujo Alternativo 2: Error en un registro
1. El sistema detecta un error al insertar un registro.
2. El sistema registra el error y continúa con los demás.

## Flujo Alternativo 3: La hoja no existe
1. El sistema detecta que la hoja no existe.
2. El sistema crea una nueva hoja antes de insertar los datos.

## Excepciones
- Error de autenticación con Google Sheets → `503 Service Unavailable`.
- Error de conexión con la base de datos → `500 Internal Server Error`.
- Fallo parcial en la escritura → resumen con registros exitosos y fallidos.

## Postcondición
- La hoja de Google Sheets contiene una tabla actualizada, ordenada y consistente con los afiliados del sistema.
- La edad no se persiste, se calcula en tiempo de ejecución (AF-RN19).