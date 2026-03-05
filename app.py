import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="Tracker Recrutement MESRS", page_icon="🎓", layout="wide")

st.title("🎓 Tracker des Postes de Maître Assistant (MESRS)")
st.write("Cette plateforme recense les annonces d'ouvertures de postes actuellement disponibles sur la plateforme officielle du ministère.")

FICHIER_JSON = "postes_ouverts.json"

# --- RÉCUPÉRATION DE LA DATE DE MISE À JOUR ---
try:
    timestamp = os.path.getmtime(FICHIER_JSON)
    last_updated = datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y à %H:%M')
    st.caption(f"🔄 **Dernière mise à jour des données :** {last_updated}")
    
    with open(FICHIER_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    st.error("Le fichier de données est introuvable. Lancez le scraper d'abord.")
    data = []

if data:
    # Convertir en DataFrame Pandas
    df = pd.DataFrame(data)
    
    # --- CALCUL DES GROS COMPTEURS ---
    total_univ = df['universite'].nunique()
    total_postes = pd.to_numeric(df['postes'], errors='coerce').fillna(0).sum()
    total_specialites = df['specialite'].nunique()

    # --- AFFICHAGE DES GROS COMPTEURS ---
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="🏫 Universités qui recrutent", value=total_univ)
    col2.metric(label="💼 Total des postes ouverts", value=int(total_postes))
    col3.metric(label="🎯 Spécialités différentes", value=total_specialites)
    st.markdown("---")
    
    # --- FILTRES (AU-DESSUS DU TABLEAU) ---
    st.write("### 🔍 Rechercher et Filtrer")
    
    # On crée deux colonnes pour mettre les filtres côte à côte
    col_filtre1, col_filtre2 = st.columns(2)
    
    universites = ["Toutes"] + sorted(df['universite'].unique().tolist())
    univ_choisie = col_filtre1.selectbox("Filtrer par Établissement", universites)
    
    recherche = col_filtre2.text_input("Rechercher une spécialité (ex: Finance, Informatique...)")

    # Application des filtres sur le tableau
    if univ_choisie != "Toutes":
        df = df[df['universite'] == univ_choisie]
    if recherche:
        df = df[df['specialite'].str.contains(recherche, case=False, na=False)]

    # --- AFFICHAGE DU TABLEAU OPTIMISÉ ---
    st.write(f"#### 📋 Résultats : {len(df)} Poste(s) correspondant(s)")
    
    # On renomme les colonnes pour que ça soit plus joli à l'écran
    df_display = df.rename(columns={
        "universite": "Établissement",
        "specialite": "Spécialité",
        "postes": "Nombre de postes",
        "departement": "Département / Faculté"
    })
    
    # Affichage propre du tableau prenant toute la largeur
    st.dataframe(df_display, use_container_width=True, hide_index=True)

else:
    st.info("Aucun poste ouvert pour le moment.")