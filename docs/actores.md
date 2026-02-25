# Actores del Sistema
## Sistema de Normalización de Datos de Afiliados

### 1. Introducción
Este documento describe los actores que interactúan con la API de normalización de datos de afiliados.

Un actor puede ser una persona, sistema externo o aplicación que utiliza el sistema.

---

### 2. Actores identificados

#### Actor: Usuario Administrativo
Descripción:
Persona encargada de gestionar los datos de afiliados del sindicato.

Responsabilidades:
- Importar datos de afiliados
- Consultar información de afiliados
- Actualizar datos de afiliados
- Ejecutar procesos de sincronización

Tipo:
Actor humano

---

#### Actor: Sistema Externo (Google Sheets)
Descripción:
Sistema externo que actúa como fuente de datos en el proceso de importación y como destino en el proceso de sincronización. La comunicación es bidireccional.

Responsabilidades:
- Recibir datos sincronizados desde la API

Tipo:
Sistema externo

---

#### Actor: Sistema Cliente
Descripción:
Aplicación o script que consume la API REST.

Responsabilidades:
- Enviar datos para importación
- Consultar afiliados
- Actualizar afiliados

Tipo:
Sistema externo
