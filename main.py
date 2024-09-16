import streamlit as st
import requests

# Funzione per ottenere latitudine e longitudine usando l'API di Google Maps
def get_lat_long_google(address, api_key):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': address,
        'key': api_key
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            return (location['lat'], location['lng'])
        else:
            return f"Errore: {data['status']}"
    except Exception as e:
        return f"Errore nella richiesta: {e}"

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Geolocalizzatore", page_icon="🌍")

# Titolo dell'app
st.title("🌍 Geolocalizzatore")

# Descrizione dell'app
st.write("Questa app converte un indirizzo in coordinate geografiche utilizzando l'API di Google Maps.")

# Input per la chiave API
api_key = st.text_input("Inserisci la tua chiave API di Google Maps:", type="password")

# Input per l'indirizzo
address = st.text_input("Inserisci l'indirizzo (via, città, CAP):")

# Pulsante per avviare la geolocalizzazione
if st.button("Ottieni Coordinate"):
    if api_key and address:
        with st.spinner("Ricerca in corso..."):
            result = get_lat_long_google(address, api_key)
        if isinstance(result, tuple):
            st.success("Coordinate trovate!")
            st.write(f"Latitudine: {result[0]}")
            st.write(f"Longitudine: {result[1]}")
            
            # Visualizzazione della mappa
            st.write("Posizione sulla mappa:")
            map_url = f"https://www.google.com/maps/embed/v1/place?key={api_key}&q={result[0]},{result[1]}"
            st.components.v1.iframe(map_url, width=600, height=450, scrolling=False)
        else:
            st.error(result)
    else:
        st.warning("Per favore, inserisci sia la chiave API che l'indirizzo.")

# Informazioni aggiuntive
st.info("Nota: Assicurati di utilizzare una chiave API valida di Google Maps per far funzionare questa app.")
