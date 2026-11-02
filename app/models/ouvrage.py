from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Ouvrage(Base):
    __tablename__ = "ouvrage"
    id_ouvrage: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    titre: Mapped[str] = mapped_column(String(150), nullable=False)
    isbn: Mapped[str] = mapped_column(String(13), nullable=False)
    annee_parution: Mapped[int] = mapped_column(Integer, nullable=False)
    collection: Mapped[str|None] = mapped_column(String(150), nullable=True)
    edition: Mapped[str] = mapped_column(String(150), nullable=False)
    id_auteur: Mapped[int] = mapped_column(Integer, ForeignKey("auteur.id_auteur"), nullable=False)
    auteur: Mapped["Auteur"] = relationship(back_populates="ouvrages")
    emprunts: Mapped[list["Emprunt"]] = relationship(back_populates="ouvrage")
    genre: Mapped[str|None] = mapped_column(String(50), nullable=True)