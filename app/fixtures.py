from app.models import Auteur, Adherent, Ouvrage, Emprunt
from app.database import SessionLocal
from datetime import date


def load_fixtures():
    with SessionLocal() as db:
        db.query(Emprunt).delete()
        db.query(Ouvrage).delete()
        db.query(Auteur).delete()
        db.query(Adherent).delete()

        auteurs = [
            Auteur(
                nom="Laghlim",
                prenom="Rim",
                date_naissance=date(2002, 3, 6),
                lieu_naissance="Milan, Italie"
            ),
            Auteur(
                nom="Marcq",
                prenom="Cyril",
                date_naissance=date(1976, 10, 12),
                lieu_naissance="Alger, Algérie"
            ),
            Auteur(
                nom="El Hihi",
                prenom="Yassine",
                date_naissance=date(1930, 2, 7),
                lieu_naissance="Rabat, Maroc"
            ),
            Auteur(
                nom="Olivier",
                prenom="Loïc",
                date_naissance=None,
                lieu_naissance="Martinique"
            ),
            Auteur(
                nom="Dupont",
                prenom="Juliette",
                date_naissance=date(1957, 1, 5),
                lieu_naissance="Saint-Malo, France"
            )
        ]

        adherents = [
            Adherent(
                nom="Coquelet",
                prenom="Jordan",
                date_naissance=date(1998, 4, 12),
                date_inscription=date(2025, 9, 1),
                adresse="12 Rue Nationale, 59000 Lille",
                email="Coquelet.jordan@gmail.com",
                telephone="0612345678"
            ),
            Adherent(
                nom="Lenpik",
                prenom="Laura",
                date_naissance=date(1997, 12, 20),
                date_inscription=date(2024, 4, 15),
                adresse="29 rue des oranges, 92000 Paris",
                email="Lenpik.laura@gmail.com",
                telephone="0767453210"
            ),
            Adherent(
                nom="Rami",
                prenom="Younes",
                date_naissance=date(2000, 5, 7),
                date_inscription=date(2024, 4, 15),
                adresse="1 rue Jean, 59000 Lille",
                email="Rami.younes@gmail.com",
                telephone="0757009812"
            ),
            Adherent(
                nom="Obinu",
                prenom="Rossana",
                date_naissance=date(1990, 5, 12),
                date_inscription=date(2018, 10, 1),
                adresse="1 via statale, 424200 italie",
                email="Obinu.rossana@gmail.com",
                telephone="0756009809"
            ),
            Adherent(
                nom="Mars",
                prenom="Siham",
                date_naissance=date(1992, 6, 7),
                date_inscription=date(2017, 7, 11),
                adresse="269 rue roger salengro, 59000 Lille",
                email="Mars.siham@gmail.com",
                telephone="0612345678"
            )
        ]
        ouvrages = [
            Ouvrage(
                titre="Le destin",
                isbn="2786003451756",
                annee_parution=2020,
                collection="Vie",
                edition="Le Livre de Poche",
                genre="Roman",
                auteur=auteurs[0]
            ),
            Ouvrage(
                titre="La vie en couleur",
                isbn="4450936187952",
                annee_parution=2003,
                collection=None,
                edition="Le Livre de Poche",
                genre="Biographie",
                auteur=auteurs[1]
            ),
            Ouvrage(
                titre="La petite robe noire",
                isbn="8760451094729",
                annee_parution=2003,
                collection=None,
                edition="Folio",
                genre="Roman",
                auteur=auteurs[2]
            ),
            Ouvrage(
                titre="La magie noire",
                isbn="4598024378112",
                annee_parution=2005,
                collection=None,
                edition="Le Livre de Poche",
                genre="Poésie",
                auteur=auteurs[4]
            ),
            Ouvrage(
                titre="Le boxeur fou",
                isbn="2266789011567",
                annee_parution=2012,
                collection=None,
                edition="Le Livre de Poche",
                genre="Roman",
                auteur=auteurs[3]
            ),
            Ouvrage(
                titre="Le jour du verdict",
                isbn="4572893648099",
                annee_parution=1994,
                collection="J'ai lu",
                edition="Gallimard",
                genre="Théâtre",
                auteur=auteurs[4]
            ),
            Ouvrage(
                titre="Les riches",
                isbn="0093452768431",
                annee_parution=1980,
                collection=None,
                edition="Folio",
                genre="Roman",
                auteur=auteurs[2]
            ),
            Ouvrage(
                titre="Je sais pas ou aller",
                isbn="2348916900336",
                annee_parution=2023,
                collection="Vie",
                edition="Gallimard",
                genre=None,
                auteur=auteurs[0]
            ),
            Ouvrage(
                titre="Le chasseur",
                isbn="4083413769461",
                annee_parution=1999,
                collection=None,
                edition="Folio",
                genre="Poésie",
                auteur=auteurs[1]
            ),
            Ouvrage(
                titre="La reine et le roi",
                isbn="4563372897001",
                annee_parution=1989,
                collection=None,
                edition="Gallimard",
                genre="Théâtre",
                auteur=auteurs[4]
            )
        ]
        emprunts = [
            Emprunt(
                date_emprunt=date(2023, 6, 4),
                date_retour_prevue=date(2023, 11, 7),
                date_retour_effective=date(2023, 10, 3),
                adherent=adherents[4],
                ouvrage=ouvrages[1]
            ),
            Emprunt(
                date_emprunt=date(2026, 6, 4),
                date_retour_prevue=date(2026, 9, 3),
                date_retour_effective=date(2026, 10, 5),
                adherent=adherents[2],
                ouvrage=ouvrages[6]
            ),
            Emprunt(
                date_emprunt=date(2026, 2, 5),
                date_retour_prevue=date(2026, 9, 5),
                date_retour_effective=None,
                adherent=adherents[0],
                ouvrage=ouvrages[3]
            ),
            Emprunt(
                date_emprunt=date(2025, 10, 5),
                date_retour_prevue=date(2026, 5, 5),
                date_retour_effective=date(2026, 6, 3),
                adherent=adherents[0],
                ouvrage=ouvrages[1]
            ),
            Emprunt(
                date_emprunt=date(2024, 8, 4),
                date_retour_prevue=date(2024, 12, 7),
                date_retour_effective=date(2024, 12, 7),
                adherent=adherents[4],
                ouvrage=ouvrages[2]
            ),
            Emprunt(
                date_emprunt=date(2026, 10, 5),
                date_retour_prevue=date(2027, 2, 7),
                date_retour_effective=None,
                adherent=adherents[2],
                ouvrage=ouvrages[8]
            )
            
        ]

        db.add_all(auteurs)
        db.add_all(adherents)
        db.add_all(ouvrages)
        db.add_all(emprunts)
        db.commit()

        print("Fixtures chargées avec succès.")

if __name__ == "__main__":
    load_fixtures()
        
