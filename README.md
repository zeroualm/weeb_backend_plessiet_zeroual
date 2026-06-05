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