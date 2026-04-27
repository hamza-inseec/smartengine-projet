import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, recall_score

def train_churn_model():
    # 1. Chargement des données
    data_path = 'data/processed/analytics.csv'
    print(f"Chargement des données depuis {data_path}...")
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {data_path} est introuvable.")
        return

    # 2. Préparation des données
    # Séparation X et y (account_id n'est pas une feature)
    if 'account_id' not in df.columns or 'churn' not in df.columns:
        print("Erreur : Les colonnes 'account_id' ou 'churn' sont manquantes.")
        return
        
    X = df.drop(columns=['account_id', 'churn'])
    y = df['churn']

    # Gestion des variables catégorielles (ex: industry, country)
    categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
    if categorical_cols:
        print(f"Variables catégorielles détectées : {categorical_cols}")
        X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)

    # Split Train/Test (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=42
    )

    # 3. Analyse du ratio de churn
    def print_ratio(y_series, label):
        counts = y_series.value_counts(normalize=True)
        ratio = counts.get(1, 0) * 100
        print(f"Ratio de Churn ({label}) : {ratio:.2f}% (Total: {len(y_series)})")

    print("\n--- Analyse du déséquilibre des classes ---")
    print_ratio(y, "Ensemble complet")
    print_ratio(y_train, "Train set")
    print_ratio(y_test, "Test set")

    # 4. Modélisation
    models = {
        "Régression Logistique": LogisticRegression(
            class_weight='balanced', 
            random_state=42, 
            max_iter=2000
        ),
        "Random Forest": RandomForestClassifier(
            class_weight='balanced', 
            random_state=42, 
            n_estimators=100
        )
    }

    # 5. Évaluation
    print("\n--- Résultats de la Modélisation ---")
    for name, model in models.items():
        print(f"\n" + "="*50)
        print(f"Modèle : {name}")
        print("="*50)
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        print("\nRapport de classification :")
        print(classification_report(y_test, y_pred, target_names=['Fidèle (0)', 'Churn (1)']))
        
        print("Matrice de Confusion :")
        print(confusion_matrix(y_test, y_pred))
        
        # Critère de sélection principal : Recall sur la classe 1
        rec = recall_score(y_test, y_pred)
        print(f"\nCRITÈRE CLÉ - Recall (Classe 1) : {rec:.4f}")

if __name__ == "__main__":
    train_churn_model()
