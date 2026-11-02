from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from app.database import Base

class Adherent(Base):
    __tablename__ = "adherent"

    id_adherent: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    nom: Mapped[str] = mapped_column(String(150), nullable=False)
    prenom: Mapped[str] = mapped_column(String(150), nullable=False)
    date_inscription: Mapped[date] = mapped_column(Date, nullable=False)
    date_naissance: Mapped[date | None] = mapped_column(Date, nullable=True)
    adresse: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    telephone: Mapped[str] = mapped_column(String(15), nullable=False)
    emprunts: Mapped[list["Emprunt"]] = relationship(back_populates="adherent")