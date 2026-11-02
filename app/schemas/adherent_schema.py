from pydantic import BaseModel, Field, field_validator, ConfigDict, EmailStr
from datetime import date

class AdherentCreate(BaseModel):
    nom: str = Field(min_length=1, max_length=150)
    prenom: str = Field(min_length=1, max_length=150)
    adresse: str = Field(min_length=1, max_length=150)
    email: EmailStr
    telephone: str = Field(pattern=r"^0\d{9}$")
    date_naissance: date | None = None
    date_inscription: date | None = None


    @field_validator("nom", "prenom", "adresse")
    @classmethod
    def nettoyer_champs_obligatoires(cls, value: str) -> str:
        value = value.strip()

        if len(value) < 1:
            raise ValueError(
                "Ce champ ne peut pas être vide."
            )
        
        return value
    
    @field_validator("date_naissance", "date_inscription")
    @classmethod
    def date_correct(cls, value: date | None) -> date | None:

        if value is None:
            return value
        
        if value > date.today():
            raise ValueError(
                "Cette date ne peut pas être dans le futur."
            )
        return value
    
class AdherentRead(AdherentCreate):
    id_adherent: int

    model_config = ConfigDict(from_attributes=True)