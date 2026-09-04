# HU-01: Caso de Uso Expandido (Importar afiliados desde API)

**Actor Principal**: Sistema Cliente
**Precondición**: El sistema se encuentra operativo y el Sistema Cliente posee credenciales de autenticación válidas (provistas por un servicio externo de autenticación).

## Flujo Principal (Éxito)
1. El Sistema Cliente envía una lista de afiliados mediante `POST /afiliados/import`.
2. El sistema recibe el lote y lo identifica como procesamiento masivo (UC1a).
3. El sistema valida cada registro según las reglas de negocio (DNI único, campos obligatorios, formato).
4. El sistema normaliza la información de los registros válidos (nombres en mayúsculas, sin espacios, DNI sin puntos ni guiones).
5. El sistema almacena los registros válidos en la base de datos.
6. El sistema registra los errores de los registros inválidos.
7. El sistema devuelve el resumen del proceso (cantidad de procesados, válidos y errores).

## Flujo Alternativo 1: Registro con DNI duplicado
1. (Pasos 1-2 del flujo principal).
2. El sistema detecta que el DNI del registro ya existe en la base de datos.
3. El sistema registra el error como "DNI duplicado" y descarta el registro.
4. El sistema continúa procesando el resto del lote.

## Flujo Alternativo 2: Datos inválidos en procesamiento masivo
1. El sistema detecta errores de validación en uno o más registros (ej. campos obligatorios vacíos).
2. El sistema registra los errores encontrados.
3. El sistema continúa procesando los registros restantes (no interrumpe el lote).

## Flujo Alternativo 3: Error inesperado del sistema
1. Ocurre un error durante el procesamiento.
2. El sistema registra el error.
3. El sistema retorna una respuesta de fallo (500).

## Postcondición
- Los afiliados válidos quedan almacenados en la base de datos.
- Los errores de los registros inválidos quedan registrados con referencia a su índice/fila.
- Se devuelve un resumen con las métricas del proceso.