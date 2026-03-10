# Veille outils – smartEngine

## Gemini CLI
- Présentation :
  Gemini CLI est un outil en ligne de commande qui permet d’interagir avec un agent IA capable de lire, créer et modifier des fichiers directement dans un projet local.

- Rôle dans le projet :
  Il sert d’« assistant développeur » pour générer le code Python, explorer les données, produire des rapports et mettre à jour les fichiers du projet smartEngine sans écrire soi‑même tout le code.

- Avantages :
  Automatisation des tâches répétitives, gain de temps pour générer du code et des rapports, intégration directe avec la structure du projet via GEMINI.md et les agents, collaboration facilitée dans une équipe non experte en développement.

- Limites :
  Nécessite un environnement technique bien configuré (Node, droits sur les fichiers), peut faire des erreurs si les instructions sont floues, pas de mémoire persistante en dehors de GEMINI.md, dépendance à une connexion internet et au service d’IA.

- Alternatives :
  Utiliser un IDE avec copilote intégré (VS Code + GitHub Copilot), passer par une interface web de type ChatGPT pour générer du code à copier‑coller, ou coder manuellement sans IA.

- Sources :
  Documentation officielle Gemini CLI, guide d’orchestration d’agents fourni dans le kit de projet.


## Python et pandas

- Présentation :
  Python est un langage de programmation très utilisé en data science ; pandas est sa bibliothèque principale pour manipuler des tableaux de données (datasets tabulaires).

- Rôle dans le projet :
  Ils servent à charger les fichiers CSV RavenStack, nettoyer les données, créer des variables dérivées et préparer les jeux de données qui seront utilisés pour le modèle de churn.

- Avantages :
  Écosystème riche pour la data, syntaxe relativement simple, pandas est très efficace pour filtrer, agréger, fusionner des tables et faire des calculs statistiques de base.

- Limites :
  Peut devenir lent ou gourmand en mémoire sur de très gros volumes, la courbe d’apprentissage peut être un peu longue pour les débutants, nécessite une bonne discipline de structuration du code.

- Alternatives :
  R ou SQL pour certaines analyses, outils no‑code comme Power BI ou Tableau pour l’exploration, bibliothèques Python plus spécialisées (Polars) pour optimiser les performances.

- Sources :
  Documentation officielle Python et pandas, ressources de cours de data science.


## scikit-learn

- Présentation :
  scikit-learn est une bibliothèque Python de machine learning qui propose de nombreux algorithmes supervisés et non supervisés ainsi que des outils d’évaluation et de validation.

- Rôle dans le projet :
  Elle sera utilisée pour entraîner le modèle de scoring de churn (classification) à partir des données préparées, choisir les algorithmes, ajuster les hyperparamètres et mesurer les performances.

- Avantages :
  Interface unifiée pour beaucoup de modèles, bonne documentation, largement utilisée en entreprise et en enseignement, intégration naturelle avec pandas et NumPy.

- Limites :
  Moins adaptée aux très grands volumes ou au deep learning, ne gère pas directement le déploiement en production, nécessite une bonne compréhension des concepts de machine learning pour interpréter les résultats.

- Alternatives :
  XGBoost, LightGBM ou CatBoost pour des modèles de gradient boosting, TensorFlow ou PyTorch pour du deep learning, AutoML comme Auto‑sklearn ou H2O pour automatiser une partie de la modélisation.

- Sources :
  Documentation officielle scikit-learn, tutoriels de machine learning classiques.


## Streamlit

- Présentation :
  Streamlit est un framework Python qui permet de créer facilement des applications web interactives à partir de scripts data, sans avoir besoin de maîtriser les technologies front‑end.

- Rôle dans le projet :
  Il servira à construire le dashboard interactif smartEngine pour visualiser le score de churn, filtrer les comptes et mettre l’outil à disposition de l’équipe Customer Success.

- Avantages :
  Mise en place rapide, syntaxe simple basée sur Python, rafraîchissement interactif des graphiques et des tableaux, bon pour des prototypes data orientés métier.

- Limites :
  Moins flexible qu’un développement web complet, limité pour des interfaces très complexes ou très customisées, peut être moins performant pour un très grand nombre d’utilisateurs en production.

- Alternatives :
  Dash (Plotly), Shiny (R), frameworks web traditionnels comme Django ou Flask + front‑end, solutions BI comme Power BI ou Looker Studio.

- Sources :
  Documentation officielle Streamlit, exemples d’applications de data science.


## n8n

- Présentation :
  n8n est un outil d’automatisation de workflows open source qui permet de connecter des services entre eux et de créer des scénarios sans beaucoup de code.

- Rôle dans le projet :
  Il peut être utilisé pour automatiser les alertes de churn (par exemple envoyer un email ou créer une tâche dans un CRM quand un compte dépasse un certain score de risque).

- Avantages :
  Interface visuelle en drag‑and‑drop, grand nombre d’intégrations possibles, auto‑hébergeable, flexible pour orchestrer des actions entre plusieurs outils.

- Limites :
  Demande une infrastructure pour être hébergé et maintenu, la complexité des workflows peut augmenter vite, certaines intégrations avancées nécessitent un peu de scripting.

- Alternatives :
  Zapier, Make (ex‑Integromat), outils d’automatisation intégrés aux CRM, scripts maison en Python ou Node.js.

- Sources :
  Documentation officielle n8n, exemples de scénarios d’automatisation marketing.


## GitHub

- Présentation :
  GitHub est une plateforme de gestion de code source basée sur Git, qui permet d’héberger des dépôts, suivre les versions et collaborer en équipe.

- Rôle dans le projet :
  C’est le point central du projet smartEngine : tout le code, les agents, les notebooks, les rapports et le dossier de conception y sont versionnés, avec une branche par membre et une branche main stable.

- Avantages :
  Historique complet des modifications, travail en branches, Pull Requests pour valider les changements, intégration avec de nombreux outils (CI/CD, documentation, gestion de projet).

- Limites :
  Nécessite une discipline dans l’utilisation des branches et des commits, la gestion de conflits peut être difficile pour les débutants, dépendance à une plateforme externe.

- Alternatives :
  GitLab, Bitbucket, ou l’hébergement Git sur un serveur interne pour des organisations qui ne veulent pas utiliser un service cloud public.

- Sources :
  Documentation GitHub, mémo Git fourni pour le projet.

