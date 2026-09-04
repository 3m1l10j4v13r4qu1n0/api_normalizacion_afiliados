# HU-07: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Baja lógica de afiliado existente (Caso Positivo)
- **Dado** que existe un afiliado activo con ID 4.
- **Cuando** el actor solicita `DELETE /afiliados/4`.
- **Entonces** el sistema lo marca como inactivo.
- **Y** confirma la operación.
- **Y** el registro permanece en la base de datos.

## Escenario 2: Afiliado inexistente (Caso Negativo)
- **Dado** que no existe un afiliado con ID 999.
- **Cuando** el actor solicita su baja.
- **Entonces** el sistema devuelve un error `404 Not Found`.

## Escenario 3: Afiliado inactivo no aparece en listados (Caso de Integración)
- **Dado** un afiliado dado de baja.
- **Cuando** se consulta el listado de afiliados.
- **Entonces** el afiliado inactivo no aparece en los listados de activos.

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_dar_baja_afiliado_existente()`
- [ ] `test_dar_baja_afiliado_inexistente_retorna_404()`
- [ ] `test_afiliado_inactivo_no_aparece_en_listados()`