# HU-03: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Listar afiliados (Caso Positivo)
- **Dado** que existen afiliados almacenados.
- **Cuando** el actor solicita el listado.
- **Entonces** el sistema devuelve una lista de afiliados en formato JSON.

## Escenario 2: Consultar afiliado por ID existente (Caso Positivo)
- **Dado** que existe un afiliado con ID 5.
- **Cuando** el actor consulta `GET /afiliados/5`.
- **Entonces** el sistema devuelve los datos del afiliado.

## Escenario 3: Consultar afiliado por ID inexistente (Caso Negativo)
- **Dado** que no existe un afiliado con ID 999.
- **Cuando** el actor consulta `GET /afiliados/999`.
- **Entonces** el sistema devuelve un error `404 Not Found`.

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_listar_afiliados()`
- [ ] `test_obtener_afiliado_por_id_existente()`
- [ ] `test_obtener_afiliado_por_id_inexistente_retorna_404()`