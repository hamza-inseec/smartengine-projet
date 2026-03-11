# Veille Outils - Projet smartEngine (Sprint 1)

Ce document présente les outils technologiques retenus pour la conception et le déploiement de **smartEngine**, notre solution de prédiction du churn pour RavenStack.

---

## 1. Gemini CLI
*   **Présentation** : Une interface en ligne de commande (CLI) qui permet d'interagir avec l'intelligence artificielle Gemini directement dans le terminal.
*   **Rôle dans le projet** : Assistant de développement principal pour coder, corriger des erreurs, automatiser des tâches et structurer le projet.
*   **Avantages** : Gain de temps massif, aide à la rédaction de documentation, suggestions de code pertinentes.
*   **Limites** : Nécessite une connexion internet ; peut parfois faire des erreurs de logique (hallucinations).
*   **Alternatives** : GitHub Copilot, ChatGPT, Claude.

## 2. Python / pandas
*   **Présentation** : Python est le langage de programmation leader en Data Science, et **pandas** est sa bibliothèque phare pour manipuler des tableaux de données.
*   **Rôle dans le projet** : Chargement, nettoyage et analyse exploratoire des données de RavenStack (logs d'utilisation, facturation).
*   **Avantages** : Très puissant pour manipuler de gros fichiers CSV/Excel ; immense communauté d'utilisateurs.
*   **Limites** : Peut être lent sur des volumes de données extrêmement massifs (plusieurs giga-octets).
*   **Alternatives** : Langage R, SQL, Excel (pour des analyses très basiques).

## 3. scikit-learn
*   **Présentation** : La bibliothèque Python de référence pour l'apprentissage automatique (Machine Learning) classique.
*   **Rôle dans le projet** : Création et entraînement du modèle de prédiction du churn (algorithmes de classification).
*   **Avantages** : Simple d'utilisation, très bien documenté, inclut tous les outils pour évaluer la performance.
*   **Limites** : Non adapté pour le "Deep Learning" (images, sons complexes).
*   **Alternatives** : XGBoost, TensorFlow, PyTorch.

## 4. Streamlit
*   **Présentation** : Un framework Python qui permet de transformer des scripts de données en applications web interactives en quelques minutes.
*   **Rôle dans le projet** : Création du tableau de bord (Dashboard) pour l'équipe Customer Success de RavenStack.
*   **Avantages** : Pas besoin de connaître le HTML/CSS/JS ; rendu professionnel immédiat.
*   **Limites** : Moins flexible qu'un site web classique pour des fonctionnalités très complexes.
*   **Alternatives** : Plotly Dash, Flask, Shiny (pour R).

## 5. n8n
*   **Présentation** : Un outil d'automatisation de workflow (flux de travail) de type "Low-Code".
*   **Rôle dans le projet** : Connecter le modèle smartEngine à des outils tiers (envoyer une alerte Slack ou un email quand un risque de churn est détecté).
*   **Avantages** : Interface visuelle simple ; s'installe facilement sur un serveur.
*   **Limites** : Demande un peu d'apprentissage pour les automatisations avancées.
*   **Alternatives** : Zapier, Make (ex-Integromat), Pipedream.

## 6. GitHub
*   **Présentation** : Plateforme de collaboration et d'hébergement de code utilisant le logiciel de versioning Git.
*   **Rôle dans le projet** : Sauvegarde du code, gestion des versions et travail d'équipe sur la branche `hamza-inseec`.
*   **Avantages** : Indispensable pour ne jamais perdre son travail ; permet de revenir en arrière en cas d'erreur.
*   **Limites** : La prise en main des commandes "Git" peut être intimidante au début.
*   **Alternatives** : GitLab, Bitbucket.
