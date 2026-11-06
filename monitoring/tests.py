from django.test import Client, TestCase, override_settings


class SentryErrorEndpointTests(TestCase):
    """Tests de la route /monitoring/sentry-error/ (vérification de Sentry)."""

    def test_la_route_genere_une_erreur_500(self):
        """La route doit produire une erreur 500 non gérée (envoyée à Sentry)."""
        response = Client(raise_request_exception=False).get(
            '/monitoring/sentry-error/'
        )
        self.assertEqual(response.status_code, 500)

    @override_settings(SENTRY_TEST_ENABLED=False)
    def test_la_route_peut_etre_desactivee(self):
        """SENTRY_TEST_ENABLED=False doit désactiver la route (404)."""
        response = self.client.get('/monitoring/sentry-error/')
        self.assertEqual(response.status_code, 404)
