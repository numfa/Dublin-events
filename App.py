import streamlit as st
import requests

# Sayfa Yapılandırması
st.set_page_config(page_title="Dublin Events", page_icon="🍀", layout="centered")

# CSS ile Renk Sabitleme ve Modern Kartlar
st.markdown("""
    <style>
    .event-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #1DB954;
        margin-bottom: 10px;
        color: #1a1a1a !important; /* Yazı rengini siyaha sabitledik */
    }
    .event-card h3 {
        color: #1a1a1a !important;
        margin-bottom: 5px;
        font-size: 1.2rem;
    }
    .event-card p {
        color: #444444 !important;
        margin: 2px 0;
    }
    .price-tag {
        color: #2e7d32 !important;
        font-weight: bold;
        font-size: 1rem;
        margin-top: 5px;
    }
    /* Buton tasarımı */
    .stLinkButton>a {
        background-color: #1DB954 !important;
        color: white !important;
        border-radius: 8px !important;
        text-align: center;
        display: block;
        text-decoration: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🍀 Dublin Rehberi")

# Kategori Seçimi
category = st.selectbox(
    "Kategori Seçin:",
    ("Hepsi", "Müzik", "Spor", "Sanat & Tiyatro")
)

cat_id = ""
if category == "Müzik": cat_id = "KZFzniwnSyZfZ7v7nJ"
elif category == "Spor": cat_id = "KZFzniwnSyZfZ7v7E"
elif category == "Sanat & Tiyatro": cat_id = "KZFzniwnSyZfZ7v7na"

def get_events(classification_id):
    api_key = "1bGiDDiTIvBAYBy68aiAAZ9TjnPZ7Vtl"
    url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={api_key}&city=Dublin&countryCode=IE&sort=date,asc&size=20"
    if classification_id:
        url += f"&classificationId={classification_id}"
    
    try:
        response = requests.get(url)
        data = response.json()
        return data.get("_embedded", {}).get("events", [])
    except:
        return []

if st.button('✨ Etkinlikleri Listele'):
    events = get_events(cat_id)
    
    if events:
        for event in events:
            name = event.get('name', 'İsimsiz Etkinlik')
            date = event.get('dates', {}).get('start', {}).get('localDate', 'Tarih Belirsiz')
            venue = event.get('_embedded', {}).get('venues', [{}])[0].get('name', 'Mekan Belirsiz')
            url = event.get('url', '#')
            
            # Fiyat Bilgisi
            price_info = ""
            prices = event.get('priceRanges', [])
            if prices:
                min_p = prices[0].get('min')
                currency = prices[0].get('currency', 'EUR')
                price_info = f"💰 {min_p} {currency}'den başlıyor"

            # Tasarım Kartı
            st.markdown(f"""
                <div class="event-card">
                    <h3>{name}</h3>
                    <p><b>📅 Tarih:</b> {date}</p>
                    <p><b>📍 Mekan:</b> {venue}</p>
                    <p class="price-tag">{price_info}</p>
                </div>
            """, unsafe_allow_html=True)
            st.link_button(f"🎟️ Detaylar ve Bilet", url)
            st.write("") # Boşluk
    else:
        st.info(f"{category} için etkinlik bulunamadı.")
