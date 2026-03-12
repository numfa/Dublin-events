import streamlit as st
import requests
from datetime import datetime, date

TM_KEY = "1bGiDDiTIvBAYBy68aiAAZ9TjnPZ7Vtl"

st.set_page_config(page_title="Dublin Events", page_icon="🎭", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #07080f; color: #e2e4f0; }
.stButton > button {
    background: linear-gradient(135deg, #5b7fff, #a855f7) !important;
    color: white !important; border: none !important;
    border-radius: 6px !important; width: 100% !important;
    font-size: 15px !important; padding: 12px !important;
}
div[data-testid="stDateInput"] input {
    background-color: #0e1018 !important;
    color: #e2e4f0 !important;
    border: 1px solid #1c1f2e !important;
    border-radius: 6px !important;
}
div[data-testid="stSelectbox"] > div {
    background-color: #0e1018 !important;
    border: 1px solid #1c1f2e !important;
}
</style>
""", unsafe_allow_html=True)

CAT_COLORS = {
    "Music": "#ff6b35",
    "Arts & Theatre": "#a855f7",
    "Sports": "#ffd84d",
    "Family": "#f040a0",
    "Miscellaneous": "#5b7fff",
}
CAT_EMOJI = {
    "Music": "🎵",
    "Arts & Theatre": "🎭",
    "Sports": "⚽",
    "Family": "👨‍👩‍👧",
    "Miscellaneous": "🎪",
}

def fetch_ticketmaster(start_date=None, end_date=None):
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": TM_KEY,
        "city": "Dublin",
        "countryCode": "IE",
        "size": 100,
        "sort": "date,asc"
    }
    if start_date:
        params["startDateTime"] = start_date.strftime("%Y-%m-%d") + "T00:00:00Z"
    if end_date:
        params["endDateTime"] = end_date.strftime("%Y-%m-%d") + "T23:59:59Z"

    res = requests.get(url, params=params, timeout=10)
    res.raise_for_status()
    data = res.json()
    events = data.get("_embedded", {}).get("events", [])
    result = []
    for ev in events:
        seg = ev.get("classifications", [{}])[0].get("segment", {}).get("name", "Miscellaneous")
        venue = ev.get("_embedded", {}).get("venues", [{}])[0].get("name", "Dublin")
        date_str = ev.get("dates", {}).get("start", {}).get("localDate", "")
        time_str = ev.get("dates", {}).get("start", {}).get("localTime", "")
        date_fmt = ""
        date_obj = None
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                date_fmt = date_obj.strftime("%d %B %Y")
                if time_str:
                    date_fmt += " - " + time_str[:5]
            except Exception:
                date_fmt = date_str
        pr = ev.get("priceRanges", [])
        price = ""
        price_min = None
        price_max = None
        if pr:
            price_min = pr[0].get("min")
            price_max = pr[0].get("max")
            currency = pr[0].get("currency", "EUR")
            if price_min is not None and price_max is not None:
                mn = round(price_min)
                mx = round(price_max)
                if mn == mx:
                    price = currency + " " + str(mn)
                else:
                    price = currency + " " + str(mn) + " - " + str(mx)
        img = ""
        for im in ev.get("images", []):
            if im.get("ratio") == "16_9" and im.get("width", 0) > 400:
                img = im["url"]
                break
        result.append({
            "name": ev.get("name", ""),
            "date": date_fmt,
            "date_obj": date_obj,
            "venue": venue,
            "category": seg,
            "price": price,
            "price_min": price_min,
            "url": ev.get("url", ""),
            "img": img,
        })
    return result

st.title("Dublin Events")
st.markdown("<p style='text-align:center;color:#4a4e6a;letter-spacing:0.1em'>Konser - Tiyatro - Spor - Festival</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    fetch = st.button("🔍 Guncel Etkinlikleri Getir")

st.markdown("---")

if fetch:
    with st.spinner("Ticketmaster taranıyor..."):
        try:
            events = fetch_ticketmaster()
            st.session_state["events"] = events
            st.session_state["fetched_at"] = datetime.now().strftime("%d.%m.%Y %H:%M")
            st.success(str(len(events)) + " etkinlik bulundu!")
        except Exception as e:
            st.error("Hata: " + str(e))

if "events" in st.session_state and st.session_state["events"]:
    events = st.session_state["events"]
    st.caption("Son guncelleme: " + st.session_state.get("fetched_at", "") + " - " + str(len(events)) + " etkinlik")

    st.markdown("### 🔎 Filtrele")
    col_f1, col_f2, col_f3, col_f4 = st.columns([1, 1, 1, 1])

    with col_f1:
        all_cats = sorted(set(ev["category"] for ev in events))
        selected_cat = st.selectbox("Kategori", ["Hepsi"] + all_cats)

    with col_f2:
        date_start = st.date_input("Baslangic Tarihi", value=None, min_value=date.today())

    with col_f3:
        date_end = st.date_input("Bitis Tarihi", value=None, min_value=date.today())

    with col_f4:
        price_opts = ["Hepsi", "Ucretsiz / Fiyatsiz", "EUR 0-50", "EUR 50-100", "EUR 100+"]
        selected_price = st.selectbox("Fiyat Araligi", price_opts)

    search = st.text_input("🔍 Etkinlik veya mekan ara")

    filtered = []
    for ev in events:
        if selected_cat != "Hepsi" and ev["category"] != selected_cat:
            continue

        if date_start and ev["date_obj"] and ev["date_obj"] < date_start:
            continue
        if date_end and ev["date_obj"] and ev["date_obj"] > date_end:
            continue

        if selected_price == "Ucretsiz / Fiyatsiz" and ev["price"]:
            continue
        elif selected_price == "EUR 0-50":
            if ev["price_min"] is None or ev["price_min"] > 50:
                continue
        elif selected_price == "EUR 50-100":
            if ev["price_min"] is None or ev["price_min"] < 50 or ev["price_min"] > 100:
                continue
        elif selected_price == "EUR 100+":
            if ev["price_min"] is None or ev["price_min"] < 100:
                continue

        q = search.lower()
        if q and q not in ev["name"].lower() and q not in ev["venue"].lower():
            continue

        filtered.append(ev)

    st.markdown("---")
    st.write(str(len(filtered)) + " etkinlik gosteriliyor")

    cols = st.columns(3)
    for i, ev in enumerate(filtered):
        color = CAT_COLORS.get(ev["category"], "#5b7fff")
        emoji = CAT_EMOJI.get(ev["category"], "🎪")

        with cols[i % 3]:
            if ev["img"]:
                st.image(ev["img"], use_container_width=True)
            price_html = ""
            if ev["price"]:
                price_html = "<div style='background:#00e5a022;border:1px solid #00e5a044;border-radius:4px;padding:4px 10px;display:inline-block;color:#00e5a0;font-size:13px;font-family:monospace;margin-bottom:8px'>🎟️ " + ev["price"] + "</div>"
            else:
                price_html = "<div style='color:#555;font-size:11px;margin-bottom:8px'>Fiyat bilgisi yok</div>"
            st.markdown(
                "<div style='background:#0e1018;border:1px solid #1c1f2e;border-top:2px solid "
                + color
                + ";border-radius:6px;padding:14px;margin-bottom:12px'>"
                + "<span style='background:" + color + "22;color:" + color + ";font-size:10px;padding:2px 8px;border-radius:3px'>"
                + emoji + " " + ev["category"] + "</span>"
                + "<div style='font-size:15px;font-weight:700;color:#fff;margin:8px 0 4px;line-height:1.3'>" + ev["name"] + "</div>"
                + "<div style='color:#5b7fff;font-size:11px;font-family:monospace;margin-bottom:3px'>📅 " + ev["date"] + "</div>"
                + "<div style='color:#4a4e6a;font-size:11px;margin-bottom:10px'>📍 " + ev["venue"] + "</div>"
                + price_html
                + ("<div style='margin-top:10px'><a href='" + ev["url"] + "' target='_blank' style='background:" + color + ";color:#000;font-size:11px;font-family:monospace;padding:5px 12px;border-radius:4px;text-decoration:none;font-weight:700'>Bilet Al →</a></div>" if ev["url"] else "")
                + "</div>",
                unsafe_allow_html=True
            )
else:
    st.markdown("<div style='text-align:center;padding:60px 0'><div style='font-size:56px'>🏙️</div><div style='color:#333;font-size:16px;margin-top:10px'>Butona bas, etkinlikleri kesfet</div></div>", unsafe_allow_html=True)
