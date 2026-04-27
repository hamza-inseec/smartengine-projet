import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.preprocessing import StandardScaler
import joblib

# 1. Chargement des données
print("Chargement des données...")
df = pd.read_csv('data/processed/analytics.csv')

# 2. Prétraitement
if 'account_id' in df.columns:
    df = df.drop(columns=['account_id'])

# Identification des colonnes catégorielles
cat_cols = df.select_dtypes(include=['object']).columns.tolist()
print(f"Colonnes catégorielles : {cat_cols}")

# Application de pd.get_dummies
df_encoded = pd.get_dummies(df, columns=cat_cols, drop_first=True)

# 3. Séparation X et y
X = df_encoded.drop(columns=['churn'])
y = df_encoded['churn']

# 4. Split train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# 5. Normalisation (StandardScaler)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("Normalisation appliquée.")

# 6. Entraînement des modèles
models = {
    "Logistic Regression": LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42),
    "Random Forest": RandomForestClassifier(class_weight='balanced', random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42)
}

best_model = None
best_auc = -1
best_name = ""

print("\nEntraînement et évaluation (AUC-ROC)...")
sample_weights = compute_sample_weight(class_weight='balanced', y=y_train)

for name, model in models.items():
    if name == "Gradient Boosting":
        model.fit(X_train_scaled, y_train, sample_weight=sample_weights)
    else:
        model.fit(X_train_scaled, y_train)
    
    y_proba = model.predict_proba(X_test_scaled)[:, 1]
    score = roc_auc_score(y_test, y_proba)
    print(f"- {name} : AUC-ROC = {score:.4f}")
    
    if score > best_auc:
        best_auc = score
        best_model = model
        best_name = name

# 7. Sauvegarde
os.makedirs('outputs/models', exist_ok=True)
joblib.dump(best_model, 'outputs/models/churn_model.joblib')
# On sauvegarde aussi le scaler car il est nécessaire pour le scoring futur
joblib.dump(scaler, 'outputs/models/scaler.joblib')

print(f"\nMeilleur modèle : {best_name} avec un AUC-ROC de {best_auc:.4f}")
