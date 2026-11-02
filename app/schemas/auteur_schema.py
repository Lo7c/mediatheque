from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import date

class AuteurCreate(BaseModel):
    nom: str = Field(min_length=1, max_length=150)
    prenom: str = Field(min_length=1, max_length=150)
    date_naissance: date | None = None
    lieu_naissance: str | None = Field(default=None, max_length=150)

    @field_validator("nom", "prenom")
    @classmethod
    def nettoyer_nom_prenom(cls, value: str) -> str:
        value = value.strip()

        if len(value) < 1:
            raise ValueError(
                "Le nom/prénom doit contenir au moins 1 caractère."
            )
        
        return value
    
    @field_validator("date_naissance")
    @classmethod
    def date_naissance_correct(cls, value: date | None) -> date | None:

        if value is None:
            return value
        
        if value > date.today():
            raise ValueError(
                "La date de naissance ne peut pas être dans le futur."
            )
        return value

class AuteurRead(AuteurCreate):
    id_auteur: int

    model_config = ConfigDict(from_attributes=True)
        


