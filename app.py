import streamlit as st
import pandas as pd
import json

# Configuration de la page
st.set_page_config(page_title="Tracker Recrutement MESRS", page_icon="🎓", layout="wide")

st.title("🎓 Tracker des Postes de Maître Assistant (MESRS)")
st.write("Cette plateforme recense les postes actuellement ouverts sur la plateforme officielle.")

# Charger les données depuis le fichier JSON généré par ton scraper
try:
    with open("postes_ouverts.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    st.error("Le fichier de données est introuvable. Lancez le scraper d'abord.")
    data = []

if data:
    # Convertir en DataFrame Pandas pour un bel affichage
    df = pd.DataFrame(data)
    
    # --- FILTRES ---
    st.sidebar.header("🔍 Filtres")
    
    # Filtre par Université
    universites = ["Toutes"] + sorted(df['universite'].unique().tolist())
    univ_choisie = st.sidebar.selectbox("Filtrer par Université", universites)
    
    # Recherche textuelle (ex: "Finance", "Informatique")
    recherche = st.sidebar.text_input("Rechercher une spécialité...")

    # Application des filtres
    if univ_choisie != "Toutes":
        df = df[df['universite'] == univ_choisie]
    if recherche:
        df = df[df['specialite'].str.contains(recherche, case=False, na=False)]

    # --- AFFICHAGE ---
    st.write(f"### 📋 {len(df)} Poste(s) trouvé(s)")
    
    # On affiche le tableau interactif
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("Aucun poste ouvert pour le moment.")