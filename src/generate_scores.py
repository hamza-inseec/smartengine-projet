import pandas as pd
import joblib
import os

# 1. Chargement du modèle et des données
print("Chargement du modèle et des données...")
model = joblib.load('outputs/models/churn_model.joblib')
df = pd.read_csv('data/processed/analytics.csv')

# 2. Préparation des features (doit être identique à l'entraînement)
# On récupère les colonnes numériques et on retire la cible 'churn'
X = df.select_dtypes(include=['number']).drop(columns=['churn'])

# 3. Prédiction des scores (probabilités)
print("Génération des scores...")
# predict_proba renvoie [prob_0, prob_1], on prend prob_1
scores = model.predict_proba(X)[:, 1]

# 4. Création du DataFrame de sortie
results = pd.DataFrame({
    'account_id': df['account_id'],
    'churn_score': scores
})

# 5. Définition des niveaux de risque
def categorize_risk(score):
    if score > 0.7:
        return "high"
    elif score >= 0.4:
        return "medium"
    else:
        return "low"

results['risk_level'] = results['churn_score'].apply(categorize_risk)

# 6. Sauvegarde
output_path = 'outputs/scores.csv'
results.to_csv(output_path, index=False)

print(f"Fichier de scores généré : {output_path}")
print("\nDistribution des niveaux de risque :")
print(results['risk_level'].value_counts())
