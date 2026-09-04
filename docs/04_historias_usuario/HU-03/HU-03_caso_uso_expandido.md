# HU-03: Caso de Uso Expandido (Consultar afiliados)

**Actor Principal**: Usuario Administrativo
**Precondición**: El actor está autenticado y puede consumir la API de consulta.

## Flujo Principal (Listado)
1. El actor solicita la lista de afiliados mediante `GET /afiliados/`.
2. El sistema obtiene los afiliados almacenados.
3. El sistema devuelve la lista en formato JSON.

## Flujo Principal (Consulta por ID)
1. El actor solicita un afiliado por su ID mediante `GET /afiliados/{afiliado_id}`.
2. El sistema busca el afiliado en la base de datos.
3. El sistema verifica que exista.
4. El sistema devuelve los datos del afiliado.

## Flujo Alternativo 1: Afiliado inexistente
1. El actor solicita un afiliado con un ID que no existe.
2. El sistema no encuentra el afiliado.
3. El sistema devuelve un error `404 Not Found`.

## Flujo Alternativo 2: Listado sin afiliados activos
1. El actor solicita el listado y no hay afiliados activos.
2. El sistema devuelve una lista vacía.

## Postcondición
- Se devuelve la información solicitada en formato JSON (los datos de un afiliado de baja lógica no se incluyen en listados activos).