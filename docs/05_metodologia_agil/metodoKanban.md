# Metodología (Kanban, WIP, flujo y ciclo de desarrollo con IA)

## Aplicación de Kanban en Trello

### Justificativo (por qué usamos Kanban)

Elegimos Kanban porque nos permite **organizar el trabajo por flujo**, visualizar el estado real de cada tarea y **adaptarnos rápido a los cambios** sin frenar el avance del proyecto. Al trabajar con un tablero (Trello) y límites de trabajo en curso (WIP), evitamos tener demasiadas tareas abiertas al mismo tiempo, reducimos bloqueos y mejoramos la coordinación del equipo.

Además, al tratarse de un proyecto de demostración, nos apoyamos y tomamos roles distintos cuando hace falta para agilizar el desarrollo y cumplir con los tiempos:

- **Emilio**: administrador del tablero, análisis funcional y backend.
- **Colaboradores**: documentación, testing y backend según necesidad.

Con esta metodología mantenemos un ritmo de entrega constante, priorizamos lo más importante y aseguramos calidad mediante revisiones y pruebas antes de dar una tarea por finalizada.

### Límites WIP definidos

- En proceso: máximo 2 tareas por persona.
- En revisión: máximo 3 tareas totales.

### Flujo de trabajo

1. El admin mueve tareas de Backlog a Pendiente según prioridad.
2. Cada desarrollador toma una tarea de Pendiente y la mueve a En proceso.
3. Al terminar el código, la mueve a En revisión y asigna un revisor.
4. El revisor valida y la mueve a Finalizado.
5. Si hay error, vuelve a Pendiente con un comentario.

### Política de commits en Trello

- Cada tarjeta en En proceso tiene un branch asociado en Git.
- El número de tarjeta (ej: HU-01) se usa en el mensaje de commit.

---

## Uso del ciclo de desarrollo con IA en nuestro proyecto

El ciclo de desarrollo de software (SDLC) son las etapas que seguimos para crear el sistema desde cero: análisis de requisitos, diseño, codificación, pruebas y entrega. Tradicionalmente, estas etapas las hace un equipo de personas. En nuestro proyecto, decidimos incorporar herramientas de Inteligencia Artificial (IA) como apoyo en varias de esas etapas.

La IA es una **asistente, no la protagonista**: propone borradores, pero el equipo decide qué sirve; sugiere código, pero los desarrolladores revisan y corrigen; identifica riesgos, pero el analista valida con el negocio.

| **Etapa** | **Qué hizo el equipo** | **Qué hizo la IA** |
| --- | --- | --- |
| Análisis de requisitos | Definimos el alcance del sistema y validamos con el negocio. | Nos ayudó a generar un borrador de 8 historias de usuario y a detectar requisitos faltantes. |
| Diseño | Definimos el modelo de datos y la arquitectura por capas. | La IA propuso una estructura inicial de base de datos y la organización de las capas. |
| Codificación | Escribimos e implementamos la lógica de negocio. | La IA sugirió fragmentos de código, casos de uso y tests unitarios. |
| Gestión de tareas | Organizamos el tablero Kanban en Trello. | La IA ayudó a desglosar historias en subtareas técnicas. |

Lo más importante que aprendimos es que **la IA no reemplaza el criterio del equipo**. Una sugerencia de la IA puede estar mal, ser incompleta o no aplicar a nuestro contexto. Siempre tenemos que revisar, ajustar y decidir nosotros.