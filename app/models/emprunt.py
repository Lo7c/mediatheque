from sqlalchemy import Date, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from app.database import Base

class Emprunt(Base):
    __tablename__ = "emprunt"

    id_emprunt: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    date_emprunt: Mapped[date] = mapped_column(Date, nullable=False)
    date_retour_prevue: Mapped[date] = mapped_column(Date, nullable=False)
    date_retour_effective: Mapped[date | None] = mapped_column(Date, nullable=True)
    id_ouvrage: Mapped[int] = mapped_column(Integer, ForeignKey("ouvrage.id_ouvrage"), nullable=False)
    id_adherent: Mapped[int] = mapped_column(Integer, ForeignKey("adherent.id_adherent"), nullable=False)
    ouvrage: Mapped["Ouvrage"] = relationship(back_populates="emprunts")
    adherent: Mapped["Adherent"] = relationship(back_populates="emprunts")