import streamlit as st
import requests

# Sayfa Yapılandırması
st.set_page_config(page_title="Dublin Events", page_icon="🍀", layout="centered")

# Tasarım
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { 
        width: 100%; 
        border-radius: 20px; 
        background-color: #00d1b2; 
        color: white; 
        font-weight: bold;
        height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🍀 Dublin Etkinlikleri")
st.write("Ticketmaster üzerinden güncel liste:")

def get_events():
    # Senin API anahtarın
    api_key = "1bGiDDiTIvBAYBy68aiAAZ9TjnPZ7Vtl"
    url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={api_key}&city=Dublin&countryCode=IE&sort=date,asc&size=20"
    
    try:
        response = requests.get(url)
        data = response.json()
        return data.get("_embedded", {}).get("events", [])
    except:
        return []

if st.button('🔄 Etkinlikleri Getir'):
    events = get_events()
    if events:
        for event in events:
            with st.expander(f"📅 {event['dates']['start']['localDate']} - {event['name']}"):
                st.write(f"**Mekan:** {event['_embedded']['venues'][0]['name']}")
                st.link_button("Bilet ve Detaylar", event['url'])
    else:
        st.error("Şu an etkinlik bulunamadı veya bir hata oluştu.")
