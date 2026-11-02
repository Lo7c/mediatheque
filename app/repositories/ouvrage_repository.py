from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Ouvrage


class OuvrageRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id_ouvrage: int) -> Ouvrage | None:
        return self.db.get(Ouvrage, id_ouvrage)
    
    def get_all(self) -> list[Ouvrage]:
        statement = select(Ouvrage).order_by(Ouvrage.id_ouvrage)
        return list(self.db.scalars(statement).all())

    def create(
        self,
        titre: str,
        isbn: str,
        annee_parution: int,
        edition: str,
        id_auteur: int,
        collection: str | None = None,
        genre: str | None = None) -> Ouvrage :
        ouvrage = Ouvrage(
            titre=titre,
            isbn=isbn,
            annee_parution=annee_parution,
            edition=edition,
            id_auteur=id_auteur,
            collection=collection,
            genre=genre
        )

        self.db.add(ouvrage)
        self.db.commit()
        self.db.refresh(ouvrage)

        return ouvrage

    def delete(self, id_ouvrage: int) -> bool:
        ouvrage = self.get_by_id(id_ouvrage)

        if ouvrage is None:
            return False
        
        self.db.delete(ouvrage)
        self.db.commit()

        return True

    def get_by_auteur(self, id_auteur: int) -> list[Ouvrage]:
        statement = select(Ouvrage).where(Ouvrage.id_auteur == id_auteur).order_by(Ouvrage.id_ouvrage)
        return list(self.db.scalars(statement).all())


    