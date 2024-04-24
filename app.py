import streamlit as st
import re
import spacy
import pandas as pd
from datetime import datetime, timedelta
import joblib

# Configuration initiale de la page pour utiliser toute la largeur
st.set_page_config(layout="wide")

# Utilisation de CSS pour le style centré et moderne
st.markdown("""
    <style>
    .stTextInput {
        margin-bottom: 1rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        margin: auto;
        display: block;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

# Chargement des modèles avec spinner
with st.spinner('Chargement en cours...'):
    nlp = spacy.load('fr_core_news_sm')
    model = joblib.load('svr_model.pkl')

# Mappings et autres configurations
job_to_number = {'valet': 1, 'cuisinier': 1, 'réceptionniste': 2, 'concierge': 2, 'technicien': 3, 'rh': 4}
month_to_number = {'janvier': 1, 'février': 2, 'mars': 3, 'avril': 4, 'mai': 5, 'juin': 6, 'juillet': 7, 'août': 8, 'septembre': 9, 'octobre': 10, 'novembre': 11, 'décembre': 12}
date_pattern = r'\b(\d{1,2}) (\w+) (\d{4})\b'
job_names = {1: 'valet/cuisinier', 2: 'réceptionniste/concierge', 3: 'technicien', 4: 'RH'}
users = {'admin': 'password123',
         'Hassan':'123',
         'Stéphane':'123',
         'Frédéric':'123',
         'Laura':'123'}

# Fonctions
def login(user, password):
    return users.get(user) == password

def extract_information(text):
    dates = []
    job_number = None
    doc = nlp(text)
    for token in doc:
        if token.text.lower() in job_to_number:
            job_number = job_to_number[token.text.lower()]
            break
    matches = re.finditer(date_pattern, text)
    for match in matches:
        day, month_text, year = match.groups()
        month = month_to_number.get(month_text.lower())
        if month:
            dates.append((int(year), month, int(day)))
    return dates, job_number

def predict_number_of_stops(start_year, start_month, start_day, end_year, end_month, end_day, employment_category):
    date_list = [datetime(start_year, start_month, start_day) + timedelta(days=x) for x in range((datetime(end_year, end_month, end_day) - datetime(start_year, start_month, start_day)).days + 1)]
    data = {
        'Début Année': [date.year for date in date_list],
        'Début Mois': [date.month for date in date_list],
        'Début Jour': [date.day for date in date_list],
        'Fin Année': [date_list[-1].year] * len(date_list),
        'Fin Mois': [date_list[-1].month] * len(date_list),
        'Fin Jour': [date_list[-1].day] * len(date_list),
        'Emploi_1': [1 if employment_category == 1 else 0] * len(date_list),
        'Emploi_2': [1 if employment_category == 2 else 0] * len(date_list),
        'Emploi_3': [1 if employment_category == 3 else 0] * len(date_list),
        'Emploi_4': [1 if employment_category == 4 else 0] * len(date_list),
    }
    input_df = pd.DataFrame(data)
    predictions = model.predict(input_df)
    return predictions.sum()

# Gestion de la page de connexion et de prédiction
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    st.image("logo.png", width=150)  # Ajustez le chemin si nécessaire

if not st.session_state.authenticated:
    with col2:
        st.title("Connexion")
        user = st.text_input("Identifiant", key="username")
        password = st.text_input("Mot de passe", type='password', key="password")
        if st.button("Se connecter"):
            st.session_state.authenticated = login(user, password)
            if not st.session_state.authenticated:
                st.error("Identifiant ou mot de passe incorrect.")
else:
    with col3:
        st.title("Prévisionnel absence maladie")
        user_input = st.text_input("Avez-vous une question ?", "Demandez moi !", key="query")
        if st.button("Prédire", key="predict"):
            dates, job_number = extract_information(user_input)
            if dates and job_number and len(dates) == 2:
                predicted_stops = predict_number_of_stops(dates[0][0], dates[0][1], dates[0][2], dates[1][0], dates[1][1], dates[1][2], job_number)
                jours_absence = round(predicted_stops, 2)
                heures_remplacement = round(predicted_stops * 7, 2)
                response = f"Je pense qu'il y aura {jours_absence} jours d'absence au total, soit en moyenne {heures_remplacement} heures de remplacement à prévoir pour les {job_names[job_number]}"
                st.write(response)
