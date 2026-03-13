from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from app.domain.models.error_validacion import ErrorValidacion


@dataclass
class Importacion:
    # Resultados del proceso
    cantidad_registros : int = 0
    cantidad_errores   : int = 0

    # Estado del proceso
    estado : str = "pendiente"   # pendiente | completada | fallida

    # Errores registrados durante la importación
    errores : list[ErrorValidacion] = field(default_factory=list)

    # Marca temporal — la asigna el sistema
    fecha_importacion : Optional[datetime] = None

    # Clave primaria — la asigna la BD
    id : Optional[int] = field(default=None)

    # ── Propiedades calculadas ──────────────────────────────

    @property
    def cantidad_validos(self) -> int:
        """Registros que pasaron la validación"""
        return self.cantidad_registros - self.cantidad_errores

    @property
    def tuvo_errores(self) -> bool:
        """Indica si la importación tuvo al menos un error"""
        return self.cantidad_errores > 0

    @property
    def fue_exitosa(self) -> bool:
        """Todos los registros fueron válidos"""
        return self.cantidad_errores == 0

    # ── Métodos de comportamiento ───────────────────────────

    def registrar_error(self, campo: str, descripcion: str, registro_origen: str) -> None:
        """
        RN12 — Los errores de validación deben registrarse
        RN13 — La importación continúa aunque haya errores
        """
        error = ErrorValidacion(
            registro_origen   = registro_origen,
            campo             = campo,
            descripcion_error = descripcion,
            id_importacion    = self.id
        )
        self.errores.append(error)
        self.cantidad_errores += 1

    def completar(self) -> None:
        """Marca la importación como completada"""
        self.estado = "completada"

    def marcar_fallida(self) -> None:
        """Marca la importación como fallida — error grave"""
        self.estado = "fallida"