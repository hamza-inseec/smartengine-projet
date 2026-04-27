import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# Configuration des chemins
PROCESSED_DIR = "data/processed/"
OUTPUT_PATH = os.path.join(PROCESSED_DIR, "analytics.csv")

def load_cleaned_data():
    """Charge les fichiers CSV nettoyés depuis data/processed/."""
    print("Chargement des fichiers nettoyés...")
    try:
        files = {
            'accounts': 'ravenstack_accounts_clean.csv',
            'subscriptions': 'ravenstack_subscriptions_clean.csv',
            'usage': 'ravenstack_feature_usage_clean.csv',
            'tickets': 'ravenstack_support_tickets_clean.csv',
            'churn': 'ravenstack_churn_events_clean.csv'
        }
        
        dfs = {}
        for key, filename in files.items():
            path = os.path.join(PROCESSED_DIR, filename)
            if not os.path.exists(path):
                raise FileNotFoundError(f"Fichier manquant : {path}")
            dfs[key] = pd.read_csv(path)
            
        # Conversion systématique des dates
        date_cols = {
            'accounts': ['signup_date'],
            'subscriptions': ['start_date', 'end_date'],
            'usage': ['usage_date'],
            'tickets': ['submitted_at', 'closed_at'],
            'churn': ['churn_date']
        }
        
        for df_key, cols in date_cols.items():
            for col in cols:
                if col in dfs[df_key].columns:
                    dfs[df_key][col] = pd.to_datetime(dfs[df_key][col])
                    
        return dfs
    except Exception as e:
        print(f"Erreur lors du chargement : {e}")
        exit(1)

def build_analytics():
    """Construit la table analytique finale au niveau account_id."""
    dfs = load_cleaned_data()
    
    accounts = dfs['accounts']
    subscriptions = dfs['subscriptions']
    usage = dfs['usage']
    tickets = dfs['tickets']
    churn_events = dfs['churn']
    
    print("Initialisation de la table analytique...")
    
    # 1. Cible Churn
    churn_ids = churn_events['account_id'].unique()
    accounts['churn'] = accounts['account_id'].isin(churn_ids).astype(int)
    
    # Récupération de la date de churn pour filtrage anti-leakage
    accounts = accounts.merge(churn_events[['account_id', 'churn_date']], on='account_id', how='left')
    
    # Date de référence globale (lendemain de la dernière activité enregistrée)
    max_date = max(usage['usage_date'].max(), subscriptions['start_date'].max())
    ref_date = max_date + timedelta(days=1)
    print(f"Date de référence : {ref_date.date()}")

    # 2. Préparation des données avec filtrage anti-leakage
    # Pour chaque compte, on ne garde que les données strictement antérieures à sa date de churn (si applicable)
    
    # Lien usage -> account_id via subscriptions
    usage = usage.merge(subscriptions[['subscription_id', 'account_id']], on='subscription_id', how='left')
    
    # Ajout churn_date aux tables transactionnelles
    usage = usage.merge(accounts[['account_id', 'churn_date']], on='account_id', how='left')
    tickets = tickets.merge(accounts[['account_id', 'churn_date']], on='account_id', how='left')
    subscriptions = subscriptions.merge(accounts[['account_id', 'churn_date']], on='account_id', how='left')

    # Filtrage
    usage_f = usage[(usage['churn_date'].isna()) | (usage['usage_date'] < usage['churn_date'])].copy()
    tickets_f = tickets[(tickets['churn_date'].isna()) | (tickets['submitted_at'] < tickets['churn_date'])].copy()
    subs_f = subscriptions[(subscriptions['churn_date'].isna()) | (subscriptions['start_date'] < subscriptions['churn_date'])].copy()

    # 3. Calcul des Features
    
    # --- Features Temporelles ---
    print("Calcul des features temporelles...")
    # Ancienneté
    accounts['obs_end_date'] = accounts['churn_date'].fillna(ref_date)
    accounts['anciennete_mois'] = ((accounts['obs_end_date'] - accounts['signup_date']).dt.days / 30.44).round(1)
    
    # --- Features Abonnement & Financier ---
    print("Calcul des features abonnement...")
    # Nombre de changements de plan (upgrades + downgrades)
    # On convertit les booléens en int pour la somme
    subs_f['upgrade_int'] = subs_f['upgrade_flag'].astype(int)
    subs_f['downgrade_int'] = subs_f['downgrade_flag'].astype(int)
    
    sub_agg = subs_f.groupby('account_id').agg(
        nb_changements_plan=('upgrade_int', 'sum'), # Somme simplifiée
        mrr_moyen=('mrr_amount', 'mean'),
        nb_sieges_max=('seats', 'max'),
        downgrade_detecte=('downgrade_int', 'max')
    )
    # Correction : nb_changements_plan est la somme des deux types
    sub_agg['nb_changements_plan'] = subs_f.groupby('account_id')[['upgrade_int', 'downgrade_int']].sum().sum(axis=1)
    
    # Dernières infos (auto_renew_flag, plan actuel)
    last_subs = subs_f.sort_values('start_date').groupby('account_id').last()[['auto_renew_flag', 'plan_tier']]
    sub_agg = sub_agg.join(last_subs)
    sub_agg['auto_renew_flag'] = sub_agg['auto_renew_flag'].astype(int)
    sub_agg['est_enterprise'] = (sub_agg['plan_tier'] == 'Enterprise').astype(int)

    # --- Features Support ---
    print("Calcul des features support...")
    tickets_f['is_urgent'] = tickets_f['priority'].isin(['urgent', 'high']).astype(int)
    
    ticket_agg = tickets_f.groupby('account_id').agg(
        nb_tickets_total=('ticket_id', 'count'),
        nb_tickets_critiques=('is_urgent', 'sum'),
        satisfaction_moyenne=('satisfaction_score', 'mean'),
        delai_resolution_moyen=('resolution_time_hours', 'mean')
    )
    ticket_agg['ratio_tickets_critiques'] = (ticket_agg['nb_tickets_critiques'] / ticket_agg['nb_tickets_total']).fillna(0)

    # --- Features Usage ---
    print("Calcul des features usage...")
    
    # Usage total et diversité
    usage_agg = usage_f.groupby('account_id').agg(
        usage_total_count=('usage_count', 'sum'),
        nb_features_uniques=('feature_name', 'nunique'),
        derniere_activite=('usage_date', 'max')
    )
    
    # Jours depuis dernière activité
    usage_agg = usage_agg.merge(accounts[['account_id', 'obs_end_date']], on='account_id', how='left').set_index('account_id')
    usage_agg['jours_depuis_derniere_activite'] = (usage_agg['obs_end_date'] - usage_agg['derniere_activite']).dt.days
    
    # Usage moyen 3 derniers mois et Tendance
    # Pour simplifier et éviter des boucles lentes, on calcule l'usage par mois relatif à la fin d'observation
    usage_f = usage_f.merge(accounts[['account_id', 'obs_end_date']], on='account_id', how='left')
    usage_f['mois_relatif'] = ((usage_f['obs_end_date'] - usage_f['usage_date']).dt.days // 30)
    
    # Usage moyen sur les 3 derniers mois (mois_relatif 0, 1, 2)
    u3m = usage_f[usage_f['mois_relatif'] < 3].groupby(['account_id', 'mois_relatif'])['usage_count'].sum().unstack(fill_value=0)
    # S'assurer que les colonnes 0, 1, 2 existent
    for m in [0, 1, 2]:
        if m not in u3m.columns: u3m[m] = 0
    
    usage_agg['usage_moyen_3mois'] = u3m[[0, 1, 2]].mean(axis=1)
    
    # Tendance : usage(m=0) - usage(m=2) / 2 (pente simplifiée)
    # Si positif : l'usage augmente (plus d'usage au mois 0 qu'au mois 2)
    # On veut : usage récent - usage ancien
    usage_agg['tendance_usage'] = (u3m[0] - u3m[2]) / 2

    # 4. Assemblage final
    print("Assemblage final...")
    analytics = accounts[['account_id', 'industry', 'country', 'anciennete_mois', 'churn']].copy()
    
    analytics = analytics.merge(sub_agg.drop(columns=['plan_tier']), on='account_id', how='left')
    analytics = analytics.merge(ticket_agg, on='account_id', how='left')
    analytics = analytics.merge(usage_agg[['usage_total_count', 'nb_features_uniques', 'jours_depuis_derniere_activite', 'usage_moyen_3mois', 'tendance_usage']], on='account_id', how='left')

    # Imputation des valeurs manquantes
    fill_zeros = ['nb_changements_plan', 'nb_tickets_total', 'nb_tickets_critiques', 
                  'ratio_tickets_critiques', 'usage_total_count', 'nb_features_uniques',
                  'usage_moyen_3mois', 'tendance_usage', 'downgrade_detecte', 'auto_renew_flag', 'est_enterprise']
    analytics[fill_zeros] = analytics[fill_zeros].fillna(0)
    
    # Imputation par la médiane pour les métriques de qualité
    analytics['satisfaction_moyenne'] = analytics['satisfaction_moyenne'].fillna(analytics['satisfaction_moyenne'].median())
    analytics['delai_resolution_moyen'] = analytics['delai_resolution_moyen'].fillna(analytics['delai_resolution_moyen'].median())
    
    # Pour les comptes sans activité, on met un max de jours
    analytics['jours_depuis_derniere_activite'] = analytics['jours_depuis_derniere_activite'].fillna(analytics['anciennete_mois'] * 30)
    analytics['mrr_moyen'] = analytics['mrr_moyen'].fillna(0)
    analytics['nb_sieges_max'] = analytics['nb_sieges_max'].fillna(0)

    # 5. Sauvegarde
    print(f"Sauvegarde de {len(analytics)} lignes dans {OUTPUT_PATH}...")
    analytics.to_csv(OUTPUT_PATH, index=False)
    
    print("Statistiques de la table produite :")
    print(f"- Taux de churn : {analytics['churn'].mean():.2%}")
    print(f"- Usage moyen : {analytics['usage_total_count'].mean():.1f}")
    print(f"- Ancienneté moyenne : {analytics['anciennete_mois'].mean():.1f} mois")
    print("Terminé !")

if __name__ == "__main__":
    build_analytics()
