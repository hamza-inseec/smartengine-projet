# Rapport de Nettoyage des Données - Projet smartEngine

Ce rapport détaille l'audit de qualité effectué sur les 5 fichiers de données brutes de RavenStack.

## 1. Analyse par fichier

### ravenstack_accounts.csv (Comptes clients)
| Problème | Volume | Stratégie de correction | Justification | Résultat attendu |
|---|---|---|---|---|
| Aucun problème majeur | 0 | Aucune | Données propres et complètes | Table de référence prête |

### ravenstack_subscriptions.csv (Abonnements)
| Problème | Volume | Stratégie de correction | Justification | Résultat attendu |
|---|---|---|---|---|
| `end_date` manquants | 4514 | Remplacer par la date du jour | Signifie que l'abonnement est actif | Calcul d'ancienneté possible |
| Format des dates | 5000 | Conversion en `datetime` | Format actuel est `string` | Calculs temporels activés |

### ravenstack_churn_events.csv (Résiliations)
| Problème | Volume | Stratégie de correction | Justification | Résultat attendu |
|---|---|---|---|---|
| `feedback_text` manquants | 148 | Remplacer par "Non fourni" | Donnée textuelle optionnelle | Analyse de sentiment possible |
| Multiples churns par compte | 175 comptes | Identifier le churn le plus récent | Gestion des réactivations | Cible binaire (0/1) cohérente |
| Format des dates | 600 | Conversion en `datetime` | Format actuel est `string` | Alignement chronologique |

### ravenstack_support_tickets.csv (Support)
| Problème | Volume | Stratégie de correction | Justification | Résultat attendu |
|---|---|---|---|---|
| `satisfaction_score` manquants | 825 | Imputer par la médiane | Absence de réponse du client | Variable numérique complète |
| Format des dates | 2000 | Conversion en `datetime` | Format actuel est `string` | Calcul des délais de résolution |

### ravenstack_feature_usage.csv (Usage)
| Problème | Volume | Stratégie de correction | Justification | Résultat attendu |
|---|---|---|---|---|
| Absence d' `account_id` direct | 25000 | Joindre via `subscription_id` | L'usage est lié à l'abonnement | Agrégation par compte possible |
| Format des dates | 25000 | Conversion en `datetime` | Fo


rmat actuel est `string` | Analyse de tendance temporelle |

## 2. Bilan global de la qualité

La qualité des données de RavenStack est jugée **satisfaisante** pour la construction du modèle de prédiction du churn.

**Points forts :**
- Intégrité référentielle : 100% des `account_id` et `subscription_id` sont cohérents entre les fichiers.
- Absence de doublons : Aucun doublon exact n'a été détecté dans les fichiers.
- Plage de données : Couvre une période cohérente de 2 ans (2023-2024).

**Points d'attention :**
- **Churn et Réactivations** : 175 comptes présentent plusieurs événements de churn. Il faudra définir une règle métier claire pour la table analytique (ex: considérer le statut au dernier jour connu).
- **Données manquantes** : Le taux important de scores de satisfaction manquants (41%) nécessite une imputation prudente pour ne pas biaiser le modèle.
- **Activité récente** : L'utilisation de la date du jour pour combler les `end_date` vides est cruciale pour le calcul de la feature `anciennete`.

**Conclusion :** Les données sont prêtes à être nettoyées et transformées via les scripts `src/clean_data.py` et `src/build_analytics.py`.
