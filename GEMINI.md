# Projet smartEngine - Groupe 2

## Contexte
Nous construisons smartEngine, un système de prédiction de churn
pour RavenStack, un SaaS B2B de gestion de projets.
L'objectif est d'identifier les clients à risque de résiliation
afin d'aider l'équipe Customer Success à agir avant le départ.
Les données brutes sont dans /data/raw/.

## Équipe Sprint 2
- Scrum Master : Elghali Nesrine
- Product Owner : Wafaa Benkorreche
- Développeurs IA : Hamza Agoumi
- Développeurs IA : Danna Rodriguez

## Ce qui a été fait au Sprint 1
- Dépôt GitHub créé et structuré
- GEMINI.md initial rédigé
- Veille outils complète (6 fiches) → docs/veille-outils.md
- Brief client reformulé → docs/brief-client.md
- Agent d'exploration créé → .gemini/agents/data-explorer.md
- Dataset exploré → docs/exploration-hamza/decouverte-dataset.md

## Sprint en cours
Sprint 2 — Traitement des données (30 mars 2026)

## Objectif Sprint 2
Produire data/processed/analytics.csv :
une table analytique avec une ligne par account_id,
contenant toutes les features nécessaires pour la modélisation.

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

