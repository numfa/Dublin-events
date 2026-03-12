import streamlit as st
import requests

# Sayfa Yapılandırması (Mobil öncelikli modern görünüm)
st.set_page_config(page_title="Dublin Events", page_icon="🍀", layout="centered")

# CSS ile Modern Arayüz Tasarımı
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background-color: #1DB954;
        color: white;
        font-weight: bold;
        border: none;
        height: 3.5em;
        margin-top: 10px;
    }
    .event-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    .price-tag {
        color: #2e7d32;
        font-weight: bold;
        font-size: 1.1em;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🍀 Dublin Etkinlik Rehberi")

# Kategori Seçimi
category = st.selectbox(
    "Hangi tür etkinlik bakıyorsun?",
    ("Hepsi", "Müzik", "Spor", "Sanat & Tiyatro")
)

# Kategori ID Eşleştirme
cat_id = ""
if category == "Müzik": cat_id = "KZFzniwnSyZfZ7v7nJ"
elif category == "Spor": cat_id = "KZFzniwnSyZfZ7v7nE"
elif category == "Sanat & Tiyatro": cat_id = "KZFzniwnSyZfZ7v7na"

def get_events(classification_id):
    api_key = "1bGiDDiTIvBAYBy68aiAAZ9TjnPZ7Vtl"
    url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={api_key}&city=Dublin&countryCode=IE&sort=date,asc&size=30"
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
        st.write(f"### {category} Kategorisindeki Sonuçlar")
        for event in events:
            # Veri çekme
            name = event.get('name', 'İsimsiz Etkinlik')
            date = event.get('dates', {}).get('start', {}).get('localDate', 'Tarih Belirsiz')
            venue = event.get('_embedded', {}).get('venues', [{}])[0].get('name', 'Mekan Belirsiz')
            url = event.get('url', '#')
            
            # Fiyat bilgisi çekme (Varsa)
            price_info = ""
            prices = event.get('priceRanges', [])
            if prices:
                min_p = prices[0].get('min')
                currency = prices[0].get('currency', 'EUR')
                price_info = f"💰 En düşük: {min_p} {currency}"

            # Görselleştirme
            with st.container():
                st.markdown(f"""
                <div class="event-card">
                    <h3 style='margin-top:0;'>{name}</h3>
                    <p>📅 <b>Tarih:</b> {date}</p>
                    <p>📍 <b>Mekan:</b> {venue}</p>
                    <p class="price-tag">{price_info}</p>
                </div>
                """, unsafe_allow_html=True)
                st.link_button(f"🎟️ Bilet Al / Detayları Gör", url)
                st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.info(f"Maalesef şu an {category} kategorisinde bir etkinlik bulunamadı.")

st.markdown("---")
st.caption("Veriler Ticketmaster API üzerinden canlı olarak çekilmektedir.")
