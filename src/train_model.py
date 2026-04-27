import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import f1_score
from sklearn.utils.class_weight import compute_sample_weight
import joblib

# 1. Chargement des données
print("Chargement des données...")
df = pd.read_csv('data/processed/analytics.csv')

# 2. Séparation X et y
# On exclut account_id (identifiant) et country/industry (catégoriques pour cet exemple simple)
# Dans un vrai projet, on les encoderait. Ici on se concentre sur les numériques pour le MVP.
X = df.select_dtypes(include=['number']).drop(columns=['churn'])
y = df['churn']

# 3. Split train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# 4. Ratio churn dans le train set
ratio = y_train.value_counts(normalize=True)
print(f"\nDistribution du churn dans l'ensemble d'entraînement :\n{ratio}")
print(f"Nombre d'exemples : {len(y_train)}")

# 5. Entraînement des modèles
models = {
    "Logistic Regression": LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42),
    "Random Forest": RandomForestClassifier(class_weight='balanced', random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42)
}

best_model = None
best_f1 = -1
best_name = ""

print("\nEntraînement et évaluation (F1-Score)...")

# Poids pour Gradient Boosting (car il n'a pas class_weight)
sample_weights = compute_sample_weight(class_weight='balanced', y=y_train)

for name, model in models.items():
    if name == "Gradient Boosting":
        model.fit(X_train, y_train, sample_weight=sample_weights)
    else:
        model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    score = f1_score(y_test, y_pred)
    print(f"- {name} : F1-Score = {score:.4f}")
    
    if score > best_f1:
        best_f1 = score
        best_model = model
        best_name = name

# 6. Sauvegarde du meilleur modèle
os.makedirs('outputs/models', exist_ok=True)
model_path = 'outputs/models/churn_model.joblib'
joblib.dump(best_model, model_path)

print(f"\nMeilleur modèle : {best_name} avec un F1-Score de {best_f1:.4f}")
print(f"Modèle sauvegardé dans {model_path}")
