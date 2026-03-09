class AfiliadoNoEncontradoError(Exception):
    
    """El afiliado no existe"""
    
    def __init__(self, identificador):
        self.identificador = identificador
        self.mensaje = f"El afiliado '{identificador}' no existe"
        super().__init__(self.mensaje)
    
    def __str__(self):
        return self.mensaje


class DatoInvalidoError(Exception):
   
    """Los datos son inválidos"""
    
    def __init__(self, mensaje: str):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
    
    def __str__(self):
        return self.mensaje


class ImportacionError(Exception):
    
    """La importación falla"""
    
    def __init__(self, mensaje: str):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
    
    def __str__(self):
        return self.mensaje


class SincronizacionError(Exception):
    
    """La sincronización falla"""
    
    def __init__(self, mensaje: str):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
    
    def __str__(self):
        return self.mensaje
    


class FechaInvalidaError(Exception):
    """
    Excepción lanzada cuando hay inconsistencias en las fechas
    
    Ejemplos:
    - Fecha de fin anterior a fecha de inicio
    - Fecha de vencimiento en el pasado
    """
    
    def __init__(self, mensaje: str):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
    
    def __str__(self):
        return f"Error de fecha: {self.mensaje}"

class EmailDuplicadoError(DatoInvalidoError):
    
    """Error específico para emails duplicados"""
    
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"El email '{email}' ya está registrado")