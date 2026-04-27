# Rapport de Nettoyage des Données - Projet smartEngine

Ce rapport détaille l'audit de qualité effectué sur les 5 fichiers de données brutes de RavenStack.

## 1. Analyse par fichier

### ravenstack_accounts.csv (Comptes clients)
| Problème | Volume | Stratégie de correction | Justification | Résultat attendu |
|---|---|---|---|---|
| Aucun problème majeur | 0 | Aucune | Données propres et complètes | Table de référence prête |

### ravenstack_subscriptions.csv (Abonnements)
| Problème | Volume | Stratégie de correction | Justification | Résultat attendu |
|---|---|---|---|---|
| `end_date` manquants | 4514 | Remplacer par la date du jour | Signifie que l'abonnement est actif | Calcul d'ancienneté possible |
| Format des dates | 5000 | Conversion en `datetime` | Format actuel est `string` | Calculs temporels activés |

### ravenstack_churn_events.csv (Résiliations)
| Problème | Volume | Stratégie de correction | Justification | Résultat attendu |
|---|---|---|---|---|
| `feedback_text` manquants | 148 | Remplacer par "Non fourni" | Donnée textuelle optionnelle | Analyse de sentiment possible |
| Multiples churns par compte | 175 comptes | Identifier le churn le plus récent | Gestion des réactivations | Cible binaire (0/1) cohérente |
| Format des dates | 600 | Conversion en `datetime` | Format actuel est `string` | Alignement chronologique |

### ravenstack_support_tickets.csv (Support)
| Problème | Volume | Stratégie de correction | Justification | Résultat attendu |
|---|---|---|---|---|
| `satisfaction_score` manquants | 825 | Imputer par la médiane | Absence de réponse du client | Variable numérique complète |
| Format des dates | 2000 | Conversion en `datetime` | Format actuel est `string` | Calcul des délais de résolution |

### ravenstack_feature_usage.csv (Usage)
| Problème | Volume | Stratégie de correction | Justification | Résultat attendu |
|---|---|---|---|---|
| Absence d' `account_id` direct | 25000 | Joindre via `subscription_id` | L'usage est lié à l'abonnement | Agrégation par compte possible |
| Format des dates | 25000 | Conversion en `datetime` | Fo


rmat actuel est `string` | Analyse de tendance temporelle |

## 2. Bilan global de la qualité

La qualité des données de RavenStack est jugée **satisfaisante** pour la construction du modèle de prédiction du churn.

**Points forts :**
- Intégrité référentielle : 100% des `account_id` et `subscription_id` sont cohérents entre les fichiers.
- Absence de doublons : Aucun doublon exact n'a été détecté dans les fichiers.
- Plage de données : Couvre une période cohérente de 2 ans (2023-2024).

**Points d'attention :**
- **Churn et Réactivations** : 175 comptes présentent plusieurs événements de churn. Il faudra définir une règle métier claire pour la table analytique (ex: considérer le statut au dernier jour connu).
- **Données manquantes** : Le taux important de scores de satisfaction manquants (41%) nécessite une imputation prudente pour ne pas biaiser le modèle.
- **Activité récente** : L'utilisation de la date du jour pour combler les `end_date` vides est cruciale pour le calcul de la feature `anciennete`.

**Conclusion :** Les données sont prêtes à être nettoyées et transformées via les scripts `src/clean_data.py` et `src/build_analytics.py`.

## 3. Variable cible : justification de la source

Le choix et la construction de la variable cible (`churn`) sont des étapes critiques pour la performance du modèle prédictif. Voici les justifications méthodologiques retenues :

### Justification de la source de données
Le fichier `ravenstack_churn_events.csv` a été privilégié comme source unique pour définir le churn. Contrairement à une approche basée sur l'inactivité (via `feature_usage.csv`), le churn renseigné ici correspond à un **acte explicite de résiliation**. L'inactivité peut être temporaire, saisonnière ou liée à une baisse d'usage ponctuelle, tandis que l'événement de churn confirme la fin de la relation commerciale.

### Logique de construction
La variable cible est construite selon la règle suivante :
*   **`churn = 1`** : L'identifiant du compte (`account_id`) est présent dans le fichier des événements de résiliation.
*   **`churn = 0`** : Le compte est toujours actif ou n'a aucun événement de résiliation enregistré.

Pour les **175 comptes** présentant des événements de churn multiples (réactivations suivies d'une nouvelle résiliation), seul l'événement le plus récent a été conservé. Cette approche permet de capturer l'état final du compte et d'aligner les prédicteurs sur la situation la plus actuelle.

### Choix du format binaire
Nous avons opté pour une variable binaire (0/1). C'est le format standard et optimal pour un problème de **classification supervisée** dans un contexte SaaS B2B. Cela permet d'utiliser une large gamme d'algorithmes (Régression Logistique, Random Forest, XGBoost) pour prédire la probabilité d'un événement discret.

### Prévention du data leakage
Afin d'éviter toute fuite de données (data leakage), une attention particulière a été portée à la temporalité. Pour tous les comptes ayant churné, nous nous assurons que les caractéristiques d'usage, de support et d'abonnement sont calculées sur une période **strictement antérieure** à la date de résiliation (`churn_date`). Cela garantit que le modèle apprend à prédire le churn à partir de signaux précurseurs et non de conséquences de la résiliation.

### Statistiques de la variable cible
Basé sur la table analytique finale `data/processed/analytics.csv`, la répartition est la suivante :

*   **Comptes avec churn (`churn=1`)** : 352 (70.40 %)
*   **Comptes sans churn (`churn=0`)** : 148 (29.60 %)

Cette répartition montre un déséquilibre en faveur des comptes ayant churné dans cet échantillon, ce qui devra être pris en compte lors de l'entraînement du modèle (via des techniques de rééquilibrage ou le choix de métriques adaptées comme le F1-score).
