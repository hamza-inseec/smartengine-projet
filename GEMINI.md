# Projet smartEngine - Groupe 2 (hamza-inseec)

## Contexte
Nous construisons smartEngine, un système de prédiction de churn pour RavenStack, un SaaS B2B de gestion de projets.

L'objectif est d'identifier les clients à risque de résiliation afin d'aider l'équipe Customer Success à agir avant le départ.

Les données brutes sont situées dans `/data/raw/`.

## Structure du projet
- `data/raw/`        → données CSV originales (NE JAMAIS MODIFIER)
- `src/`             → scripts Python générés par les agents
- `outputs/`         → rapports et analyses générés
- `docs/`            → documents du projet (veille, brief, conception)
- `.gemini/agents/`  → agents IA utilisés dans le projet

## Conventions
- Tous les rapports doivent être en français.
- Les données dans `data/raw/` ne doivent jamais être modifiées.
- Les scripts Python doivent être placés dans `/src`.
- Les rapports doivent être placés dans `/outputs`.
- Chaque membre travaille sur sa branche personnelle (ici: `hamza-inseec`).

## Sprint en cours
Sprint 1 : Découverte du projet et exploration du dataset
