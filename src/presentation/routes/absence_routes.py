from fastapi import FastAPI
from src.presentation.controller.absence_controller import router as absence_router

app = FastAPI(title="API de Ausências")

app.include_router(absence_router)