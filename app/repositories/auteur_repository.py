from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Auteur
from datetime import date

class AuteurRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id_auteur: int) -> Auteur | None:
        return self.db.get(Auteur, id_auteur)
    
    def get_all(self) -> list[Auteur]:
        statement = select(Auteur).order_by(Auteur.id_auteur)
        return list(self.db.scalars(statement).all())
    
    def create(
        self,
        nom: str,
        prenom: str,
        date_naissance: date | None = None, 
        lieu_naissance: str | None = None) -> Auteur:
        auteur = Auteur(
            nom=nom, 
            prenom=prenom, 
            date_naissance=date_naissance, 
            lieu_naissance=lieu_naissance)
        
        self.db.add(auteur)
        self.db.commit()
        self.db.refresh(auteur)

        return auteur