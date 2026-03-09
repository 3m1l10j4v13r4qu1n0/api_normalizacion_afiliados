from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from domain.exceptions import (
    AfiliadoNoEncontradoError,
    EmailDuplicadoError,       
    DatoInvalidoError,          
    ImportacionError,
    SincronizacionError,
    FechaInvalidaError,
)

def registrar_handlers(app: FastAPI):

    @app.exception_handler(AfiliadoNoEncontradoError)
    async def afiliado_no_encontrado_handler(request: Request, exc: AfiliadoNoEncontradoError):
        return JSONResponse(
            status_code=404,
            content={"error": str(exc)}
        )

    @app.exception_handler(EmailDuplicadoError)          
    async def email_duplicado_handler(request: Request, exc: EmailDuplicadoError):
        return JSONResponse(
            status_code=409,                             
            content={"error": str(exc)}
        )

    @app.exception_handler(DatoInvalidoError)            
    async def dato_invalido_handler(request: Request, exc: DatoInvalidoError):
        return JSONResponse(
            status_code=422,
            content={"error": str(exc)}
        )

    @app.exception_handler(FechaInvalidaError)
    async def fecha_invalida_handler(request: Request, exc: FechaInvalidaError):
        return JSONResponse(
            status_code=422,                             
            content={"error": str(exc)}
        )

    @app.exception_handler(ImportacionError)
    async def importacion_handler(request: Request, exc: ImportacionError):
        return JSONResponse(
            status_code=500,
            content={"error": str(exc)}
        )

    @app.exception_handler(SincronizacionError)
    async def sincronizacion_handler(request: Request, exc: SincronizacionError):
        return JSONResponse(
            status_code=500,
            content={"error": str(exc)}
        )