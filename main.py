"""
Módulo principal de la API para el sistema de préstamos.

Este módulo inicializa FastAPI y define las rutas principales para usuarios, materiales y préstamos.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.usersRoutes import user
from routes.materialRoutes import material
from routes.loanRoutes import loan

app = FastAPI(
    title="Prestamos",
    description="API de prueba para registrar de prestamo de material educativo"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.include_router(user)
app.include_router(material)
app.include_router(loan)
