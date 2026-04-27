# Section 3 : Modélisation et Évaluation

Cette section détaille la conception, l'entraînement et la validation du modèle prédictif de churn pour RavenStack.

## 3.1 Approche et Algorithmes
L'objectif métier étant de minimiser les faux négatifs (clients qui partent sans être détectés), nous avons privilégié des algorithmes capables de gérer le déséquilibre des classes et de fournir des probabilités de sortie.

Les algorithmes suivants ont été évalués :
*   **Régression Logistique** : Modèle de référence (baseline) pour sa simplicité et son interprétabilité.
*   **Random Forest** : Modèle d'ensemble robuste aux valeurs aberrantes et capable de capturer les relations non-linéaires.

## 3.2 Protocole d'Entraînement
*   **Split Train/Test** : 80% pour l'entraînement et 20% pour le test, avec une stratification sur la variable cible `churn` pour préserver le ratio initial.
*   **Gestion du déséquilibre** : Le dataset présentant une classe minoritaire (churn), nous avons appliqué la stratégie `class_weight='balanced'`. Cela permet de donner un poids plus important aux cas de churn lors de l'apprentissage sans perdre d'échantillons de la classe majoritaire.
*   **Reproductibilité** : Utilisation d'un `random_state=42` pour garantir la stabilité des résultats.

## 3.3 Performances du Modèle
Le modèle **Random Forest** a été sélectionné comme modèle final en raison de son **Recall élevé (0.84)** sur la classe churners.

| Métrique | Random Forest | Logistic Regression |
| :--- | :--- | :--- |
| **Recall (Classe 1)** | **0.84** | 0.76 |
| Accuracy | 0.64 | 0.67 |
| Precision | 0.70 | 0.77 |
| F1-score | 0.77 | 0.76 |
| AUC-ROC | 0.63 | 0.66 |

## 3.4 Interprétation et Facteurs de Risque
L'analyse de l'importance des variables (Feature Importances) révèle les leviers principaux de résiliation :
1.  **Ancienneté (15.3%)** : Les clients récents sont les plus fragiles.
2.  **Activité Globale (9.3%)** : Une chute du volume d'actions total est un précurseur fiable du départ.
3.  **MRR Moyen (8.7%)** : Les variations de revenus mensuels impactent la fidélité.
4.  **Nombre de Sièges (7.9%)** : Les petits comptes semblent plus volatiles.

## 3.5 Analyse d'Équité et Biais
Nous avons validé que le modèle ne présente pas de biais discriminatoires :
*   **Industrie** : Le taux de détection (Recall) est homogène entre les secteurs (Cybersecurity, FinTech, etc.).
*   **Type de Compte** : Le modèle performe de manière équitable sur les comptes **Standard** et **Enterprise**, garantissant que les clients premium ne sont pas sous-évalués.

## 3.6 Scoring et Seuils Métier
Le modèle génère un `churn_score` (probabilité de 0 à 1) traduit en trois niveaux d'alerte pour les équipes Customer Success :
*   **Élevé (score > 0.7)** : Alerte rouge, action corrective immédiate requise.
*   **Modéré (0.4 - 0.7)** : Surveillance accrue et prise de contact lors de la prochaine revue.
*   **Faible (score < 0.4)** : Client considéré comme stable.
