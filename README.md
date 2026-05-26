# smartEngine 🚀

## Contexte

RavenStack est une entreprise SaaS B2B qui propose une plateforme de gestion de projets pour les équipes techniques.

Comme beaucoup d'entreprises SaaS, RavenStack perd certains clients chaque mois. Ce phénomène est appelé **churn** (résiliation d’abonnement).

## Objectif du projet

Le projet **smartEngine** vise à développer un système de prédiction du churn afin d’identifier les clients à risque de résiliation.

Ce système permettra à l’équipe **Customer Success** d’agir en amont pour améliorer la rétention des clients.

## Dataset

Le projet utilise 5 fichiers CSV :

| Fichier | Description |
|------|------|
| accounts.csv | informations des comptes clients |
| subscriptions.csv | historique des abonnements |
| feature_usage.csv | utilisation des fonctionnalités |
| support_tickets.csv | tickets de support |
| churn_events.csv | données de résiliation |

## Structure du projet

smartengine-groupe-X

- .gemini/agents → agents IA  
- data/raw → données du dataset  
- src → scripts Python  
- outputs → résultats et rapports  
- docs → documents du projet  

## Méthodologie

Le projet est réalisé en équipe selon la méthode **Scrum** et se déroule en **4 sprints** :

- Sprint 1 : découverte du projet et du dataset  
- Sprint 2 : traitement des données  
- Sprint 3 : modélisation prédictive  
- Sprint 4 : dashboard et déploiement  

## Technologies utilisées

- Python
- pandas
- scikit-learn
- Streamlit
- Gemini CLI
- GitHub
- n8n
