from pydantic import BaseModel, Field, ConfigDict, model_validator
from datetime import date

class EmpruntCreate(BaseModel):
    id_ouvrage: int = Field(gt=0)
    id_adherent: int = Field(gt=0)
    date_emprunt: date | None = None
    date_retour_prevue: date

    @model_validator(mode="after")
    def verifier_coherence_dates(self):
        
        date_debut = self.date_emprunt
        if date_debut is None:
            date_debut = date.today()
        
        if date_debut > self.date_retour_prevue:
            raise ValueError(
                "La date de retour ne peut pas être antérieure à la date d'emprunt"
            )

        return self

class EmpruntRead(EmpruntCreate):
    id_emprunt: int
    date_retour_effective: date | None = None

    model_config = ConfigDict(from_attributes=True)