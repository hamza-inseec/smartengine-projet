# Brief client – RavenStack

## Qui est RavenStack ?
RavenStack est un éditeur SaaS B2B qui propose une plateforme de gestion de projets
pour des équipes techniques. Les clients paient un abonnement mensuel avec plusieurs
offres (Starter, Growth, Enterprise).

## Problème métier : le churn
Une partie des clients résilie son abonnement chaque mois. Cela augmente le taux
de churn et réduit le MRR (revenu mensuel récurrent), ce qui rend le chiffre
d'affaires moins prévisible.

## Objectif du projet smartEngine
L'objectif est de construire smartEngine, un système de scoring qui prédit le risque
de churn pour chaque compte. Les scores doivent aider l'équipe Customer Success à
prioriser les clients à contacter avant qu'ils ne résilient.

## Rôle de l'équipe Customer Success
L'équipe Customer Success accompagne les clients après la vente, s'assure qu'ils
utilisent bien la plateforme et qu'ils en retirent de la valeur. Avec smartEngine,
elle pourra identifier plus tôt les comptes en difficulté et adapter ses actions
(onboarding, formation, relance, etc.).

## Critères de succès
- Avoir un modèle de churn avec des performances jugées suffisantes
  (par exemple AUC ≥ 0,75 sur le jeu de test).
- Mettre à disposition un dashboard simple permettant de filtrer les comptes
  par niveau de risque et par segment.
- Permettre à l'équipe Customer Success de réduire le churn sur une période cible
  (par exemple une baisse du churn de X % sur 6 à 12 mois).
