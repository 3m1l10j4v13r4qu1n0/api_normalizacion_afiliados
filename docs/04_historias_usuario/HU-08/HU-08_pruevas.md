# HU-08: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Generar tabla con afiliados ordenados (Caso Positivo)
- **Dado** que existen afiliados activos en la base de datos.
- **Cuando** el usuario inicia la generación de la tabla en Google Sheets.
- **Entonces** los afiliados se ordenan alfabéticamente por nombre y apellido.
- **Y** la tabla se genera con el formato correcto.

## Escenario 2: Cálculo de edad (Caso de Formato)
- **Dado** un afiliado con fecha de nacimiento 10/05/1990.
- **Cuando** se genera la tabla.
- **Entonces** el sistema calcula la edad dinámicamente al momento de la generación.
- **Y** no persiste la edad en la base de datos.

## Escenario 3: Hoja existente se sobrescribe (Caso Positivo)
- **Dado** que la hoja de destino ya existe con datos previos.
- **Cuando** se regenera la tabla.
- **Entonces** el sistema limpia y regraba la tabla.
- **Y** no se generan duplicados.

## Escenario 4: Hoja inexistente se crea (Caso Positivo)
- **Dado** que la hoja de destino no existe.
- **Cuando** se genera la tabla.
- **Entonces** el sistema crea la hoja antes de insertar los datos.

## Escenario 5: Sin afiliados activos (Caso Negativo)
- **Dado** que no hay afiliados activos.
- **Cuando** se genera la tabla.
- **Entonces** el sistema informa que no hay datos para exportar.

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_generar_tabla_ordenada_alfabeticamente()`
- [ ] `test_calcular_edad_dinamicamente()`
- [ ] `test_sobrescribir_hoja_existente()`
- [ ] `test_crear_hoja_inexistente()`
- [ ] `test_sin_afiliados_activos()`