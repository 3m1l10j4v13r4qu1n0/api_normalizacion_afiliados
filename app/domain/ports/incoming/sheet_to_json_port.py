from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Protocol
from dataclasses import dataclass
from datetime import datetime

class SheetToJsonPort(ABC):
    """
    PUERTO DE ENTRADA: Define el caso de uso principal.
    Expone la funcionalidad de mi aplicación al exterior.
    """
    
    @abstractmethod
    async def process_sheet(self, 
                           sheet_id: str, 
                           range_name: str, 
                           mapping: Dict[str, str],
                           models_name: str,
                           output_path: Optional[str] = None) -> str:
        """
        Procesa una hoja y genera JSON.
        Este es el contrato que mi app ofrece al mundo exterior.
        """
        pass


###

@dataclass
class ProcessSheetRequest:
    """
    DTO (Data Transfer Object) para la solicitud de procesamiento.
    
    Encapsula todos los parámetros necesarios para el caso de uso.
    Esto facilita agregar nuevos parámetros sin cambiar la interfaz.
    """
    sheet_id: str
    range_name: str
    mapping: Dict[str, str]
    models_name: str
    output_path: Optional[str] = None
    options: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Validaciones básicas del dominio."""
        if not self.sheet_id:
            raise ValueError("sheet_id no puede estar vacío")
        if not self.range_name:
            raise ValueError("range_name no puede estar vacío")
        if not self.mapping:
            raise ValueError("mapping no puede estar vacío")

@dataclass
class ProcessSheetResponse:
    """
    DTO para la respuesta del procesamiento.
    """
    success: bool
    json_data: Optional[str] = None
    error_message: Optional[str] = None
    record_count: Optional[int] = None
    processing_time_ms: Optional[int] = None
    output_location: Optional[str] = None
    
    @classmethod
    def success_response(cls, json_data: str, record_count: int, 
                        processing_time_ms: int, output_location: Optional[str] = None):
        """Factory method para respuesta exitosa."""
        return cls(
            success=True,
            json_data=json_data,
            record_count=record_count,
            processing_time_ms=processing_time_ms,
            output_location=output_location
        )
    
    @classmethod
    def error_response(cls, error_message: str):
        """Factory method para respuesta de error."""
        return cls(
            success=False,
            error_message=error_message
        )

class SheetToJsonPort(ABC):
    """
    PUERTO DE ENTRADA (DRIVING PORT)
    
    Define el contrato para el caso de uso principal de la aplicación:
    "Procesar una hoja de cálculo y generar un JSON"
    
    Este puerto es la puerta de entrada al dominio. Cualquier adaptador
    (web, cli, cola de mensajes) que quiera usar esta funcionalidad
    debe implementar este puerto.
    
    Beneficios:
    - Define claramente qué puede hacer la aplicación
    - Aísla el dominio de los mecanismos de entrega (HTTP, CLI, etc.)
    - Facilita el testing (puedes mockear este puerto)
    """
    
    @abstractmethod
    async def process_sheet(self, request: ProcessSheetRequest) -> ProcessSheetResponse:
        """
        Procesa una hoja de cálculo y genera un JSON.
        
        Este es el método principal del caso de uso. Recibe todos los parámetros
        necesarios encapsulados en un objeto Request y retorna una Response.
        
        Args:
            request: Objeto con todos los parámetros necesarios
                - sheet_id: ID de la hoja de cálculo
                - range_name: Rango de celdas a procesar
                - mapping: Diccionario con mapeo de claves
                - models_name: Nombre del modelo
                - output_path: Ruta opcional para guardar
                - options: Opciones adicionales de procesamiento
                
        Returns:
            ProcessSheetResponse: Objeto con el resultado del procesamiento
                - success: Indica si la operación fue exitosa
                - json_data: El JSON generado (si success=True)
                - error_message: Mensaje de error (si success=False)
                - record_count: Número de registros procesados
                - processing_time_ms: Tiempo de procesamiento
                - output_location: Dónde se guardó el archivo
                
        Examples:
            >>> request = ProcessSheetRequest(
            ...     sheet_id="abc123",
            ...     range_name="Hoja1!A1:C10",
            ...     mapping={"Name": "nombre", "Age": "edad"},
            ...     models_name="usuarios"
            ... )
            >>> response = await port.process_sheet(request)
            >>> if response.success:
            ...     print(f"JSON generado: {response.json_data[:50]}...")
            ... else:
            ...     print(f"Error: {response.error_message}")
        """
        pass
    
    @abstractmethod
    async def process_sheet_simple(self,
                                   sheet_id: str,
                                   range_name: str,
                                   mapping: Dict[str, str],
                                   models_name: str,
                                   output_path: Optional[str] = None) -> str:
        """
        Versión simplificada del caso de uso para casos donde no se necesitan opciones.
        
        Algunos adaptadores pueden preferir esta interfaz más simple.
        Por defecto, llama a process_sheet con options={}.
        
        Args:
            sheet_id: ID de la hoja de cálculo
            range_name: Rango de celdas
            mapping: Mapeo de claves
            models_name: Nombre del modelo
            output_path: Ruta opcional
            
        Returns:
            str: JSON string generado
            
        Raises:
            Exception: Si hay error en el procesamiento
        """
        # Implementación por defecto que usa el método principal
        request = ProcessSheetRequest(
            sheet_id=sheet_id,
            range_name=range_name,
            mapping=mapping,
            models_name=models_name,
            output_path=output_path,
            options={}
        )
        
        response = await self.process_sheet(request)
        
        if not response.success:
            raise Exception(f"Error procesando hoja: {response.error_message}")
        
        return response.json_data
