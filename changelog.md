# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.5] - 2026-11-06

### Ajouté
- App `monitoring` avec la route `/monitoring/sentry-error/` qui génère une
  erreur 500 volontaire pour tester le renvoi des erreurs vers Sentry
  (désactivable avec `SENTRY_TEST_ENABLED=False`)

---

## [0.0.4] - 2026-11-06

### Corrigé
- Un `SENTRY_DSN` invalide (ex. clé publique manquante sur Render) ne bloque plus
  le démarrage : warning dans les logs et Sentry désactivé

---

## [0.0.3] - 2026-11-06

### Ajouté
- Monitoring Sentry (capture des erreurs Django / DRF, tracing optionnel)

---

## [0.0.2] - 2026-06-01

### Corrigé
- Présence de tag sur le repo

---

## [0.0.2] - 2026-06-01

### Corrigé
- Présence de tag sur le repo

---

## [0.0.1] - 2026-06-01

### Ajouté
- Initialisation du repo