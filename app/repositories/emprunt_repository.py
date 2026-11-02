from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Emprunt
from datetime import date

class EmpruntRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id_emprunt: int) -> Emprunt | None:
        return self.db.get(Emprunt, id_emprunt)
    
    def get_all(self) -> list[Emprunt]:
        statement = select(Emprunt).order_by(Emprunt.id_emprunt)
        return list(self.db.scalars(statement).all())

    def create(
        self,
        date_retour_prevue: date,
        id_adherent: int,
        id_ouvrage: int,
        date_emprunt: date | None = None) -> Emprunt:
        if date_emprunt is None:
            date_emprunt = date.today()

        emprunt = Emprunt(
            date_retour_prevue=date_retour_prevue,
            date_emprunt=date_emprunt,
            id_adherent=id_adherent,
            id_ouvrage=id_ouvrage
        )
        self.db.add(emprunt)
        self.db.commit()
        self.db.refresh(emprunt)

        return emprunt

    def get_by_adherent(self, id_adherent: int) -> list[Emprunt]:
        statement = select(Emprunt).where(Emprunt.id_adherent == id_adherent).order_by(Emprunt.date_emprunt)
        return list(self.db.scalars(statement).all())

    def get_by_en_cours_ouvrage(self, id_ouvrage: int) -> Emprunt | None:
        statement = select(Emprunt).where(Emprunt.id_ouvrage == id_ouvrage, Emprunt.date_retour_effective.is_(None)).order_by(Emprunt.date_emprunt)
        return self.db.scalars(statement).first()

    def get_en_cours(self) -> list[Emprunt]:
        statement = select(Emprunt).where(Emprunt.date_retour_effective.is_(None)).order_by(Emprunt.date_retour_prevue)
        return list(self.db.scalars(statement).all())