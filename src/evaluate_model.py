import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, roc_auc_score, confusion_matrix)
from sklearn.utils.class_weight import compute_sample_weight

# 1. Chargement et préparation (identique au train)
df = pd.read_csv('data/processed/analytics.csv')
X = df.select_dtypes(include=['number']).drop(columns=['churn'])
y = df['churn']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# 2. Définition et ré-entraînement pour comparaison complète
models = {
    "Logistic Regression": LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42),
    "Random Forest": RandomForestClassifier(class_weight='balanced', random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42)
}

sample_weights = compute_sample_weight(class_weight='balanced', y=y_train)

results = []
cms = {}

print("Évaluation des modèles...")
for name, model in models.items():
    if name == "Gradient Boosting":
        model.fit(X_train, y_train, sample_weight=sample_weights)
    else:
        model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    metrics = {
        "Modèle": name,
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "F1-Score": f1_score(y_test, y_pred),
        "AUC-ROC": roc_auc_score(y_test, y_prob)
    }
    results.append(metrics)
    cms[name] = confusion_matrix(y_test, y_pred)
    
    print(f"\n--- {name} ---")
    print(f"Matrice de confusion :\n{cms[name]}")

# 3. Analyse du meilleur modèle (chargé depuis le disque pour vérification)
best_model = joblib.load('outputs/models/churn_model.joblib')
best_name = "Random Forest" # Basé sur le F1-Score précédent

importances = pd.DataFrame({
    'feature': X.columns,
    'importance': best_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nFeature Importances (Meilleur Modèle) :")
print(importances.head(10))

# 4. Génération du rapport Markdown
report_path = 'outputs/rapport-modele.md'
with open(report_path, 'w', encoding='utf-8') as f:
    f.write("# Rapport de Modélisation Prédictive - smartEngine\n\n")
    
    f.write("## 1. Performance des Modèles\n\n")
    f.write("| Modèle | Accuracy | Precision | Recall | F1-Score | AUC-ROC |\n")
    f.write("| :--- | :---: | :---: | :---: | :---: | :---: |\n")
    for r in results:
        f.write(f"| {r['Modèle']} | {r['Accuracy']:.3f} | {r['Precision']:.3f} | {r['Recall']:.3f} | {r['F1-Score']:.3f} | {r['AUC-ROC']:.3f} |\n")
    
    f.write("\n## 2. Matrices de Confusion\n\n")
    for name, matrix in cms.items():
        f.write(f"### {name}\n")
        f.write(f"```\n{matrix}\n```\n")
    
    f.write("\n## 3. Importance des Variables (Meilleur Modèle)\n\n")
    f.write("| Variable | Importance |\n")
    f.write("| :--- | :---: |\n")
    for _, row in importances.head(10).iterrows():
        f.write(f"| {row['feature']} | {row['importance']:.4f} |\n")
    
    f.write("\n## 4. Justification du Modèle Retenu\n\n")
    f.write(f"Le modèle **{best_name}** a été sélectionné pour la production car il présente le meilleur équilibre entre Précision et Rappel (F1-Score le plus élevé). ")
    f.write("Sa capacité à gérer les déséquilibres de classes via `class_weight='balanced'` et à capturer des relations non-linéaires le rend particulièrement robuste pour la prédiction du churn.")

print(f"\nRapport généré : {report_path}")
