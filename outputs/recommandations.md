cat > outputs/recommandations.md << 'EOF'
# Recommandations et mesure d'impact
## Projet smartEngine – RavenStack

---

## 1. Ce que dit le modèle

Le modèle prédit un taux de churn de **73.8%** sur les 500 comptes analysés.
Les 3 facteurs principaux qui augmentent le risque de churn sont :
- Une faible ancienneté (comptes récents plus volatils)
- Un nombre élevé de tickets critiques (insatisfaction)
- Une baisse d'usage sur les 3 derniers mois (désengagement)

---

## 2. Actions par quadrant

| Quadrant | Profil | Action | Responsable |
|----------|--------|--------|-------------|
| Q1 – Priorité maximale (177 comptes) | Gros comptes à risque élevé | Appel CSM sous 24h, offre de fidélisation personnalisée | Customer Success Manager |
| Q2 – Action automatisée (192 comptes) | Petits comptes à risque élevé | Email automatisé de relance, accès formation offert | Marketing automation |
| Q3 – Surveiller (73 comptes) | Gros comptes fidèles | Suivi mensuel, programme de fidélisation | Account Manager |
| Q4 – Stable (58 comptes) | Petits comptes stables | Aucune action prioritaire | — |

---

## 3. ROI estimé

### Coût actuel du churn
- MRR total à risque : **782 568 €**
- Si 30% des comptes Q1 churne : perte estimée ~**70 000 €/mois**

### Gain potentiel
- En retenant 40% des comptes Q1 (71 comptes) : **+28 000 €/mois** de MRR sauvé
- En retenant 20% des comptes Q2 (38 comptes) : **+8 000 €/mois**

### Coût des actions
- Appels CSM Q1 : ~50€/compte × 177 = **8 850 €**
- Emails automatisés Q2 : ~2€/compte × 192 = **384 €**
- **ROI estimé : x3 à x4 sur 3 mois**

---

## 4. Feuille de route

### Phase 1 – Pilote (mois 1)
- Déployer le dashboard auprès de 2 CSM
- Traiter uniquement les comptes Q1 (177 comptes)
- Mesurer le taux de rétention après 30 jours

### Phase 2 – Élargissement (mois 2)
- Intégrer Q2 avec emails automatisés
- Former l'équipe Customer Success au dashboard
- Ajuster les seuils si nécessaire

### Phase 3 – Industrialisation (mois 3)
- Déploiement complet sur tous les quadrants
- Mise à jour mensuelle des scores
- Rapport de performance mensuel à la direction

---

## 5. Protocole de mesure d'impact

### Pourquoi un groupe témoin ?
Si on traite tous les comptes à risque et qu'on observe 70% de rétention,
on ne sait pas si c'est grâce à l'action ou si ces comptes seraient restés
de toute façon. Le groupe témoin répond à cette question.

### Protocole A/B
- **Groupe traité (80%)** : reçoit l'action de rétention (appel, email)
- **Groupe témoin (20%)** : ne reçoit aucune action
- **Durée** : 6 semaines
- **Comparaison** : taux de rétention des deux groupes

### Uplift