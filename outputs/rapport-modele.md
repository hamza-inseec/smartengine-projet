# Rapport de Modélisation Prédictive - smartEngine

## 1. Performance des Modèles (Mis à jour)

Suite à l'ajout de la normalisation (`StandardScaler`) et de l'encodage des variables catégorielles, voici les nouvelles performances basées sur l'AUC-ROC :

| Modèle | AUC-ROC |
| :--- | :---: |
| **Logistic Regression** | **0.6619** |
| Random Forest | 0.6314 |
| Gradient Boosting | 0.6086 |

## 2. Analyse SHAP (Interprétabilité)

L'analyse SHAP (SHapley Additive exPlanations) permet de comprendre l'impact de chaque variable sur la prédiction individuelle du risque de churn pour la Régression Logistique.

| Variable | Importance SHAP | Sens Métier pour RavenStack |
| :--- | :--- | :--- |
| **usage_total_count** | 360.51 | L'activité globale est le premier indicateur. Une baisse radicale signale un abandon progressif de l'outil. |
| **mrr_moyen** | 35.44 | Les comptes à MRR élevé sont plus stables, mais leur départ serait plus coûteux. |
| **usage_moyen_3mois** | 6.90 | Reflète l'engagement récent. Une déconnexion entre l'usage historique et récent est critique. |
| **anciennete_mois** | 5.33 | Les nouveaux clients sont plus fragiles (risque de "early churn"). |
| **nb_features_uniques** | 4.59 | Un client qui utilise peu de fonctionnalités différentes perçoit moins la valeur de la plateforme. |

## 3. Analyse de Biais

Nous avons audité les performances du modèle sur différents segments pour garantir l'équité des alertes.

### Par Industrie
- **FinTech** : Recall = **53.3%** ⚠️ (Le modèle manque près de la moitié des churners dans ce secteur).
- **Cybersecurity / EdTech / DevTools** : Recall > 80% (Excellente détection).
- **HealthTech** : Recall = 71.4%.

### Par Type de Plan
- **SMB** (est_enterprise=0) : Recall = 78.8%
- **Enterprise** (est_enterprise=1) : Recall = **55.5%** ⚠️

**Note :** Le modèle est moins performant sur les gros comptes (Enterprise) et le secteur FinTech. Une collecte de données spécifiques à ces segments (ex: feedback qualitatif) est recommandée.

## 4. Justification des Seuils de Risque

Les scores de probabilité (0 à 1) ont été segmentés en trois catégories basées sur la distribution observée (Percentiles 50 et 80) :

| Niveau | Seuil (Score) | Signification Métier | Action Recommandée |
| :--- | :--- | :--- | :--- |
| **High** | >= 0.95 | Risque Critique | Action immédiate du CSM (appel direct, offre de rétention). |
| **Medium** | 0.86 - 0.95 | Surveillance | Envoi d'un email automatisé ou check-up de santé du compte. |
| **Low** | < 0.86 | Stable | Compte sain. Continuer les rituels de succès habituels. |

Ces seuils garantissent que l'équipe CSM concentre ses efforts sur les 20% de comptes les plus à risque (Top 20% = High Risk).

## 5. Conclusion

Le modèle de **Régression Logistique** avec normalisation est retenu pour la phase pilote. Malgré un AUC-ROC modéré (0.66), il offre une interprétabilité claire via SHAP et permet de prioriser efficacement les interventions.
