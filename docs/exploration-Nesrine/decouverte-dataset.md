# Découverte du Dataset - SmartEngine

Ce document résume l'exploration approfondie des fichiers de données fournis pour le projet de prédiction du churn RavenStack, réalisée par l'agent Data-explorer.

## 1. Comptes Clients (`ravenstack_accounts.csv`)

*   **Nombre de lignes :** 500
*   **Nombre de colonnes :** 10
*   **Colonnes clés :**
    *   `account_id` (str) : Identifiant unique du compte.
    *   `industry` (str) : Secteur d'activité (5 secteurs uniques).
    *   `plan_tier` (str) : Niveau d'abonnement (Basic, Pro, Enterprise).
    *   `seats` (int64) : Nombre de licences.
    *   `is_trial` (bool) : Indicateur de période d'essai.
    *   `churn_flag` (bool) : Variable cible (vrai si le client a churné).
*   **Qualité des données :** 100% de complétude sur toutes les colonnes. Aucune valeur manquante.
*   **Colonnes utiles pour prédire le churn :**
    *   `industry` : Certains secteurs (ex: FinTech vs EdTech) peuvent avoir des comportements de rétention différents.
    *   `plan_tier` et `seats` : Reflètent l'engagement financier et la taille de l'organisation.
    *   `is_trial` : Les comptes en essai ont une probabilité de churn structurellement plus élevée.
    *   `signup_date` : Permet de calculer l'ancienneté du compte.

## 2. Événements de Churn (`ravenstack_churn_events.csv`)

*   **Nombre de lignes :** 600
*   **Nombre de colonnes :** 9
*   **Colonnes clés :**
    *   `reason_code` (str) : Motif du départ (pricing, support, budget, etc.).
    *   `refund_amount_usd` (float64) : Montant remboursé.
    *   `preceding_downgrade_flag` (bool) : Indique si un downgrade a eu lieu avant le churn.
    *   `feedback_text` (str) : Commentaire textuel du client.
*   **Qualité des données :** 24,67% de valeurs manquantes pour `feedback_text`, ce qui est attendu pour un champ de commentaire libre. Les autres colonnes sont complètes.
*   **Colonnes utiles pour prédire le churn :**
    *   `reason_code` : Analyse historique des causes de départ pour identifier les points de douleur récurrents.
    *   `preceding_downgrade_flag` : Un signal d'alerte fort ; les clients qui réduisent leur voilure sont souvent sur le point de partir.
    *   `refund_amount_usd` : Peut indiquer une insatisfaction majeure (demande de remboursement).

## 3. Utilisation des Fonctionnalités (`ravenstack_feature_usage.csv`)

*   **Nombre de lignes :** 25 000
*   **Nombre de colonnes :** 8
*   **Colonnes clés :**
    *   `feature_name` (str) : Nom de la fonctionnalité utilisée (40 fonctionnalités différentes).
    *   `usage_count` (int64) : Nombre d'utilisations.
    *   `usage_duration_secs` (int64) : Temps passé sur la fonctionnalité.
    *   `error_count` (int64) : Nombre d'erreurs rencontrées.
    *   `is_beta_feature` (bool) : Utilisation de fonctionnalités en bêta.
*   **Qualité des données :** Excellente complétude (0% de valeurs manquantes).
*   **Colonnes utiles pour prédire le churn :**
    *   `usage_count` / `usage_duration_secs` : La baisse tendancielle de l'usage est le meilleur indicateur avancé du churn.
    *   `error_count` : Un utilisateur qui rencontre des erreurs répétées est un candidat sérieux au churn par frustration.
    *   `is_beta_feature` : L'adoption précoce de nouvelles fonctionnalités peut être un signe de fort engagement.

## 4. Abonnements (`ravenstack_subscriptions.csv`)

*   **Nombre de lignes :** 5 000
*   **Nombre de colonnes :** 14
*   **Colonnes clés :**
    *   `mrr_amount` (int64) : Revenu mensuel récurrent.
    *   `billing_frequency` (str) : mensuel ou annuel.
    *   `auto_renew_flag` (bool) : Renouvellement automatique actif ou non.
    *   `upgrade_flag` / `downgrade_flag` : Historique des changements de plan.
*   **Qualité des données :** 90,28% de valeurs manquantes pour `end_date`, ce qui est normal car cela correspond aux abonnements toujours actifs.
*   **Colonnes utiles pour prédire le churn :**
    *   `auto_renew_flag` : Les clients désactivant le renouvellement automatique expriment une intention de départ probable.
    *   `billing_frequency` : Les contrats annuels offrent une meilleure stabilité que les contrats mensuels.
    *   `downgrade_flag` : Transition vers un plan inférieur, souvent précurseur du churn.

## 5. Tickets de Support (`ravenstack_support_tickets.csv`)

*   **Nombre de lignes :** 2 000
*   **Nombre de colonnes :** 9
*   **Colonnes clés :**
    *   `priority` (str) : Urgence du ticket (low, medium, high, urgent).
    *   `resolution_time_hours` (float64) : Temps de résolution.
    *   `satisfaction_score` (float64) : Note donnée par le client (1 à 5).
    *   `escalation_flag` (bool) : Si le ticket a été escaladé.
*   **Qualité des données :** 41,25% de valeurs manquantes pour `satisfaction_score`. C'est un point de vigilance : peu de clients notent leur support.
*   **Colonnes utiles pour prédire le churn :**
    *   `satisfaction_score` : Un score faible (1 ou 2) est un signal critique immédiat.
    *   `resolution_time_hours` : Un support lent dégrade la relation client.
    *   `escalation_flag` : Reflète des problèmes complexes ou persistants.
    *   `priority` : Un volume élevé de tickets "urgent" ou "high" indique une dépendance critique avec des frictions potentielles.
