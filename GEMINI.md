# Projet smartEngine - Groupe 2

## Contexte
Nous construisons smartEngine, un système de prédiction de churn
pour RavenStack, un SaaS B2B de gestion de projets.
L'objectif est d'identifier les clients à risque de résiliation
afin d'aider l'équipe Customer Success à agir avant le départ.
Les données brutes sont dans /data/raw/.

## Équipe Sprint 3
- Scrum Master : Danna Rodriguez
- Product Owner : Hamza Agoumi
- Développeurs IA : Elghali Nesrine
- Développeurs IA : Wafaa Benkorreche

## Ce qui a été fait au Sprint 2
- Données nettoyées et validées
- Table analytique produite : `data/processed/analytics.csv` (500 comptes, 21 features)
- Scripts de traitement automatisés : `src/clean_data.py`, `src/build_features.py`

## Sprint en cours
Sprint 3 — Modélisation et Prédiction (27 avril 2026)

## Objectif Sprint 3
Entraîner un modèle prédictif performant pour identifier le churn et générer des scores de risque actionnables pour les équipes métiers.

## Livrables Sprint 3
- Agent de modélisation : `.gemini/agents/model-trainer.md`
- Meilleur modèle sauvegardé : `outputs/models/churn_model.joblib`
- Rapport de performance : `outputs/rapport-modele.md`
- Fichier de scoring final : `outputs/scores.csv`

## Structure du projet
- data/raw/          → données CSV originales (NE JAMAIS MODIFIER)
- data/processed/    → table analytique produite au Sprint 2
- src/               → scripts Python générés par les agents
- outputs/           → rapports et analyses
- docs/              → documents du projet
- .gemini/agents/    → agents IA

## Conventions
- Tous les rapports sont en français
- Scripts Python → /src/
- Rapports → /outputs/
- Ne jamais modifier /data/raw/
- Table analytique finale → data/processed/analytics.csv
```

---

