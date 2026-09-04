# HU-02: Plan de Pruebas (Specification by Example & TDD)

## Escenario 1: Alta de afiliado válido (Caso Positivo)
- **Dado** que se ingresa un afiliado con nombre, apellido, DNI y estado válidos.
- **Cuando** el usuario envía el registro.
- **Entonces** el sistema lo valida y normaliza.
- **Y** lo almacena en la base de datos.
- **Y** confirma la operación con `cantidad_registros_validos = 1`.

## Escenario 2: Campo obligatorio vacío (Caso Negativo)
- **Dado** que el afiliado no tiene nombre.
- **Cuando** el usuario envía el registro.
- **Entonces** el sistema informa el error de validación.
- **Y** no persiste el registro.

## Escenario 3: DNI duplicado (Caso Negativo)
- **Dado** que el DNI ingresado ya existe en el sistema.
- **Cuando** el usuario envía el registro.
- **Entonces** el sistema rechaza el afiliado como duplicado.
- **Y** devuelve un error de conflicto (409).

## Casos de Prueba TDD (Checklist para Desarrolladores)
- [ ] `test_alta_afiliado_valido()`
- [ ] `test_validar_campo_obligatorio_vacio()`
- [ ] `test_rechazar_dni_duplicado()`