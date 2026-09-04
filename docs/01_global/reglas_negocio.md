# Reglas de Negocio Transversales

Estas reglas aplican a múltiples Historias de Usuario y deben ser respetadas por el backend y los adaptadores de infraestructura:

1. **Identificación y unicidad (HU-1, HU-2, HU-4)**: el DNI del afiliado debe ser único en el sistema. No se deben almacenar afiliados duplicados (AF-RN01, AF-RN02).
2. **Formato del DNI (HU-1, HU-2)**: el DNI debe contener solo valores numéricos y almacenarse sin puntos ni guiones (AF-RN03, AF-RN10).
3. **Email (HU-1, HU-2, HU-4)**: el email debe tener un formato válido y no debe estar en uso por otro afiliado (AF-RN04).
4. **Datos obligatorios (HU-1, HU-2, HU-4)**: los campos obligatorios no pueden estar vacíos y el afiliado debe tener un estado definido (AF-RN05, AF-RN06, AF-RN07).
5. **Normalización de nombres (HU-1, HU-2)**: los nombres deben almacenarse en mayúsculas y sin espacios al inicio ni al final (AF-RN08, AF-RN09).
6. **Validación e importación (HU-1, HU-5)**: los registros con datos inválidos no deben persistirse (AF-RN11), los errores deben registrarse con referencia a la fila o índice (AF-RN12) y la importación debe continuar aunque existan registros inválidos (AF-RN13).
7. **Sincronización (HU-5, HU-6, HU-8)**: solo se sincronizan afiliados válidos (AF-RN14), la sincronización no debe modificar datos locales (AF-RN15) y los valores controlados (género, estado civil, nivel educativo, relación de dependencia, estado del afiliado) deben pertenecer a entidades de dominio (AF-RN17).
8. **Baja lógica (HU-7)**: la eliminación de un afiliado debe realizarse mediante baja lógica, marcando su estado como inactivo (AF-RN16).
9. **Visualización (HU-8)**: se muestra el nombre completo en una única columna (AF-RN18), la edad se calcula dinámicamente (AF-RN19), solo se exponen datos relevantes (AF-RN20) y los afiliados se ordenan alfabéticamente sin duplicados (AF-RN21, AF-RN22).
10. **Feedback de errores (HU-5, HU-6)**: si existe un error, el sistema debe informarlo al usuario (AF-RN23).