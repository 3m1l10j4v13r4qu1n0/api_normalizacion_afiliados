# HU-07: Caso de Uso Expandido (Dar de baja afiliado)

**Actor Principal**: Usuario Administrativo
**Precondición**: El actor está autenticado y puede ejecutar la operación de baja.

## Flujo Principal (Éxito)
1. El actor solicita la baja de un afiliado mediante `DELETE /afiliados/{afiliado_id}`.
2. El sistema verifica la existencia del afiliado.
3. El sistema marca al afiliado como inactivo (baja lógica).
4. El sistema confirma la operación.

## Flujo Alternativo 1: Afiliado inexistente
1. El actor solicita la baja de un afiliado con ID inexistente.
2. El sistema no encuentra el afiliado.
3. El sistema devuelve un error `404 Not Found`.

## Postcondición
- El afiliado queda con estado inactivo.
- El registro NO se elimina físicamente de la base de datos (AF-RN16).