from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from app.database import Base


class Auteur(Base):
    __tablename__ = "auteur"

    id_auteur: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    nom: Mapped[str] = mapped_column(String(150), nullable=False)
    prenom: Mapped[str] = mapped_column(String(150), nullable=False)
    date_naissance: Mapped[date | None] = mapped_column(Date, nullable=True)
    lieu_naissance: Mapped[str | None] = mapped_column(String(150), nullable=True)
    ouvrages: Mapped[list["Ouvrage"]] = relationship(back_populates="auteur")