# Projet smartEngine - Groupe 2

## Contexte
Nous construisons smartEngine, un système de prédiction de churn
pour RavenStack, un SaaS B2B de gestion de projets.
L'objectif est d'identifier les clients à risque de résiliation
afin d'aider l'équipe Customer Success à agir avant le départ.
Les données brutes sont dans /data/raw/.

## Équipe Sprint 3
- Scrum Master : [Hamza Agoumi]
- Product Owner : [Nesrine Elghali]
- Développeurs IA : [Wfaa Benkorreche]
- Développeurs IA : [Danna Rodriguez]

## Ce qui a été fait au Sprint 1
- Dépôt GitHub créé et structuré
- GEMINI.md initial rédigé
- Veille outils complète (6 fiches) → docs/veille-outils.md
- Brief client reformulé → docs/brief-client.md
- Agent d'exploration créé → .gemini/agents/data-explorer.md
- Dataset exploré → docs/exploration-hamza/decouverte-dataset.md

## Ce qui a été fait au Sprint 2
- Agent data-engineer créé → .gemini/agents/data-engineer.md
- Nettoyage des données → src/clean_data.py
- Feature engineering → src/build_features.py
- Table analytique produite → data/processed/analytics.csv
- Rapport de nettoyage → outputs/rapport-nettoyage.md

## Ce qui a été fait au Sprint 3
- Agent de modélisation créé → .gemini/agents/model-trainer.md
- Modèle entraîné et sauvegardé → outputs/models/churn_model.joblib
- Script d'entraînement → src/train_model.py
- Script d'analyse du modèle → src/analyze_model_details.py
- Script de mise à jour des niveaux de risque → src/update_risk_levels.py
- Rapport du modèle → outputs/rapport-modele.md
- Scores de churn → outputs/scores.csv

## Sprint en cours
Sprint 4 — Déploiement et soutenance (26-29 mai 2026)

## Objectif Sprint 4
Déployer smartEngine :
- Dashboard Streamlit interactif pour l'équipe Customer Success
- Alertes automatiques via n8n pour les comptes à risque élevé
- Soutenance finale du projet

## Structure du projet
- data/raw/          → données CSV originales (NE JAMAIS MODIFIER)
- data/processed/    → table analytique produite au Sprint 2
- src/               → scripts Python générés par les agents
- outputs/           → rapports, modèles et analyses
- docs/              → documents du projet
- .gemini/agents/    → agents IA

## Conventions
- Tous les rapports sont en français
- Scripts Python → /src/
- Rapports → /outputs/
- Ne jamais modifier /data/raw/
- Table analytique finale → data/processed/analytics.csv
- Modèle → outputs/models/churn_model.joblib