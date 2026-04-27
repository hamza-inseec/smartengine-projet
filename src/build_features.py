import pandas as pd
import numpy as np
import os
from datetime import datetime

# Chemins des fichiers
RAW_DIR = "data/raw/"
PROCESSED_DIR = "data/processed/"
OUTPUT_PATH = os.path.join(PROCESSED_DIR, "analytics.csv")

def load_data():
    """Charge les fichiers CSV nettoyés."""
    print("Chargement des données nettoyées...")
    try:
        accounts = pd.read_csv(os.path.join(PROCESSED_DIR, "ravenstack_accounts_clean.csv"))
        subscriptions = pd.read_csv(os.path.join(PROCESSED_DIR, "ravenstack_subscriptions_clean.csv"))
        usage = pd.read_csv(os.path.join(PROCESSED_DIR, "ravenstack_feature_usage_clean.csv"))
        tickets = pd.read_csv(os.path.join(PROCESSED_DIR, "ravenstack_support_tickets_clean.csv"))
        churn_events = pd.read_csv(os.path.join(PROCESSED_DIR, "ravenstack_churn_events_clean.csv"))
        
        # Conversion des dates
        accounts['signup_date'] = pd.to_datetime(accounts['signup_date'])
        subscriptions['start_date'] = pd.to_datetime(subscriptions['start_date'])
        subscriptions['end_date'] = pd.to_datetime(subscriptions['end_date'])
        usage['usage_date'] = pd.to_datetime(usage['usage_date'])
        tickets['submitted_at'] = pd.to_datetime(tickets['submitted_at'])
        churn_events['churn_date'] = pd.to_datetime(churn_events['churn_date'])
        
        return accounts, subscriptions, usage, tickets, churn_events
    except FileNotFoundError as e:
        print(f"Erreur : Fichier introuvable. {e}")
        exit(1)

def build_analytics():
    accounts, subscriptions, usage, tickets, churn_events = load_data()
    
    # 1. Définition de la cible Churn
    # On considère qu'un compte a churné s'il apparaît dans la table churn_events.
    # C'est la source de vérité pour les résiliations effectives.
    print("Définition de la cible churn...")
    churn_ids = churn_events['account_id'].unique()
    accounts['churn'] = accounts['account_id'].isin(churn_ids).astype(int)
    
    # Récupération de la date de churn pour filtrage (leakage)
    accounts = accounts.merge(churn_events[['account_id', 'churn_date']], on='account_id', how='left')
    
    # Date de référence pour le calcul de l'ancienneté (date du sprint ou max du dataset)
    # On prend la date la plus tardive observée dans les usages ou abonnements pour les non-churners
    ref_date = max(usage['usage_date'].max(), subscriptions['start_date'].max())
    print(f"Date de référence pour le dataset : {ref_date}")

    # 2. Gestion du Data Leakage
    # Pour les churners, on ne doit utiliser que les données ANTÉRIEURES au churn.
    # On crée une fonction de filtrage par compte.
    
    print("Application des filtres anti-leakage...")
    
    # Jointure pour avoir account_id dans l'usage
    usage = usage.merge(subscriptions[['subscription_id', 'account_id']], on='subscription_id', how='left')
    
    # Ajout de la churn_date aux tables temporelles
    usage = usage.merge(accounts[['account_id', 'churn_date']], on='account_id', how='left')
    tickets = tickets.merge(accounts[['account_id', 'churn_date']], on='account_id', how='left')
    subscriptions = subscriptions.merge(accounts[['account_id', 'churn_date']], on='account_id', how='left')
    
    # Filtrage : garder uniquement si date < churn_date (ou pas de churn_date)
    usage_filtered = usage[(usage['churn_date'].isna()) | (usage['usage_date'] < usage['churn_date'])].copy()
    tickets_filtered = tickets[(tickets['churn_date'].isna()) | (tickets['submitted_at'] < tickets['churn_date'])].copy()
    subs_filtered = subscriptions[(subscriptions['churn_date'].isna()) | (subscriptions['start_date'] < subscriptions['churn_date'])].copy()

    # 3. Calcul des Features
    print("Calcul des features...")
    
    # --- Features Temporelles ---
    # Ancienneté : Ref Date - Signup Date (ou Churn Date - Signup Date pour les churners ?)
    # Pour la modélisation, on veut savoir combien de temps ils sont restés avant de churner ou jusqu'à aujourd'hui.
    accounts['date_fin_obs'] = accounts['churn_date'].fillna(ref_date)
    accounts['anciennete_jours'] = (accounts['date_fin_obs'] - accounts['signup_date']).dt.days
    
    # --- Features Abonnement ---
    print("- Features abonnement...")
    sub_features = subs_filtered.groupby('account_id').agg(
        mrr_moyen=('mrr_amount', 'mean'),
        nb_sieges_max=('seats', 'max'),
        a_fait_un_downgrade=('downgrade_flag', lambda x: (x == True).sum())
    ).reset_index()
    
    # est_enterprise : si au moins un plan 'Enterprise'
    ent_accounts = subs_filtered[subs_filtered['plan_tier'] == 'Enterprise']['account_id'].unique()
    sub_features['est_enterprise'] = sub_features['account_id'].isin(ent_accounts).astype(int)
    
    # --- Features Support ---
    print("- Features support...")
    ticket_features = tickets_filtered.groupby('account_id').agg(
        nb_tickets_total=('ticket_id', 'count'),
        satisfaction_moyenne=('satisfaction_score', 'mean'),
        delai_resolution_moyen=('resolution_time_hours', 'mean')
    ).reset_index()
    
    # --- Features Usage ---
    print("- Features usage...")
    usage_features = usage_filtered.groupby('account_id').agg(
        usage_total_count=('usage_count', 'sum'),
        nb_features_uniques_utilisees=('feature_name', 'nunique'),
        nb_jours_activite=('usage_date', 'nunique')
    ).reset_index()
    
    # 4. Assemblage Final
    print("Assemblage de la table analytique...")
    df_final = accounts[['account_id', 'industry', 'country', 'anciennete_jours', 'churn']]
    
    df_final = df_final.merge(sub_features, on='account_id', how='left')
    df_final = df_final.merge(ticket_features, on='account_id', how='left')
    df_final = df_final.merge(usage_features, on='account_id', how='left')
    
    # Imputation des valeurs manquantes pour les comptes sans tickets ou sans usage
    df_final['nb_tickets_total'] = df_final['nb_tickets_total'].fillna(0)
    df_final['usage_total_count'] = df_final['usage_total_count'].fillna(0)
    df_final['nb_features_uniques_utilisees'] = df_final['nb_features_uniques_utilisees'].fillna(0)
    df_final['nb_jours_activite'] = df_final['nb_jours_activite'].fillna(0)
    df_final['a_fait_un_downgrade'] = df_final['a_fait_un_downgrade'].fillna(0)
    
    # Pour les scores et délais, on peut imputer par la médiane ou une valeur neutre
    df_final['satisfaction_moyenne'] = df_final['satisfaction_moyenne'].fillna(df_final['satisfaction_moyenne'].median())
    df_final['delai_resolution_moyen'] = df_final['delai_resolution_moyen'].fillna(df_final['delai_resolution_moyen'].median())
    df_final['mrr_moyen'] = df_final['mrr_moyen'].fillna(0)
    df_final['nb_sieges_max'] = df_final['nb_sieges_max'].fillna(0)
    df_final['est_enterprise'] = df_final['est_enterprise'].fillna(0)

    # 5. Vérification de cohérence
    print(f"Nombre de lignes final : {len(df_final)}")
    print(f"Taux de churn : {df_final['churn'].mean():.2%}")
    
    # Sauvegarde
    df_final.to_csv(OUTPUT_PATH, index=False)
    print(f"Table analytique sauvegardée dans {OUTPUT_PATH}")

if __name__ == "__main__":
    build_analytics()
