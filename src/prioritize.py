import pandas as pd

# Chargement des fichiers
scores = pd.read_csv("outputs/scores.csv")
analytics = pd.read_csv("data/processed/analytics.csv")

# Fusion sur account_id
df = scores.merge(analytics[["account_id", "mrr_moyen"]], on="account_id", how="left")
df.rename(columns={"mrr_moyen": "MRR"}, inplace=True)

# Seuil de valeur : médiane du MRR
mrr_median = df["MRR"].median()
print(f"Médiane MRR : {mrr_median:.2f}")

# Définition des quadrants
def get_quadrant(row):
    high_risk = row["churn_score"] >= 0.5
    high_value = row["MRR"] >= mrr_median

    if high_risk and high_value:
        return "Q1 - Priorité maximale"
    elif high_risk and not high_value:
        return "Q2 - Action automatisée"
    elif not high_risk and high_value:
        return "Q3 - Surveiller"
    else:
        return "Q4 - Stable"

# Actions recommandées par quadrant
def get_action(quadrant):
    actions = {
        "Q1 - Priorité maximale": "Appel CSM immédiat sous 24h",
        "Q2 - Action automatisée": "Email automatisé de relance",
        "Q3 - Surveiller":        "Suivi mensuel, offre fidélisation",
        "Q4 - Stable":            "Aucune action prioritaire"
    }
    return actions[quadrant]

df["quadrant"] = df.apply(get_quadrant, axis=1)
df["action_recommandee"] = df["quadrant"].apply(get_action)

# Sauvegarde
output_cols = ["account_id", "churn_score", "risk_level", "MRR", "quadrant", "action_recommandee"]
df[output_cols].to_csv("outputs/priorisation.csv", index=False)

print("✅ priorisation.csv généré")
print(df["quadrant"].value_counts())