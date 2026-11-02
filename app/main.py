from fastapi import FastAPI
from app.routers.auteurs import router as auteurs_router
from app.routers.ouvrages import router as ouvrages_router
from app.routers.adherents import router as adherents_router
from app.routers.emprunts import router as emprunts_router

app = FastAPI(title="API Médiathèque")

app.include_router(auteurs_router)
app.include_router(ouvrages_router)
app.include_router(adherents_router)
app.include_router(emprunts_router)