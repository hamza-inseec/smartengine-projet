import pandas as pd
import numpy as np

# 1. Chargement
df = pd.read_csv('outputs/scores.csv')
scores = df['churn_score']

# 2. Histogramme en texte
print("Distribution des churn_score (par tranches de 0.1) :")
bins = np.arange(0, 1.1, 0.1)
counts, _ = np.histogram(scores, bins=bins)
for i in range(len(counts)):
    bar = '*' * (counts[i] // 2)  # Echelle réduite pour affichage CLI
    print(f"{bins[i]:.1f} - {bins[i+1]:.1f} | {counts[i]:4d} | {bar}")

# 3. Calcul des percentiles
p50 = np.percentile(scores, 50)
p80 = np.percentile(scores, 80)
print(f"\nSeuils calculés :")
print(f"- 50ème percentile (Low/Medium) : {p50:.4f}")
print(f"- 80ème percentile (Medium/High) : {p80:.4f}")

# 4. Mise à jour des risk_level
def assign_risk(score):
    if score >= p80:
        return 'high'
    elif score >= p50:
        return 'medium'
    else:
        return 'low'

df['risk_level'] = df['churn_score'].apply(assign_risk)

# 5. Comptage et sauvegarde
counts_new = df['risk_level'].value_counts()
print("\nNouveau comptage des niveaux de risque :")
for level in ['high', 'medium', 'low']:
    print(f"- {level}: {counts_new.get(level, 0)}")

df.to_csv('outputs/scores.csv', index=False)
print("\nFichier outputs/scores.csv mis à jour.")
