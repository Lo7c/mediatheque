from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.ouvrage_repository import OuvrageRepository
from app.repositories.adherent_repository import AdherentRepository
from app.repositories.emprunt_repository import EmpruntRepository
from app.schemas.emprunt_schema import EmpruntRead, EmpruntCreate

router = APIRouter(prefix="/loans", tags=["Emprunts"])

@router.post("", response_model=EmpruntRead, status_code=201)
def creer_emprunt(emprunt: EmpruntCreate, db: Session = Depends(get_db)):

    adherent_repo = AdherentRepository(db)
    adherent = adherent_repo.get_by_id(emprunt.id_adherent)
    if adherent is None:
        raise HTTPException(status_code=404, detail="Adhérent introuvable")

    ouvrage_repo = OuvrageRepository(db)
    ouvrage = ouvrage_repo.get_by_id(emprunt.id_ouvrage)
    if ouvrage is None:
        raise HTTPException(status_code=404, detail="Ouvrage introuvable")
    
    emprunt_repo = EmpruntRepository(db)
    emprunt_en_cours = emprunt_repo.get_by_en_cours_ouvrage(emprunt.id_ouvrage)
    if emprunt_en_cours is not None:
        raise HTTPException(status_code=409, detail="Ouvrage déjà emprunté")

    return emprunt_repo.create(**emprunt.model_dump())

@router.get("/en-cours", response_model=list[EmpruntRead])
def lister_emprunts_en_cours(db: Session = Depends(get_db)):
    repo = EmpruntRepository(db)
    return repo.get_en_cours()