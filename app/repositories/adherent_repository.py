from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Adherent
from datetime import date

class AdherentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id_adherent: int) -> Adherent | None:
        return self.db.get(Adherent, id_adherent)
    
    def get_all(self) -> list[Adherent]:
        statement = select(Adherent).order_by(Adherent.id_adherent)
        return list(self.db.scalars(statement).all())
    
    def create(
        self,
        nom: str,
        prenom: str,
        adresse: str,
        email: str,
        telephone: str,
        date_naissance: date | None = None,
        date_inscription: date | None = None) -> Adherent:
        if date_inscription is None:
            date_inscription = date.today()
            
        adherent = Adherent(
            nom=nom,
            prenom=prenom,
            date_naissance=date_naissance,
            date_inscription=date_inscription,
            adresse=adresse,
            email=email,
            telephone=telephone
        )
        self.db.add(adherent)
        self.db.commit()
        self.db.refresh(adherent)

        return adherent