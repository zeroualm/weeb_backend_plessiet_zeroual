#!/bin/sh
# Point d'entrée du conteneur Weeb (backend Django).
#   1. vérifie que la configuration minimale est présente ;
#   2. applique les migrations de la base ;
#   3. lance Gunicorn (ou la commande passée à `docker run`).
set -eu

# --- 1. Configuration obligatoire -------------------------------------------
# SECRET_KEY n'a pas de valeur par défaut dans settings.py : mieux vaut un
# message clair ici qu'une trace Python au démarrage.
if [ -z "${DJANGO_SECRET_KEY:-}" ]; then
    echo "ERREUR : DJANGO_SECRET_KEY est obligatoire." >&2
    echo "         Renseignez-la dans votre fichier .env (voir .env.example)," >&2
    echo "         puis relancez avec : docker run --env-file .env ..." >&2
    exit 1
fi

# --- 2. Base de données -------------------------------------------------------
# Migrations idempotentes : sans effet si la base est déjà à jour.
echo "==> Application des migrations Django"
python manage.py migrate --noinput

# --- 3. Lancement -------------------------------------------------------------
# Une commande explicite est passée ? On l'exécute telle quelle
# (ex. : docker run --rm weeb-backend python manage.py createsuperuser).
if [ "$#" -gt 0 ]; then
    exec "$@"
fi

echo "==> Démarrage de Gunicorn sur 0.0.0.0:${PORT:-8000} (${GUNICORN_WORKERS:-3} workers)"
exec gunicorn weeb_api.wsgi:application \
    --bind "0.0.0.0:${PORT:-8000}" \
    --workers "${GUNICORN_WORKERS:-3}" \
    --access-logfile - \
    --error-logfile -
