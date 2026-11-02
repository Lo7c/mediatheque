
# API Médiathèque

Loïc Olivier, Rim Laghlim

L'API permet de consulter la base de données d'une médiathèque, d'y ajouter des auteurs, adhérents, ouvrages et emprunts.
Pour cela on utilise FastAPI, SQLAlchemy, Alembic, SQLite.
Le dossier conception permet de comprendre le projet.

## Prérequis
- Python 3.10 ou plus récent (projet développé avec Python 3.13)
- pip

## Installation
```bash
git clone https://github.com/Lo7c/mediatheque.git
cd mediatheque
python3 -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration de la base de données

Le projet utilise SQLite: aucun serveur à installer ni à configurer.
Le fichier `mediatheque.db` est créé à la racine du projet lors de l'exécution des migrations.

L'adresse de la base est définie à deux endroits, qui doivent rester identiques:
- `DATABASE_URL` dans `app/database.py`(utilisée par l'API);
- `sqlalchemy.url` dans `alembic.ini` (utilisée par les migrations).

Le chemin étant relatif (`sqlite:///./mediatheque.db`), toutes les commandes (`alembic`, fixtures, `uvicorn`) doivent être lancées depuis la racine du projet.


## Migrations

```bash
alembic upgrade head
```

| Révision | Contenu |
|---|---|
| `f2aa52e7590f` | Création des tables auteur, ouvrage, adherent, emprunt |
| `8c4df117d7b1` | Ajout de la colonne `genre` (facultative) à la table ouvrage|

### Évolution du modèle: ajout du genre

Après la première version, la médiathèque a demandé de pouvoir classer les ouvrages par genre.
L'évolution a été faite sans supprimer ni recréer la base:

1. Ajout de l'attribut `genre` dans le modèle `Ouvrage`(`app/models/ouvrage.py`). Le texte a un maximum de 50 caractères, **facultatif**, car les ouvrages déjà enregistrés n'ont pas de genre.
2. Génération de la migration par comparaison entre le modèle et la base:
```bash
alembic revision --autogenerate -m "ajout du genre aux ouvrages"
```
La migration produite (`8c4df117d7b1`) contient uniquement l'ajout de la colonne (`add_column`) et sa suppression en cas de retour en arrière (`drop_column`).
3. Application de la migration à la base existante:

```bash
alembic upgrade head
```

Pour revenir à la version précédente:
```bash
alembic downgrade -1
```

## Chargement des fixtures

Le projet fournit un jeu de données de test dans `app/fixtures.py`.
Les migrations doivent avoir été appliquées avant (`alembic upgrade head`).

```bash
python3 -m app.fixtures
```
Le script vide d'abord les tables, des emprunts vers les auteurs pour respecter les clés étrangères, puis les remplit. Il peut donc être relancé à tout moment pour revenir au jeu de données d'origine, par exemple après les tests.

### Contenu

| Table | Nombre | Particularités |
|---|---|---|
| Auteurs | 5 | dont un auteur avec 3 ouvrages et un sans date de naissance |
| Ouvrages | 10 | dont un sans genre (créé avant l'ajout du genre en V2) |
| Adhérents | 5 | dont 2 sans aucun emprunt |
| Emprunts | 6 | dont 2 en cours, 1 en retard, et un même ouvrage emprunté deux fois |

### Cas de test couverts

| Cas à tester | Données à utiliser |
|---|---|
| Ouvrages d'un auteur | `GET /authors/4/books` (3 ouvrages)|
| Adhérent sans emprunt | `GET /members/4/loans` (liste vide) |
| Ouvrage déjà emprunté | `POST /loans` avec `"id_ouvrage": 6` ou `9` (409) |
| Ouvrage disponible | `POST /loans` avec `"id_ouvrage": 1` (201) |
| Suppression refusée | `DELETE /books/3` (ouvrage avec historique, 409) |
| Suppression acceptée | `DELETE /books/1` (ouvrage sans emprunt, 204) |
| Emprunts en cours | `GET /loans/en-cours` (2 emprunts, le plus en retard en premier) |


## Lancement de l'API
```bash
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000
- Documentation interactive: http://127.0.0.1:8000/docs

## Endpoints

| Méthode | URL | Description |
|---|---|---|
| GET | `/authors` | Lister les auteurs |
| POST | `/authors` | Créer un auteur |
| GET | `/authors/{id}` | Consulter un auteur |
| GET | `/authors/{id}/books` | Rechercher les ouvrages d'un auteur |
| GET | `/books` | Lister les ouvrages |
| POST | `/books` | Créer un ouvrage |
| GET | `/books/{id}` | Consulter un ouvrage |
| DELETE | `/books/{id}` | Supprimer un ouvrage |
| GET | `/members` | Lister les adhérents |
| POST | `/members` | Créer un adhérent |
| GET | `/members/{id}`| Consulter un adhérent *(ajout)* |
| GET | `/members/{id}/loans` | Consulter les emprunts d'un adhérent |
| POST | `/loans` | Créer un emprunt |
| GET | `/loans/en-cours`| Lister les emprunts en cours *(ajout)* |

## Exemples d'utilisation

Les identifiants ci-dessous correspondent aux données des fixtures

**Créer un auteur**: `POST /authors` -> 201

```json
{"nom": "Hugo", "prenom": "Victor", "date_naissance": "1802-02-26", "lieu_naissance": "Besançon"}
```

**Créer un emprunt**: `POST /loans` -> 201 (la date d'emprunt est celle du jour)
```json
{"id_ouvrage": 1, "id_adherent": 4, "date_retour_prevue": "2026-11-30"}
```

**Cas d'erreur**

| Requête | Réponse|
|---|---|
| `GET /authors/999` |404 - Auteur introuvable |
| `POST /books` avec `"id_auteur": 999` | 404 - Auteur introuvable |
| `POST /loans` avec `"id_ouvrage": 6`(" La magie noire ", déjà emprunté) | 409 - Ouvrage déjà emprunté |
| `POST /loans` avec une date de retour antérieure à la date d'emprunt | 422 |
| `DELETE /books/3` (" La vie en couleur ", a des emprunts)| 409 |

## Choix d'architecture

### Organisation

```
app/
├── database.py     # engine, session, Base, get_db
├── models/         # modèles SQLAlchemy
├── repositories/   # accès aux données
├── schemas/        # modèle Pydantic (Create / Read)
├── routers/        # endpoints FastAPI
├── fixtures.py     # jeu de données de test
└── main.py         # application FastAPI
migrations/         # migrations Alembic
```
Le projet sépare les responsabilités en couches:
- **models**: décrivent les tables (colonnes, clés, relations) avec SQLAlchemy; ils correspondent au MLD;
- **repositories**: seuls à accéder à la base (lecture, création, suppression); ils renvoient des objets ou `None`, sans gérer le HTTP;
- **schémas**: modèles Pydantic qui valident les données reçues (`...Create`) et définissent le format des réponses (`...Read`);
- **routers**: reçoivent les requêtes, appliquent les règles métier en s'appuyant sur les repositories et renvoient le code HTTP adapté.

```
Requête HTTP -> validation Pydantic -> route -> repository -> SQLAlchemy -> SQLite
```

### Règles métier

| Règle | Où elle est vérifiée | Réponse |
| --- | --- | --- |
| Auteur obligatoire | Route `POST /books` (+ colonne `id_auteur` NOT NULL) | 404 |
| Ouvrage disponible | Route `POST /loans` | 409 |
| Cohérence des dates | Schéma `EmpruntCreate` (`model_validator`) | 422 |
| Ressources inexistantes | Routes | 404 |

La cohérence des dates est vérifiée par Pydantic, car elle ne dépend que des données envoyées: elle est contrôlée avant même l'exécution de la route, donc avant tout enregistrement.
Les autres règles ont besoin de la base (l'auteur existe-t-il ? l'ouvrage est-il déjà emprunté ?): elles sont vérifiées dans les routes à l'aide de repositories.

Autres validations Pydantic:
- ISBN de 13 chiffres; email valide; téléphone de 10 chiffres commençant par 0;
- dates de naissance, d'inscription et année de parution non situées dans le futur;
- textes obligatoires non vides, avec suppression des espaces superflus;
- identifiants strictement positifs.

Codes HTTP utilisés: 200(lecture), 201(création), 204(suppression), 404(ressource inexistante), 409(conflit: ouvrage déjà emprunté ou suppression impossible), 422(données invalides).

### Choix de modélisation

- **Un ouvrage correspond à un exemplaire physique**: c'est ce qui donne son sens à la règle "un ouvrage ne peut pas avoir deux emprunts en cours". Il n'y a donc pas de quantité en stock.
- **Un ouvrage a un seul auteur** (cardinalité 1,1 de l'association ECRIRE): le sujet associe un ouvrage à "un auteur existant", et une simple clé étrangère `id_auteur` suffit, sans table d'association.
- **L'emprunt est une entité à part entière**, reliée à un adhérent et à un ouvrage: un même ouvrage peut être emprunté plusieurs fois au cours du temps, ce qui conserve l'historique.
- **Un emprunt est en cours quand `date_retour_effective` est vide**: aucun champ calculé (statut, durée) n'est stocké.
- **La suppression d'un ouvrage est refusée s'il a des emprunts (409)**, afin de conserver l'historique.
- **Les dates d'inscription et d'emprunt** prennent la date du jour si elles ne sont pas fournies.
- **Écarts entre conception et implémentation**: le genre figure dans le MCD final, mais a été ajouté dans une seconde migration pour répondre à l'évolution demandée. Les tables gardent les noms du MLD (en français), tandis que les URLs de l'API suivent celles imposées par le sujet (en anglais).