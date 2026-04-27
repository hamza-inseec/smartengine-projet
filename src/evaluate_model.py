import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score, 
                             roc_auc_score, confusion_matrix, classification_report)

try:
    import lightgbm as lgb
    LGBM_AVAILABLE = True
except ImportError:
    LGBM_AVAILABLE = False
    print("Avertissement : LightGBM n'est pas installé. Ce modèle sera ignoré.")

def evaluate_models():
    # 1. Chargement
    df = pd.read_csv('data/processed/analytics.csv')
    
    # 2. Préparation
    X = df.drop(columns=['account_id', 'churn'])
    y = df['churn']
    
    # Encodage
    X = pd.get_dummies(X, drop_first=True)
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    
    # 3. Initialisation des modèles
    models = {
        "Logistic Regression": LogisticRegression(class_weight='balanced', random_state=42, max_iter=2000),
        "Random Forest": RandomForestClassifier(class_weight='balanced', random_state=42)
    }
    
    if LGBM_AVAILABLE:
        models["LightGBM"] = lgb.LGBMClassifier(is_unbalance=True, random_state=42, verbose=-1)
    
    results = []
    
    # 4. Évaluation
    print("\n" + "="*60)
    print("ÉVALUATION DES MODÈLES DE CHURN")
    print("="*60)
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]
        
        metrics = {
            "Modèle": name,
            "Accuracy": accuracy_score(y_test, y_pred),
            "Precision": precision_score(y_test, y_pred),
            "Recall (Churn)": recall_score(y_test, y_pred),
            "F1-score": f1_score(y_test, y_pred),
            "AUC-ROC": roc_auc_score(y_test, y_proba)
        }
        results.append(metrics)
        
        print(f"\n[+] {name}")
        print(f"Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}")
        print(f"Classification Report:\n{classification_report(y_test, y_pred)}")

    # 5. Comparaison finale
    df_results = pd.DataFrame(results).sort_values(by="Recall (Churn)", ascending=False)
    print("\n" + "="*60)
    print("TABLEAU RÉCAPITULATIF DES PERFORMANCES")
    print("="*60)
    print(df_results.to_string(index=False))

if __name__ == "__main__":
    evaluate_models()
