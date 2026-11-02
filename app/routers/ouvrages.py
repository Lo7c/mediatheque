from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.auteur_repository import AuteurRepository
from app.repositories.ouvrage_repository import OuvrageRepository
from app.schemas.ouvrage_schema import OuvrageRead, OuvrageCreate

router = APIRouter(prefix="/books", tags=["Ouvrages"])

@router.get("", response_model=list[OuvrageRead])
def lister_ouvrages(db: Session = Depends(get_db)):
    repo = OuvrageRepository(db)
    return repo.get_all()

@router.post("", response_model=OuvrageRead, status_code=201)
def creer_ouvrage(ouvrage: OuvrageCreate, db: Session = Depends(get_db)):
    auteur = AuteurRepository(db).get_by_id(ouvrage.id_auteur)
    if auteur is None:
        raise HTTPException(status_code=404, detail="Auteur introuvable")
    repo = OuvrageRepository(db)
    return repo.create(**ouvrage.model_dump())

@router.get("/{id_ouvrage}", response_model=OuvrageRead)
def consulter_ouvrage(id_ouvrage: int, db: Session = Depends(get_db)):
    repo = OuvrageRepository(db)
    ouvrage = repo.get_by_id(id_ouvrage)
    if ouvrage is None:
        raise HTTPException(status_code=404, detail="Ouvrage introuvable")
    return ouvrage

@router.delete("/{id_ouvrage}", status_code=204)
def supprimer_ouvrage(id_ouvrage: int, db: Session = Depends(get_db)):
    repo = OuvrageRepository(db)
    ouvrage = repo.get_by_id(id_ouvrage)
    if ouvrage is None:
        raise HTTPException(status_code=404, detail="Ouvrage introuvable")
    if ouvrage.emprunts:
        raise HTTPException(status_code=409, detail="Impossible de supprimer cet ouvrage: il possède un historique d'emprunts")
    repo.delete(id_ouvrage)
