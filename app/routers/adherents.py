from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.adherent_repository import AdherentRepository
from app.repositories.emprunt_repository import EmpruntRepository
from app.schemas.adherent_schema import AdherentCreate, AdherentRead
from app.schemas.emprunt_schema import EmpruntRead

router = APIRouter(prefix="/members", tags=["Adhérents"])

@router.get("", response_model=list[AdherentRead])
def lister_adherents(db: Session = Depends(get_db)):
    repo = AdherentRepository(db)
    return repo.get_all()

@router.post("", response_model=AdherentRead, status_code=201)
def creer_adherent(adherent: AdherentCreate, db: Session = Depends(get_db)):
    repo = AdherentRepository(db)
    return repo.create(**adherent.model_dump())

@router.get("/{id_adherent}/loans", response_model=list[EmpruntRead])
def rechercher_emprunts_adherent(id_adherent: int, db: Session = Depends(get_db)):
    adherent_repo = AdherentRepository(db)
    adherent = adherent_repo.get_by_id(id_adherent)
    if adherent is None:
        raise HTTPException(status_code=404, detail="Adhérent introuvable")
    emprunt_repo = EmpruntRepository(db)
    return emprunt_repo.get_by_adherent(id_adherent)

@router.get("/{id_adherent}", response_model=AdherentRead)
def consulter_adherent(id_adherent: int, db: Session = Depends(get_db)):
    repo = AdherentRepository(db)
    adherent = repo.get_by_id(id_adherent)
    if adherent is None:
        raise HTTPException(status_code=404, detail="Adhérent introuvable")
    return adherent