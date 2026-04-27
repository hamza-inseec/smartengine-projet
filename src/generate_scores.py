import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import recall_score
import joblib
import os

def main():
    # 1. Charge data/processed/analytics.csv
    file_path = '/Users/wafaabenkorreche/Documents/smartengine-projet/data/processed/analytics.csv'
    if not os.path.exists(file_path):
        print(f"Erreur : Le fichier {file_path} est introuvable.")
        return
        
    df = pd.read_csv(file_path)

    # 2. Prépare les données
    # Garde une copie pour l'analyse finale et de biais
    df_analysis = df[['account_id', 'industry', 'est_enterprise', 'churn']].copy()

    # Features et Target
    X = df.drop(columns=['account_id', 'churn'])
    y = df['churn']

    # Encodage des variables catégorielles (industry, country)
    # On utilise LabelEncoder pour simplifier, comme demandé
    categorical_cols = X.select_dtypes(include=['object']).columns
    le_dict = {}
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        le_dict[col] = le

    # 3. Entraîne le meilleur modèle
    # Random Forest avec class_weight='balanced' pour gérer le déséquilibre des classes
    model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    model.fit(X, y)

    # 4. Sauvegarde le modèle
    model_dir = '/Users/wafaabenkorreche/Documents/smartengine-projet/outputs/models'
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'churn_model.joblib')
    joblib.dump(model, model_path)

    # 5. Calcule et affiche les Feature Importances (Top 10)
    importances = model.feature_importances_
    feature_names = X.columns
    feature_importance_df = pd.DataFrame({'feature': feature_names, 'importance': importances})
    feature_importance_df = feature_importance_df.sort_values(by='importance', ascending=False)
    
    print("\n--- Top 10 Feature Importances ---")
    print(feature_importance_df.head(10).to_string(index=False))

    # 6. Analyse les biais
    # On utilise les prédictions sur le même dataset pour l'analyse demandée
    y_pred = model.predict(X)
    df_analysis['prediction'] = y_pred

    print("\n--- Analyse des Biais (Recall moyen) ---")
    
    # Par industry
    recall_industry = df_analysis.groupby('industry').apply(
        lambda x: recall_score(x['churn'], x['prediction'], zero_division=0)
    )
    print("\nRecall par Industry :")
    for ind, rec in recall_industry.items():
        print(f"  - {ind}: {rec:.2f}")

    # Par est_enterprise (0: Plan Standard, 1: Plan Enterprise)
    recall_enterprise = df_analysis.groupby('est_enterprise').apply(
        lambda x: recall_score(x['churn'], x['prediction'], zero_division=0)
    )
    print("\nRecall par Type de Compte (0=Standard, 1=Enterprise) :")
    for ent, rec in recall_enterprise.items():
        label = "Enterprise" if ent == 1.0 else "Standard"
        print(f"  - {label}: {rec:.2f}")

    # 7. Génère les scores pour TOUS les comptes
    probs = model.predict_proba(X)[:, 1]
    df_analysis['churn_score'] = probs

    def get_risk_level(score):
        if score > 0.7:
            return 'High'
        elif score >= 0.4:
            return 'Medium'
        else:
            return 'Low'

    df_analysis['risk_level'] = df_analysis['churn_score'].apply(get_risk_level)

    # 8. Exporte le résultat final
    output_path = '/Users/wafaabenkorreche/Documents/smartengine-projet/outputs/scores.csv'
    df_analysis[['account_id', 'churn_score', 'risk_level']].to_csv(output_path, index=False)

    # 9. Résumé
    print("\n--- Résumé de l'exécution ---")
    print(f"Modèle entraîné et sauvegardé dans 'outputs/models/churn_model.joblib'.")
    print(f"Scores générés pour {len(df_analysis)} comptes et sauvegardés dans 'outputs/scores.csv'.")
    print(f"\nRépartition des niveaux de risque :")
    counts = df_analysis['risk_level'].value_counts()
    for level, count in counts.items():
        print(f"  - {level}: {count}")

if __name__ == "__main__":
    main()
