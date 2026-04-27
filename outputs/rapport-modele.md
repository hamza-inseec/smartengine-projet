# Rapport de Modélisation Prédictive - smartEngine

## 1. Performance des Modèles

| Modèle | Accuracy | Precision | Recall | F1-Score | AUC-ROC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Logistic Regression | 0.680 | 0.779 | 0.757 | 0.768 | 0.670 |
| Random Forest | 0.670 | 0.718 | 0.871 | 0.787 | 0.620 |
| Gradient Boosting | 0.620 | 0.729 | 0.729 | 0.729 | 0.592 |

## 2. Matrices de Confusion

### Logistic Regression
```
[[15 15]
 [17 53]]
```
### Random Forest
```
[[ 6 24]
 [ 9 61]]
```
### Gradient Boosting
```
[[11 19]
 [19 51]]
```

## 3. Importance des Variables (Meilleur Modèle)

| Variable | Importance |
| :--- | :---: |
| anciennete_mois | 0.1651 |
| usage_total_count | 0.1081 |
| nb_sieges_max | 0.0797 |
| mrr_moyen | 0.0765 |
| tendance_usage | 0.0724 |
| delai_resolution_moyen | 0.0653 |
| usage_moyen_3mois | 0.0641 |
| nb_tickets_total | 0.0636 |
| nb_features_uniques | 0.0605 |
| jours_depuis_derniere_activite | 0.0554 |

## 4. Justification du Modèle Retenu

Le modèle **Random Forest** a été sélectionné pour la production car il présente le meilleur équilibre entre Précision et Rappel (F1-Score le plus élevé). Sa capacité à gérer les déséquilibres de classes via `class_weight='balanced'` et à capturer des relations non-linéaires le rend particulièrement robuste pour la prédiction du churn.