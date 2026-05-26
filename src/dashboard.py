import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import shap
import joblib
import numpy as np

# ── Config ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="smartEngine – Churn Dashboard",
    page_icon="🔮",
    layout="wide"
)

# ── Chargement des données ───────────────────────────────────────────────────
@st.cache_data
def load_data():
    scores     = pd.read_csv("outputs/scores.csv")
    prior      = pd.read_csv("outputs/priorisation.csv")
    analytics  = pd.read_csv("data/processed/analytics.csv")
    df = prior.merge(analytics, on="account_id", how="left")
    return df

@st.cache_resource
def load_model():
    return joblib.load("outputs/models/churn_model.joblib")

df    = load_data()
model = load_model()

# ── Sidebar navigation ───────────────────────────────────────────────────────
st.sidebar.title("Navigation")
vue = st.sidebar.radio("Choisir une vue", ["📊 Portefeuille", "🎯 Priorisation", "🔍 Fiche compte"])

# ════════════════════════════════════════════════════════════════════════════
# VUE 1 — PORTEFEUILLE
# ════════════════════════════════════════════════════════════════════════════
if vue == "📊 Portefeuille":
    st.title("📊 Vue Portefeuille")
    st.caption("Synthèse globale du risque de churn sur l'ensemble des comptes.")

    # KPIs
    total       = len(df)
    a_risque    = (df["churn_score"] >= 0.5).sum()
    taux_churn  = round(a_risque / total * 100, 1)
    mrr_risque  = df[df["churn_score"] >= 0.5]["MRR"].sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Comptes total",          total)
    c2.metric("Comptes à risque (≥0.5)", a_risque)
    c3.metric("Taux de churn prédit",   f"{taux_churn} %")
    c4.metric("MRR à risque (€)",       f"{mrr_risque:,.0f}")

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribution des scores de churn")
        fig = px.histogram(
            df, x="churn_score", nbins=30,
            color_discrete_sequence=["#3B82F6"],
            labels={"churn_score": "Score de churn"}
        )
        fig.add_vline(x=0.5, line_dash="dash", line_color="red",
                      annotation_text="Seuil risque", annotation_position="top right")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Répartition par quadrant")
        quad_counts = df["quadrant"].value_counts().reset_index()
        quad_counts.columns = ["Quadrant", "Nombre de comptes"]
        colors = {
            "Q1 - Priorité maximale":  "#EF4444",
            "Q2 - Action automatisée": "#F97316",
            "Q3 - Surveiller":         "#3B82F6",
            "Q4 - Stable":             "#22C55E"
        }
        fig2 = px.pie(
            quad_counts, values="Nombre de comptes", names="Quadrant",
            color="Quadrant", color_discrete_map=colors
        )
        st.plotly_chart(fig2, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# VUE 2 — PRIORISATION
# ════════════════════════════════════════════════════════════════════════════
elif vue == "🎯 Priorisation":
    st.title("🎯 Vue Priorisation")
    st.caption("Matrice risque / valeur et liste des comptes à traiter en priorité.")

    # Matrice scatter
    st.subheader("Matrice risque / valeur")
    colors = {
        "Q1 - Priorité maximale":  "#EF4444",
        "Q2 - Action automatisée": "#F97316",
        "Q3 - Surveiller":         "#3B82F6",
        "Q4 - Stable":             "#22C55E"
    }
    fig3 = px.scatter(
        df, x="churn_score", y="MRR",
        color="quadrant", color_discrete_map=colors,
        hover_data=["account_id", "action_recommandee"],
        labels={"churn_score": "Score de churn", "MRR": "MRR moyen (€)"},
        opacity=0.7
    )
    fig3.add_vline(x=0.5,                   line_dash="dash", line_color="gray")
    fig3.add_hline(y=df["MRR"].median(),    line_dash="dash", line_color="gray")
    st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    # Filtres
    st.subheader("Liste des comptes")
    col1, col2, col3 = st.columns(3)
    with col1:
        quadrants = ["Tous"] + sorted(df["quadrant"].unique().tolist())
        filtre_quad = st.selectbox("Filtrer par quadrant", quadrants)
    with col2:
        filtre_score = st.slider("Score de churn minimum", 0.0, 1.0, 0.0, 0.05)
    with col3:
        sort_col = st.selectbox("Trier par", ["churn_score", "MRR"])

    df_filtre = df.copy()
    if filtre_quad != "Tous":
        df_filtre = df_filtre[df_filtre["quadrant"] == filtre_quad]
    df_filtre = df_filtre[df_filtre["churn_score"] >= filtre_score]
    df_filtre = df_filtre.sort_values(sort_col, ascending=False)

    st.dataframe(
        df_filtre[["account_id", "churn_score", "risk_level", "MRR", "quadrant", "action_recommandee"]],
        use_container_width=True, height=400
    )

# ════════════════════════════════════════════════════════════════════════════
# VUE 3 — FICHE COMPTE
# ════════════════════════════════════════════════════════════════════════════
elif vue == "🔍 Fiche compte":
    st.title("🔍 Fiche compte")
    st.caption("Profil détaillé, score et explication des facteurs de risque.")

    account = st.selectbox("Sélectionner un compte", df["account_id"].tolist())
    row = df[df["account_id"] == account].iloc[0]

    # Profil
    col1, col2, col3 = st.columns(3)
    col1.metric("Score de churn",  f"{row['churn_score']:.0%}")
    col2.metric("Niveau de risque", row["risk_level"].upper())
    col3.metric("MRR moyen",       f"{row['MRR']:,.0f} €")

    st.info(f"**Quadrant :** {row['quadrant']}  \n**Action recommandée :** {row['action_recommandee']}")

    st.divider()

    # Profil détaillé
    st.subheader("Profil du compte")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"- **Secteur :** {row.get('industry', 'N/A')}")
        st.write(f"- **Pays :** {row.get('country', 'N/A')}")
        st.write(f"- **Ancienneté :** {row.get('anciennete_mois', 'N/A')} mois")
    with col2:
        st.write(f"- **Tickets total :** {row.get('nb_tickets_total', 'N/A')}")
        st.write(f"- **Satisfaction moyenne :** {row.get('satisfaction_moyenne', 'N/A')}")
        st.write(f"- **Jours sans activité :** {row.get('jours_depuis_derniere_activite', 'N/A')}")

    st.divider()

    # Explication : Feature Importances
    st.subheader("🧠 Pourquoi ce score ? (facteurs de risque)")
    st.caption("Les barres montrent quels facteurs contribuent le plus au risque de churn.")

    feature_cols = [
        "anciennete_mois", "nb_changements_plan", "mrr_moyen", "nb_sieges_max",
        "downgrade_detecte", "auto_renew_flag", "est_enterprise",
        "nb_tickets_total", "nb_tickets_critiques", "satisfaction_moyenne",
        "delai_resolution_moyen", "ratio_tickets_critiques",
        "usage_total_count", "nb_features_uniques",
        "jours_depuis_derniere_activite", "usage_moyen_3mois", "tendance_usage"
    ]
    available_cols = [c for c in feature_cols if c in df.columns]

    try:
        importances = model.feature_importances_
        feat_df = pd.DataFrame({
            "Feature": available_cols,
            "Importance": importances[:len(available_cols)]
        }).sort_values("Importance", ascending=True).tail(10)

        fig_imp = px.bar(
            feat_df, x="Importance", y="Feature", orientation="h",
            color="Importance",
            color_continuous_scale=["#3B82F6", "#EF4444"],
            labels={"Importance": "Importance du facteur", "Feature": "Variable"}
        )
        fig_imp.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_imp, use_container_width=True)

    except Exception as e:
        st.warning(f"Explication non disponible : {e}")