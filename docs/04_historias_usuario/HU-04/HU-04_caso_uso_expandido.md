# HU-04: Caso de Uso Expandido (Actualizar afiliado)

**Actor Principal**: Usuario Administrativo
**Precondición**: El actor está autenticado y el afiliado puede o no existir.

## Flujo Principal (Éxito)
1. El actor envía los datos actualizados mediante `PATCH /afiliados/{afiliado_id}`.
2. El sistema verifica que el afiliado exista.
3. El sistema valida los datos enviados (formato y campos no vacíos).
4. El sistema verifica que el email no esté en uso por otro afiliado.
5. El sistema actualiza solo los campos enviados.
6. El sistema confirma la actualización devolviendo el afiliado actualizado.

## Flujo Alternativo 1: Afiliado inexistente
1. El actor envía una actualización para un ID inexistente.
2. El sistema no encuentra el afiliado.
3. El sistema devuelve un error `404 Not Found`.

## Flujo Alternativo 2: Email duplicado
1. El actor envía un email que ya está en uso por otro afiliado.
2. El sistema detecta el conflicto.
3. El sistema rechaza el cambio y devuelve un error `409 Conflict`.

## Flujo Alternativo 3: Nombre o apellido vacío
1. El actor envía un nombre o apellido vacío (solo espacios).
2. El sistema valida el dato.
3. El sistema rechaza la actualización con un error de validación.

## Postcondición
- Los campos enviados quedan actualizados en el afiliado.
- Se confirma la operación con el afiliado resultante.