import pandas as pd
import os
from datetime import datetime

# Configuration des chemins
RAW_DIR = "/Users/wafaabenkorreche/Documents/smartengine-projet/data/raw"
PROCESSED_DIR = "/Users/wafaabenkorreche/Documents/smartengine-projet/data/processed"

def ensure_directories():
    """Crée le dossier processed s'il n'existe pas."""
    if not os.path.exists(PROCESSED_DIR):
        os.makedirs(PROCESSED_DIR)
        print(f"Dossier créé : {PROCESSED_DIR}")

def clean_accounts():
    """Nettoie le fichier des comptes."""
    file_path = os.path.join(RAW_DIR, "ravenstack_accounts.csv")
    if not os.path.exists(file_path):
        print(f"Erreur : {file_path} introuvable.")
        return
    
    df = pd.read_csv(file_path)
    # Conversion des dates
    df['signup_date'] = pd.to_datetime(df['signup_date'])
    
    # Sauvegarde
    output_path = os.path.join(PROCESSED_DIR, "ravenstack_accounts_clean.csv")
    df.to_csv(output_path, index=False)
    print(f"Comptes nettoyés : {len(df)} lignes.")

def clean_subscriptions():
    """Nettoie le fichier des abonnements."""
    file_path = os.path.join(RAW_DIR, "ravenstack_subscriptions.csv")
    if not os.path.exists(file_path):
        print(f"Erreur : {file_path} introuvable.")
        return
    
    df = pd.read_csv(file_path)
    
    # Conversion des dates
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    
    # Imputation de end_date : si vide, l'abonnement est actif. On utilise la date du jour.
    today = pd.Timestamp.now().normalize()
    df['end_date'] = df['end_date'].fillna(today)
    
    # Sauvegarde
    output_path = os.path.join(PROCESSED_DIR, "ravenstack_subscriptions_clean.csv")
    df.to_csv(output_path, index=False)
    print(f"Abonnements nettoyés : {len(df)} lignes.")

def clean_churn_events():
    """Nettoie le fichier des événements de résiliation."""
    file_path = os.path.join(RAW_DIR, "ravenstack_churn_events.csv")
    if not os.path.exists(file_path):
        print(f"Erreur : {file_path} introuvable.")
        return
    
    df = pd.read_csv(file_path)
    
    # Conversion des dates
    df['churn_date'] = pd.to_datetime(df['churn_date'])
    
    # Imputation feedback_text
    df['feedback_text'] = df['feedback_text'].fillna("Non fourni")
    
    # Gestion des multi-churns : on garde le plus récent par compte
    df = df.sort_values(by=['account_id', 'churn_date'], ascending=[True, False])
    df = df.drop_duplicates(subset=['account_id'], keep='first')
    
    # Sauvegarde
    output_path = os.path.join(PROCESSED_DIR, "ravenstack_churn_events_clean.csv")
    df.to_csv(output_path, index=False)
    print(f"Événements de churn nettoyés : {len(df)} lignes.")

def clean_support_tickets():
    """Nettoie le fichier des tickets de support."""
    file_path = os.path.join(RAW_DIR, "ravenstack_support_tickets.csv")
    if not os.path.exists(file_path):
        print(f"Erreur : {file_path} introuvable.")
        return
    
    df = pd.read_csv(file_path)
    
    # Conversion des dates
    df['submitted_at'] = pd.to_datetime(df['submitted_at'])
    df['closed_at'] = pd.to_datetime(df['closed_at'])
    
    # Imputation satisfaction_score par la médiane
    median_score = df['satisfaction_score'].median()
    df['satisfaction_score'] = df['satisfaction_score'].fillna(median_score)
    
    # Sauvegarde
    output_path = os.path.join(PROCESSED_DIR, "ravenstack_support_tickets_clean.csv")
    df.to_csv(output_path, index=False)
    print(f"Tickets de support nettoyés : {len(df)} lignes.")

def clean_feature_usage():
    """Nettoie le fichier d'utilisation des fonctionnalités."""
    file_path = os.path.join(RAW_DIR, "ravenstack_feature_usage.csv")
    if not os.path.exists(file_path):
        print(f"Erreur : {file_path} introuvable.")
        return
    
    df = pd.read_csv(file_path)
    
    # Conversion des dates
    df['usage_date'] = pd.to_datetime(df['usage_date'])
    
    # Sauvegarde
    output_path = os.path.join(PROCESSED_DIR, "ravenstack_feature_usage_clean.csv")
    df.to_csv(output_path, index=False)
    print(f"Usage fonctionnalités nettoyé : {len(df)} lignes.")

def main():
    print("Début du nettoyage des données...")
    ensure_directories()
    clean_accounts()
    clean_subscriptions()
    clean_churn_events()
    clean_support_tickets()
    clean_feature_usage()
    print("Nettoyage terminé avec succès.")

if __name__ == "__main__":
    main()
