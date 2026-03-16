from typing import Dict

from domain.ports.outgoing.data_mapper_port import DataMapperPort
from domain.models.raw_data import RawData
from domain.models.mapped_data import MappedData

class KeyMapperAdapter(DataMapperPort):
    """
    ADAPTADOR DE SALIDA: Implementa el mapeo de claves.
    """
    async def add_new_key(self, 
                        data: RawData, 
                        mapping: Dict[str, str], 
                        models_name: str) -> None:
        
        # Lógica de mapeo
        for key, new_key in mapping.items():
            valor = data.get(key, "no_dato")
            if valor != "no_dato":
                # Si el valor no es "no_dato", lo agregamos al diccionario
                models_name[new_key] = valor

        
    async def remap_keys(self) -> MappedData:
        
        
        mapped_values = {"Marca temporal": "marca_temporal_creacion",
            "Apellido/s:": "apellido",
            "Nombre/s:": "nombre",
            "Fecha de Nacimiento:": "fecha_nacimiento",
            "D.N.I:": "dni",
            "Tel Contacto:": "telefono",
            "Email:": "email",
            "Nacionalidad:": "nacionalidad",
            "Género:": "genero",
            "Estado civil:": "estado_civil",
            "Domicilio (Calle y n°):": "direccion",
            "Localidad:": "localidad",
            "Provincia:": "provincia",
            "Codigo Postal:": "codigo_postal",
            "Estudios:": "nivel_educativo",
            "Titulo / Carrera:": "titulo_obtenido",
            "N° De Legajo:": "numero_legajo",
            "Comuna del sendero donde trabaja:": "comuna_donde_trabaja",
            "Inicio Actividad en Prevención:": "fecha_ingreso",
            "Relación de Dependencia:": "relacion_dependencia",
            }
        self.add_new_key(mapped_values, "afiliado")
        # ... lógica de transformación ...
        
        return MappedData(
            values=mapped_values,
            source=models_name
        )