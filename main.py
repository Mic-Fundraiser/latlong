import streamlit as st
import requests
import streamlit.components.v1 as components

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

# Configura la chiave API direttamente nel codice
API_KEY = 'AIzaSyArBylVJ80cO8QsvhvQbpGZIoHOj3ESgcY'  # Sostituisci con la tua chiave API

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Geolocalizzatore", page_icon="🌍")

# Titolo dell'app
st.title("🌍 Geolocalizzatore")

# Descrizione dell'app
st.write("Questa app converte un indirizzo in coordinate geografiche utilizzando l'API di Google Maps.")

# Input per l'indirizzo
address = st.text_input("Inserisci l'indirizzo (via, città, CAP):")

# Componente personalizzato per il pulsante di copia
def copy_button(text, button_text="Copia"):
    components.html(
        f"""
        <button onclick="copyToClipboard('{text}')">{button_text}</button>
        <script>
        function copyToClipboard(text) {{
            navigator.clipboard.writeText(text).then(function() {{
                console.log('Copying to clipboard was successful!');
            }}, function(err) {{
                console.error('Could not copy text: ', err);
            }});
        }}
        </script>
        """,
        height=30
    )

# Pulsante per avviare la geolocalizzazione
if st.button("Ottieni Coordinate"):
    if address:
        with st.spinner("Ricerca in corso..."):
            result = get_lat_long_google(address, API_KEY)
        if isinstance(result, tuple):
            st.success("Coordinate trovate!")
            
            # Visualizza latitudine con pulsante di copia
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"Latitudine: {result[0]}")
            with col2:
                copy_button(result[0])
            
            # Visualizza longitudine con pulsante di copia
            col3, col4 = st.columns([3, 1])
            with col3:
                st.write(f"Longitudine: {result[1]}")
            with col4:
                copy_button(result[1])
            
            # Visualizzazione della mappa
            st.write("Posizione sulla mappa:")
            map_url = f"https://www.google.com/maps/embed/v1/place?key={API_KEY}&q={result[0]},{result[1]}"
            st.components.v1.iframe(map_url, width=600, height=450, scrolling=False)
        else:
            st.error(result)
    else:
        st.warning("Per favore, inserisci un indirizzo.")

# Informazioni aggiuntive
st.info("Nota: Questa app utilizza una chiave API predefinita per Google Maps.")
