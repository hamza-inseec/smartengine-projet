# Rapport de Modélisation Churn - smartEngine

## 1. Synthèse de la Performance
Le modèle sélectionné pour la mise en production est le **Random Forest**, choisi pour sa capacité supérieure à détecter les clients à risque (Recall).

| Modèle | Accuracy | Precision | Recall (Churn) | F1-score | AUC-ROC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Random Forest** | 0.64 | 0.70 | **0.84** | 0.77 | 0.63 |
| Logistic Regression | 0.67 | 0.77 | 0.76 | 0.76 | 0.66 |

*Note : LightGBM n'a pas été testé dans cet environnement faute de bibliothèque installée.*

## 2. Préparation des Données et Stratégie
- **Découpage** : 80% Entraînement / 20% Test avec stratification sur la cible.
- **Gestion du déséquilibre** : Utilisation du paramètre `class_weight='balanced'`. Cette stratégie est privilégiée pour pénaliser plus fortement les erreurs sur la classe minoritaire (churners) sans supprimer d'informations (contrairement à l'undersampling).
- **Encodage** : Transformation des variables `industry` et `country` via LabelEncoding/OneHotEncoding.

## 3. Interprétation du Modèle (Feature Importances)
Les 5 variables les plus prédictives du churn sont :
1. **anciennete_mois** (15.3%) : Plus un client est récent, plus le risque est élevé.
2. **usage_total_count** (9.3%) : Un faible volume d'activité globale est un signal fort.
3. **mrr_moyen** (8.7%) : Le montant de l'abonnement influence la propension à résilier.
4. **nb_sieges_max** (7.9%) : La taille du compte au sein de RavenStack.
5. **usage_moyen_3mois** (6.8%) : La régularité de l'usage récent.

## 4. Analyse des Biais et Équité
L'analyse du Recall par sous-groupe montre une performance homogène :
- **Par Industrie** : Le modèle détecte les churners avec une efficacité constante (Recall ~1.00 sur le set complet) à travers la Cybersecurity, FinTech, EdTech, etc.
- **Par Type de Plan** : Aucune différence significative de détection n'est observée entre les comptes **Enterprise** et **Standard**.

## 5. Scoring et Recommandations Opérationnelles
Les scores ont été générés pour les 500 comptes dans `outputs/scores.csv` avec les seuils suivants :
- **High Risk (> 0.7)** : 349 comptes. Nécessitent une intervention immédiate du Customer Success.
- **Medium Risk (0.4 - 0.7)** : 4 comptes. À surveiller lors des prochains points trimestriels.
- **Low Risk (< 0.4)** : 147 comptes. Clients stables.

Le modèle est sauvegardé dans `outputs/models/churn_model.joblib`.
