# HU-04: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Actualización válida (Caso Positivo)
- **Dado** que existe un afiliado con ID 3 y email `viejo@test.com`.
- **Cuando** el actor envía `PATCH /afiliados/3` con email `nuevo@test.com`.
- **Entonces** el sistema actualiza el email del afiliado.
- **Y** devuelve el afiliado actualizado.

## Escenario 2: Afiliado inexistente (Caso Negativo)
- **Dado** que no existe un afiliado con ID 999.
- **Cuando** el actor envía una actualización para ese ID.
- **Entonces** el sistema devuelve un error `404 Not Found`.

## Escenario 3: Email duplicado (Caso Negativo)
- **Dado** que el email `yaenuso@test.com` pertenece a otro afiliado.
- **Cuando** el actor intenta asignarlo al afiliado actual.
- **Entonces** el sistema rechaza el cambio.
- **Y** devuelve un error `409 Conflict`.

## Escenario 4: Nombre vacío (Caso Borde)
- **Dado** que el actor envía `nombre` con solo espacios.
- **Cuando** intenta actualizar el afiliado.
- **Entonces** el sistema rechaza la actualización con un error de validación (422).

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_actualizar_afiliado_valido()`
- [ ] `test_actualizar_afiliado_inexistente_retorna_404()`
- [ ] `test_rechazar_email_duplicado()`
- [ ] `test_validar_nombre_vacio()`