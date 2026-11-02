from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import date

class OuvrageCreate(BaseModel):
    titre: str = Field(min_length=1, max_length=150)
    isbn: str = Field(pattern=r"^\d{13}$")
    annee_parution: int = Field(gt=0)
    edition: str = Field(min_length=1, max_length=150)
    id_auteur: int = Field(gt=0)
    collection: str | None = Field(default=None, max_length=150)
    genre: str | None = Field(default=None, max_length=50)

    @field_validator("titre", "edition")
    @classmethod
    def nettoyer_titre_edition(cls, value: str) -> str:
        value = value.strip()

        if len(value) < 1:
            raise ValueError(
                "Ce champ ne peut pas être vide"
            )
        
        return value

    @field_validator("annee_parution")
    @classmethod
    def annee_parution_correct(cls, value: int) -> int:
        
        if value > date.today().year:
            raise ValueError(
                "L'année de parution ne peut pas être dans le futur."
            )
        return value


class OuvrageRead(OuvrageCreate):
    id_ouvrage: int

    model_config = ConfigDict(from_attributes=True)