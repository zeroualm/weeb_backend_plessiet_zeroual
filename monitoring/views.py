"""
Vues du monitoring.

Cette app ne contient qu'une route de test : elle génère volontairement une
erreur 500 afin de vérifier que les erreurs remontent bien dans Sentry.
"""
import logging

from django.conf import settings
from django.http import Http404

logger = logging.getLogger(__name__)


def sentry_error(request):
    """
    Route de test de l'intégration Sentry.

    GET /monitoring/sentry-error/

    Lève volontairement une exception non gérée : Django renvoie une erreur 500
    et l'intégration Sentry (DjangoIntegration) envoie l'événement au projet
    configuré via SENTRY_DSN. L'erreur doit apparaître dans Sentry → Issues,
    avec l'environnement et la release définis dans settings.py.

    La route peut être désactivée avec la variable d'environnement
    SENTRY_TEST_ENABLED=False (elle renvoie alors une 404).
    """
    if not getattr(settings, 'SENTRY_TEST_ENABLED', True):
        raise Http404("Route de test Sentry désactivée.")

    logger.warning("Erreur volontaire générée pour tester l'envoi vers Sentry.")
    raise RuntimeError(
        "Erreur de test Sentry : exception volontaire pour vérifier que le "
        "monitoring remonte bien les erreurs."
    )
