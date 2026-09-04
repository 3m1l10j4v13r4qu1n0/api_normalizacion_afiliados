# HU-01: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Lote con registros válidos e inválidos (Caso Mixto)
- **Dado** que se envía una lista de 4 afiliados donde 3 son válidos y 1 tiene DNI duplicado.
- **Cuando** el sistema procesa el lote.
- **Entonces** se almacenan 3 afiliados válidos.
- **Y** se registra 1 error de validación por DNI duplicado.
- **Y** se devuelve `cantidad_registros_procesados = 4`, `cantidad_registros_validos = 3`, `cantidad_errores = 1`.

## Escenario 2: Afiliado sin nombre (Caso Negativo)
- **Dado** que un registro tiene el campo `nombre` vacío.
- **Cuando** el sistema valida el registro.
- **Entonces** el registro se descarta.
- **Y** se registra un error de campo obligatorio para "nombre".

## Escenario 3: Normalización de datos (Caso de Formato)
- **Dado** que un registro llega con nombre "juan" y DNI "12.345.678".
- **Cuando** el sistema lo normaliza.
- **Entonces** se almacena con nombre "JUAN" y DNI "12345678".

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_importar_lote_con_registros_validos_e_invalidos()`
- [ ] `test_rechazar_dni_duplicado()`
- [ ] `test_normalizar_nombre_y_dni()`
- [ ] `test_validar_campo_obligatorio_vacio()`