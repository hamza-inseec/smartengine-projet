# Brief client – RavenStack / smartEngine

## 1. Contexte

RavenStack est un éditeur SaaS B2B qui propose une plateforme de gestion de projets pour des équipes tech.  
L’entreprise fonctionne par abonnement (Starter, Growth, Enterprise) et génère du MRR à partir des abonnements actifs.

Aujourd’hui, RavenStack fait face à un problème de churn : chaque mois, une partie des clients résilie et le MRR diminue de façon difficilement prévisible.  

## 2. Problématique

Sans système de prédiction, les équipes Customer Success ne savent pas quels comptes sont réellement à risque.  
Elles interviennent trop tard ou de manière non priorisée, ce qui limite l’impact des actions de rétention.

RavenStack a besoin d’identifier en amont les comptes qui risquent le plus de partir pour concentrer les efforts sur ces clients.

## 3. Solution proposée : smartEngine

Notre équipe va concevoir smartEngine, un système de scoring de churn basé sur les données historiques de RavenStack :

- Analyse et nettoyage des données clients (accounts, subscriptions, feature usage, support tickets, churn events).  
- Construction d’un modèle de prédiction du churn.  
- Mise à disposition du score dans un dashboard utilisable par les équipes Customer Success.  
- Automatisation d’alertes pour les comptes à risque élevé.

## 4. Parties prenantes

- Direction de RavenStack : pilote la stratégie MRR et churn.  
- Équipe Customer Success : utilisatrice principale du score et du dashboard.  
- Équipe Data / projet (nous) : conception, modélisation, mise en place du système.

## 5. Critères de succès (mesurables)

1. *Performance modèle* : obtenir un modèle de churn avec une AUC ≥ 0,75 sur le jeu de test.  
2. *Impact métier* : réduire le churn mensuel d’au moins X % sur une période de test (à définir avec RavenStack).  
3. *Adoption* : avoir au moins Y utilisateurs actifs côté Customer Success qui consultent le dashboard chaque semaine.  
4. *Opérationnel* : déclenchement automatique d’alertes pour 100 % des comptes classés « risque élevé ».

## 6. Périmètre du Sprint 1

- Compréhension du contexte métier et du modèle économique SaaS B2B.  
- Mise en place de l’infrastructure (GitHub, GEMINI.md, orchetration d’agents IA).  
- Première exploration du dataset RavenStack et identification de signaux potentiels de churn.