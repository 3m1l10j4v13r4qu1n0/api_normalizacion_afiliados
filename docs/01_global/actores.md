# Actores del Sistema

1. **Usuario Administrativo**: persona encargada de gestionar los datos de afiliados del sindicato. Importa datos, consulta y actualiza afiliados, y ejecuta los procesos de sincronización con Google Sheets.
2. **Sistema Cliente**: aplicación o script externo que consume la API REST. Envía datos para importación, consulta afiliados y actualiza registros.
3. **Google Sheets**: sistema externo que actúa como **fuente** de datos en el proceso de importación y como **destino** en el proceso de sincronización. La comunicación es bidireccional.