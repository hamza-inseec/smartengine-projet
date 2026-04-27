# Rapport de Découverte du Dataset - Projet smartEngine

Ce rapport présente l'analyse descriptive initiale des données de RavenStack pour le Sprint 1. L'objectif est de comprendre la structure des fichiers et d'identifier les signaux pertinents pour la prédiction du churn.

## 1. Comptes Clients (`ravenstack_accounts.csv`)

*   **Dimensions** : 500 lignes, 10 colonnes.
*   **Schéma** :
    *   `account_id` : Identifiant unique (string)
    *   `account_name` : Nom de l'entreprise (string)
    *   `industry` : Secteur d'activité (EdTech, FinTech, etc.)
    *   `country` : Pays (US, UK, IN, etc.)
    *   `signup_date` : Date d'inscription
    *   `referral_source` : Source d'acquisition (partner, organic, etc.)
    *   `plan_tier` : Niveau de plan actuel (Basic, Enterprise)
    *   `seats` : Nombre de licences
    *   `is_trial` : Indicateur de période d'essai (bool)
    *   `churn_flag` : Indicateur historique de churn (bool)
*   **Aperçu** :
    ```csv
    account_id,account_name,industry,country,signup_date,referral_source,plan_tier,seats,is_trial,churn_flag
    A-2e4581,Company_0,EdTech,US,2024-10-16,partner,Basic,9,False,False
    A-43a9e3,Company_1,FinTech,IN,2023-08-17,other,Basic,18,False,True
    ```
*   **Qualité des données** : Pas de valeurs manquantes identifiées sur l'échantillon.
*   **Potentiel Prédictif** : Le `plan_tier` et le nombre de `seats` sont cruciaux. Les comptes avec beaucoup de licences ou sur des plans Enterprise pourraient avoir un comportement de churn différent des petits comptes.

## 2. Événements de Churn (`ravenstack_churn_events.csv`)

*   **Dimensions** : 600 lignes, 9 colonnes.
*   **Schéma** : Inclut `reason_code`, `refund_amount_usd`, `feedback_text`, etc.
*   **Aperçu** :
    ```csv
    churn_event_id,account_id,churn_date,reason_code,refund_amount_usd,preceding_upgrade_flag,preceding_downgrade_flag,is_reactivation,feedback_text
    C-816288,A-c37cab,2024-10-27,pricing,4.03,False,False,False,switched to competitor
    ```
*   **Qualité des données** : Présence de valeurs manquantes dans `feedback_text`.
*   **Potentiel Prédictif** : `reason_code` permet de comprendre pourquoi les clients partent (prix, support, budget), ce qui est vital pour segmenter le risque.

## 3. Utilisation des Fonctionnalités (`ravenstack_feature_usage.csv`)

*   **Dimensions** : 25 000 lignes, 8 colonnes.
*   **Schéma** : `usage_count`, `usage_duration_secs`, `error_count`, `feature_name`.
*   **Potentiel Prédictif** : Une baisse du `usage_count` ou une augmentation du `error_count` sont des signaux faibles (ou forts) de désengagement et de churn futur.

## 4. Abonnements (`ravenstack_subscriptions.csv`)

*   **Dimensions** : 5 000 lignes, 14 colonnes.
*   **Schéma** : `mrr_amount`, `arr_amount`, `billing_frequency`, `auto_renew_flag`.
*   **Aperçu** :
    ```csv
    subscription_id,account_id,start_date,end_date,plan_tier,seats,mrr_amount,arr_amount,is_trial,upgrade_flag,downgrade_flag,churn_flag,billing_frequency,auto_renew_flag
    S-8cec59,A-3c1a3f,2023-12-23,2024-04-12,Enterprise,14,2786,33432,False,False,False,True,monthly,True
    ```
*   **Qualité des données** : `end_date` est vide pour les abonnements actifs.
*   **Potentiel Prédictif** : L'indicateur `downgrade_flag` est un prédicteur de churn très probable. L'absence d'auto-renouvellement (`auto_renew_flag` = False) est également suspecte.

## 5. Tickets de Support (`ravenstack_support_tickets.csv`)

*   **Dimensions** : 2 000 lignes, 9 colonnes.
*   **Schéma** : `resolution_time_hours`, `priority`, `satisfaction_score`.
*   **Qualité des données** : `satisfaction_score` est souvent manquant si le client n'a pas répondu à l'enquête.
*   **Potentiel Prédictif** : Un `resolution_time_hours` élevé ou un faible `satisfaction_score` augmentent drastiquement le risque de churn.

## Conclusion

Le dataset est riche et bien structuré. Les données couvrent les dimensions démographiques (accounts), financières (subscriptions), comportementales (usage) et relationnelles (tickets). La prochaine étape consistera à nettoyer ces données et à fusionner ces différentes sources pour créer une table d'entraînement unique par `account_id`.
