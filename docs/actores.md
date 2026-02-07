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
Sistema utilizado para almacenar o visualizar información sincronizada de afiliados.

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
