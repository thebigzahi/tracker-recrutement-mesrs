import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="Tracker Recrutement MESRS", page_icon="🎓", layout="wide")

st.title("🎓 Tracker des Postes de Maître Assistant (MESRS)")
st.write("Cette plateforme recense les postes actuellement ouverts sur la plateforme officielle.")

FICHIER_JSON = "postes_ouverts.json"

# --- RÉCUPÉRATION DE LA DATE DE MISE À JOUR ---
try:
    # On regarde l'heure de dernière modification du fichier
    timestamp = os.path.getmtime(FICHIER_JSON)
    last_updated = datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y à %H:%M')
    # st.caption écrit le texte en petit et en gris (style "note de bas de page")
    st.caption(f"🔄 **Dernière mise à jour des données :** {last_updated}")
    
    # Chargement des données
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
    
    # On convertit la colonne 'postes' en nombres pour faire la somme (les erreurs/textes deviennent 0)
    total_postes = pd.to_numeric(df['postes'], errors='coerce').fillna(0).sum()
    total_specialites = df['specialite'].nunique()

    # --- AFFICHAGE DES GROS COMPTEURS ---
    st.markdown("---") # Petite ligne de séparation esthétique
    col1, col2, col3 = st.columns(3) # On divise la page en 3 colonnes
    col1.metric(label="🏫 Universités qui recrutent", value=total_univ)
    col2.metric(label="💼 Total des postes ouverts", value=int(total_postes))
    col3.metric(label="🎯 Spécialités différentes", value=total_specialites)
    st.markdown("---")
    
    # --- FILTRES BARRE LATÉRALE ---
    st.sidebar.header("🔍 Filtres")
    
    universites = ["Toutes"] + sorted(df['universite'].unique().tolist())
    univ_choisie = st.sidebar.selectbox("Filtrer par Université", universites)
    
    recherche = st.sidebar.text_input("Rechercher une spécialité...")

    # Application des filtres sur le tableau
    if univ_choisie != "Toutes":
        df = df[df['universite'] == univ_choisie]
    if recherche:
        df = df[df['specialite'].str.contains(recherche, case=False, na=False)]

    # --- AFFICHAGE DU TABLEAU ---
    st.write(f"### 📋 {len(df)} Ligne(s) correspondante(s)")
    
    # Affichage propre avec Streamlit
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("Aucun poste ouvert pour le moment.")