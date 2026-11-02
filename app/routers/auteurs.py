from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.auteur_repository import AuteurRepository
from app.repositories.ouvrage_repository import OuvrageRepository
from app.schemas.auteur_schema import AuteurCreate, AuteurRead
from app.schemas.ouvrage_schema import OuvrageRead

router = APIRouter(prefix="/authors", tags=["Auteurs"])

@router.get("", response_model=list[AuteurRead])
def lister_auteurs(db: Session = Depends(get_db)):
    repo = AuteurRepository(db)
    return repo.get_all()

@router.post("", response_model=AuteurRead, status_code=201)
def creer_auteur(auteur: AuteurCreate, db: Session = Depends(get_db)):
    repo = AuteurRepository(db)
    return repo.create(**auteur.model_dump())

@router.get("/{id_auteur}", response_model=AuteurRead)
def consulter_auteur(id_auteur: int, db: Session = Depends(get_db)):
    repo = AuteurRepository(db)
    auteur = repo.get_by_id(id_auteur)
    if auteur is None:
        raise HTTPException(status_code=404, detail="Auteur introuvable")
    return auteur

@router.get("/{id_auteur}/books", response_model=list[OuvrageRead])
def rechercher_ouvrages_auteur(id_auteur: int, db: Session = Depends(get_db)):
    auteur_repo = AuteurRepository(db)
    auteur = auteur_repo.get_by_id(id_auteur)
    if auteur is None:
        raise HTTPException(status_code=404, detail="Auteur introuvable")
    ouvrage_repo = OuvrageRepository(db)
    return ouvrage_repo.get_by_auteur(id_auteur)

