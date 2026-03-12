import streamlit as st
import requests
from datetime import datetime

API_KEY = "1bGiDDiTIvBAYBy68aiAAZ9TjnPZ7Vtl"

st.set_page_config(page_title=“Dublin’de Ne Var?”, page_icon=“🎭”, layout=“wide”)

st.markdown(”””

<style>
.stApp { background-color: #07080f; color: #e2e4f0; }
h1 { text-align: center; color: #ffffff !important; }
.stButton > button {
    background: linear-gradient(135deg, #5b7fff, #a855f7) !important;
    color: white !important; border: none !important;
    border-radius: 6px !important; width: 100% !important;
}
</style>

“””, unsafe_allow_html=True)

CAT_COLORS = {
“Music”: “#ff6b35”,
“Arts & Theatre”: “#a855f7”,
“Sports”: “#ffd84d”,
“Family”: “#f040a0”,
“Miscellaneous”: “#5b7fff”,
}
CAT_EMOJI = {
“Music”: “🎵”,
“Arts & Theatre”: “🎭”,
“Sports”: “⚽”,
“Family”: “👨‍👩‍👧”,
“Miscellaneous”: “🎪”,
}

def fetch_events():
url = “https://app.ticketmaster.com/discovery/v2/events.json”
params = {
“apikey”: API_KEY,
“city”: “Dublin”,
“countryCode”: “IE”,
“size”: 50,
“sort”: “date,asc”
}
res = requests.get(url, params=params, timeout=10)
res.raise_for_status()
data = res.json()
return data.get(”_embedded”, {}).get(“events”, [])

def format_date(ev):
date_str = ev.get(“dates”, {}).get(“start”, {}).get(“localDate”, “”)
time_str = ev.get(“dates”, {}).get(“start”, {}).get(“localTime”, “”)
if not date_str:
return “Tarih belirtilmemis”
try:
dt = datetime.strptime(date_str, “%Y-%m-%d”)
formatted = dt.strftime(”%d %B %Y”)
if time_str:
formatted += “ - “ + time_str[:5]
return formatted
except Exception:
return date_str

def format_price(ev):
ranges = ev.get(“priceRanges”, [])
if not ranges:
return “”
pr = ranges[0]
mn = round(pr.get(“min”, 0))
mx = round(pr.get(“max”, 0))
if mn == mx:
return “EUR” + str(mn)
return “EUR” + str(mn) + “ - “ + str(mx)

st.title(“Dublin’de Ne Var?”)
st.markdown(”<p style='text-align:center;color:#4a4e6a'>Konser · Tiyatro · Spor · Festival</p>”, unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
fetch = st.button(“🔍 Guncel Etkinlikleri Getir”)

st.markdown(”—”)

if fetch:
with st.spinner(“Ticketmaster’dan veriler cekiliyor…”):
try:
events = fetch_events()
st.session_state[“events”] = events
st.session_state[“fetched_at”] = datetime.now().strftime(”%d.%m.%Y %H:%M”)
except Exception as e:
st.error(“Hata: “ + str(e))

if “events” in st.session_state and st.session_state[“events”]:
events = st.session_state[“events”]
st.caption(“Son guncelleme: “ + st.session_state.get(“fetched_at”, “”) + “ - “ + str(len(events)) + “ etkinlik”)

```
all_segs = sorted(set(
    ev.get("classifications", [{}])[0].get("segment", {}).get("name", "Miscellaneous")
    for ev in events
))
filter_options = ["Hepsi"] + all_segs
selected = st.selectbox("Kategori", filter_options)
search = st.text_input("Etkinlik veya mekan ara")

filtered = []
for ev in events:
    seg = ev.get("classifications", [{}])[0].get("segment", {}).get("name", "Miscellaneous")
    if selected != "Hepsi" and seg != selected:
        continue
    name = ev.get("name", "").lower()
    venue_name = ev.get("_embedded", {}).get("venues", [{}])[0].get("name", "").lower()
    if search and search.lower() not in name and search.lower() not in venue_name:
        continue
    filtered.append(ev)

st.write(str(len(filtered)) + " etkinlik")

cols = st.columns(3)
for i, ev in enumerate(filtered):
    seg = ev.get("classifications", [{}])[0].get("segment", {}).get("name", "Miscellaneous")
    color = CAT_COLORS.get(seg, "#5b7fff")
    emoji = CAT_EMOJI.get(seg, "🎪")
    venue_name = ev.get("_embedded", {}).get("venues", [{}])[0].get("name", "Dublin")
    price = format_price(ev)
    date = format_date(ev)
    link = ev.get("url", "")

    img = ""
    for im in ev.get("images", []):
        if im.get("ratio") == "16_9" and im.get("width", 0) > 400:
            img = im["url"]
            break

    with cols[i % 3]:
        if img:
            st.image(img, use_container_width=True)
        st.markdown(
            "<div style='background:#0e1018;border:1px solid #1c1f2e;border-top:2px solid "
            + color
            + ";border-radius:6px;padding:14px;margin-bottom:12px'>"
            + "<span style='background:" + color + "22;border:1px solid " + color + "44;color:" + color + ";font-size:10px;font-family:monospace;padding:2px 8px;border-radius:3px'>"
            + emoji + " " + seg
            + "</span>"
            + ("<span style='float:right;color:#00e5a0;font-size:12px;font-family:monospace'>" + price + "</span>" if price else "")
            + "<div style='font-size:15px;font-weight:700;color:#fff;margin:8px 0 4px'>" + ev.get("name", "") + "</div>"
            + "<div style='color:#5b7fff;font-size:11px;font-family:monospace'>📅 " + date + "</div>"
            + "<div style='color:#4a4e6a;font-size:11px;margin-top:3px'>📍 " + venue_name + "</div>"
            + ("<div style='margin-top:10px'><a href='" + link + "' target='_blank' style='color:" + color + ";font-size:11px;font-family:monospace'>Bilet Al →</a></div>" if link else "")
            + "</div>",
            unsafe_allow_html=True
        )
```

else:
st.markdown(”<div style='text-align:center;padding:60px 0;color:#333'><div style='font-size:48px'>🏙️</div><div>Butona bas, etkinlikleri kefset</div></div>”, unsafe_allow_html=True)
