import streamlit as st
import requests

# Sayfa Yapılandırması
st.set_page_config(page_title="Dublin Events", page_icon="🍀", layout="centered")

st.title("🍀 Dublin Etkinlikleri")
st.write("Ticketmaster üzerinden güncel liste:")

def get_events():
    api_key = "1bGiDDiTIvBAYBy68aiAAZ9TjnPZ7Vtl"
    url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={api_key}&city=Dublin&countryCode=IE&sort=date,asc&size=20"
    
    try:
        response = requests.get(url)
        data = response.json()
        return data.get("_embedded", {}).get("events", [])
    except Exception as e:
        return []

if st.button('🔄 Etkinlikleri Getir'):
    events = get_events()
    if events:
        for event in events:
            # Etkinlik bilgilerini güvenli bir şekilde çekelim
            name = event.get('name', 'İsimsiz Etkinlik')
            date = event.get('dates', {}).get('start', {}).get('localDate', 'Tarih Belirsiz')
            url = event.get('url', None) # Link yoksa None döner
            
            venues = event.get('_embedded', {}).get('venues', [])
            venue_name = venues[0].get('name', 'Mekan Belirsiz') if venues else 'Mekan Belirsiz'

            with st.expander(f"📅 {date} - {name}"):
                st.write(f"**Mekan:** {venue_name}")
                if url:
                    st.link_button("Bilet ve Detaylar", url)
                else:
                    st.write("Bilet linki mevcut değil.")
    else:
        st.info("Şu an yeni etkinlik bulunamadı.")
