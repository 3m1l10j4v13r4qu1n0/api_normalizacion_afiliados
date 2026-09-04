# HU-02: Caso de Uso Expandido (Registrar afiliado manualmente)

**Actor Principal**: Usuario Administrativo
**Precondición**: El usuario administrativo está autenticado y accede a la funcionalidad de alta manual de afiliados.

## Flujo Principal (Éxito)
1. El usuario ingresa los datos de un afiliado (individual) mediante `POST /afiliados/`.
2. El sistema recibe los datos y los identifica como carga individual (UC1b).
3. El sistema valida los datos (campos obligatorios, formato, DNI único).
4. El sistema normaliza la información (nombres en mayúsculas, sin espacios, DNI sin puntos ni guiones).
5. El sistema almacena el afiliado.
6. El sistema devuelve el resumen de la operación.

## Flujo Alternativo 1: Campos obligatorios vacíos
1. El sistema detecta campos obligatorios sin valor (ej. nombre, apellido o DNI).
2. El sistema informa los errores de validación al usuario.
3. El registro NO se persiste.

## Flujo Alternativo 2: DNI duplicado
1. El sistema detecta que el DNI ya existe en la base de datos.
2. El sistema rechaza el registro.
3. Se informa al usuario del conflicto.

## Postcondición
- Si el registro es válido, el afiliado queda almacenado normalizado y se confirma la operación.
- Si hay errores, estos se informan al usuario y no se persiste nada.