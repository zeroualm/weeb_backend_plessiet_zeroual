# Projet Weeb (backend)

## Description
API RESTful Django pour gérer l'authentification et l'autorisation avec JWT. 

---

## Stack
- Python 3.11+
- Django 6.0
- Django REST Framework
- Simple JWT

---

## Installation

1. **Cloner le projet**
```bash
git clone https://github.com/zeroualm/weeb_backend_plessiet_zeroual
cd config
```

2. **Créer et activer l'environnement virtuel**

```bash
python3 -m venv env
source env/bin/activate   # macOS / Linux
env\Scripts\activate      # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Appliquer les migrations**

```bash
python manage.py migrate
```

5. **Lancer le serveur**
```bash
python manage.py runserver
```

Serveur disponible sur : http://127.0.0.1:8000/

---

## Endpoints principaux 

* POST /api/users/signup/ --> Création de compte
* POST /api/users/token/ --> Connexion (retourne access et refresh JWT)
* POST /api/users/token/refresh/ --> Rafraîchir l’access token
* POST /api/users/password-reset/request/ --> Demande la réinitialisation du mot de passe
* POST /api/users/password-reset/confirm/ --> Confirme la réinitialisation du mot de passe

## Monitoring (Sentry)

Le backend est instrumenté avec [Sentry](https://sentry.io) pour remonter en
temps réel les exceptions non gérées (Django / DRF).

1. Créer un projet **Django** sur Sentry et récupérer le **DSN** du projet.
2. Ajouter le DSN dans le fichier `.env` :

```env
SENTRY_DSN=https://<cle>@oXXXXXX.ingest.sentry.io/<projet>
SENTRY_ENVIRONMENT=development
SENTRY_TRACES_SAMPLE_RATE=0.0
```

3. Redémarrer le serveur : les erreurs 500 remontent automatiquement dans Sentry.

Tant que `SENTRY_DSN` est vide, Sentry reste désactivé : aucun impact en local,
en CI ou pendant les tests.

| Variable | Défaut | Description |
| --- | --- | --- |
| `SENTRY_DSN` | *(vide)* | DSN du projet Sentry. Vide = Sentry désactivé. |
| `SENTRY_ENVIRONMENT` | `development` / `production` (selon `DJANGO_DEBUG`) | Environnement affiché dans Sentry. |
| `SENTRY_RELEASE` | *(détecté automatiquement)* | Version de l'application (ex. tag Git) associée aux événements. |
| `SENTRY_TRACES_SAMPLE_RATE` | `0.0` | Part des requêtes tracées (performance). `0.1` = 10 %. |
| `SENTRY_PROFILES_SAMPLE_RATE` | `0.0` | Part des requêtes profilées (nécessite le tracing). |
| `SENTRY_SEND_DEFAULT_PII` | `False` | Envoi des données personnelles (emails, corps de requête, cookies). |

> En production, définir ces variables dans l'environnement du serveur. Le
> fichier `.env` est déjà ignoré par Git : le DSN ne doit pas être commité.
