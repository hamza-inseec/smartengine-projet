import pandas as pd
import numpy as np
import joblib
import shap
from sklearn.metrics import recall_score, precision_score
from sklearn.model_selection import train_test_split

# 1. Chargement
df = pd.read_csv('data/processed/analytics.csv')
model = joblib.load('outputs/models/churn_model.joblib')
scaler = joblib.load('outputs/models/scaler.joblib')

# Préparation des données (identique à train_model.py)
df_model = df.drop(columns=['account_id'])
cat_cols = df_model.select_dtypes(include=['object']).columns.tolist()
df_encoded = pd.get_dummies(df_model, columns=cat_cols, drop_first=True)

X = df_encoded.drop(columns=['churn'])
y = df_encoded['churn']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

X_test_scaled = scaler.transform(X_test)

# --- SECTION 1: SHAP ---
explainer = shap.LinearExplainer(model, X_train)
shap_values = explainer.shap_values(X_test_scaled)
feature_importance = np.abs(shap_values).mean(0)
importance_df = pd.DataFrame({'feature': X.columns, 'importance': feature_importance})
top_5 = importance_df.sort_values('importance', ascending=False).head(5)

print("### SECTION 1: SHAP")
print(top_5)

# --- SECTION 2: BIAIS ---
y_pred = model.predict(X_test_scaled)

# On rajoute les infos de groupe au set de test
test_indices = X_test.index
df_test = df.loc[test_indices].copy()
df_test['y_true'] = y_test
df_test['y_pred'] = y_pred

def bias_report(group_col):
    report = []
    for val in df_test[group_col].unique():
        sub = df_test[df_test[group_col] == val]
        rec = recall_score(sub['y_true'], sub['y_pred'], zero_division=0)
        prec = precision_score(sub['y_true'], sub['y_pred'], zero_division=0)
        report.append({
            'group': val,
            'recall': rec,
            'precision': prec,
            'count': len(sub)
        })
    return pd.DataFrame(report)

industry_bias = bias_report('industry')
plan_bias = bias_report('est_enterprise')
# est_enterprise 1.0 = Enterprise, 0.0 = SMB
plan_bias['group'] = plan_bias['group'].map({1.0: 'Enterprise', 0.0: 'SMB'})

print("\n### SECTION 2: BIAIS")
print("Biais Industrie:")
print(industry_bias)
print("Biais Plan:")
print(plan_bias)

# --- SECTION 3: SEUILS ---
# On récupère les scores pour justifier
y_proba = model.predict_proba(X_test_scaled)[:, 1]
p50 = np.percentile(y_proba, 50)
p80 = np.percentile(y_proba, 80)
print(f"\n### SECTION 3: SEUILS\np50={p50:.4f}, p80={p80:.4f}")
