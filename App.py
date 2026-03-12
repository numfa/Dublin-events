import streamlit as st
import requests
from datetime import datetime

API_KEY = “1bGiDDiTIvBAYBy68aiAAZ9TjnPZ7Vtl”

st.set_page_config(
page_title=“Dublin’de Ne Var?”,
page_icon=“🎭”,
layout=“wide”
)

st.markdown(”””

<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #07080f;
    color: #e2e4f0;
}
.stApp { background-color: #07080f; }

h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 3rem !important;
    color: #ffffff !important;
    text-align: center;
}
.subtitle {
    text-align: center;
    color: #4a4e6a;
    font-size: 14px;
    letter-spacing: 0.15em;
    margin-bottom: 24px;
}
.label-top {
    text-align: center;
    color: #5b7fff;
    font-size: 11px;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.card {
    background: #0e1018;
    border: 1px solid #1c1f2e;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 14px;
    border-top: 2px solid;
}
.card-name {
    font-family: 'Playfair Display', serif;
    font-size: 16px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 6px;
}
.card-date { color: #5b7fff; font-size: 12px; font-family: monospace; margin-bottom: 4px; }
.card-venue { color: #4a4e6a; font-size: 12px; margin-bottom: 8px; }
.card-price { color: #00e5a0; font-size: 12px; font-family: monospace; }
.badge {
    display: inline-block;
    font-size: 10px;
    font-family: monospace;
    padding: 2px 8px;
    border-radius: 3px;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.stButton > button {
    background: linear-gradient(135deg, #5b7fff, #a855f7) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    letter-spacing: 0.1em !important;
    padding: 12px 32px !important;
    width: 100% !important;
    box-shadow: 0 0 32px rgba(91,127,255,0.35) !important;
}
.stButton > button:hover {
    box-shadow: 0 0 48px rgba(91,127,255,0.5) !important;
    transform: translateY(-1px) !important;
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
return “Tarih belirtilmemiş”
try:
dt = datetime.strptime(date_str, “%Y-%m-%d”)
formatted = dt.strftime(”%A, %d %B %Y”)
if time_str:
formatted += f” · {time_str[:5]}”
return formatted
except:
return date_str

def format_price(ev):
ranges = ev.get(“priceRanges”, [])
if not ranges:
return “”
pr = ranges[0]
mn = round(pr.get(“min”, 0))
mx = round(pr.get(“max”, 0))
if mn == mx:
return f”€{mn}”
return f”€{mn} – €{mx}”

# ── UI ──────────────────────────────────────────────────────────────

st.markdown(’<div class="label-top">◈ Dublin Event Tracker ◈</div>’, unsafe_allow_html=True)
st.markdown(”# Dublin’de Ne Var?”)
st.markdown(’<div class="subtitle">Konser  ·  Tiyatro  ·  Sergi  ·  Spor  ·  Festival</div>’, unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
fetch = st.button(“🔍  Güncel Etkinlikleri Getir”)

st.markdown(”—”)

if fetch:
with st.spinner(“Ticketmaster’dan veriler çekiliyor…”):
try:
events = fetch_events()
st.session_state[“events”] = events
st.session_state[“fetched_at”] = datetime.now().strftime(”%d.%m.%Y %H:%M”)
except Exception as e:
st.error(f”⚠️ Hata: {e}”)

if “events” in st.session_state and st.session_state[“events”]:
events = st.session_state[“events”]
st.caption(f”Son güncelleme: {st.session_state.get(‘fetched_at’, ‘’)} · {len(events)} etkinlik bulundu”)

```
# Filters
all_segs = sorted(set(
    ev.get("classifications", [{}])[0].get("segment", {}).get("name", "Miscellaneous")
    for ev in events
))
filter_options = ["🌍 Hepsi"] + [f"{CAT_EMOJI.get(s,'🎪')} {s}" for s in all_segs]
selected = st.selectbox("Kategori", filter_options, label_visibility="collapsed")
search = st.text_input("", placeholder="🔍 Etkinlik veya mekan ara...", label_visibility="collapsed")

# Filter events
filtered = []
for ev in events:
    seg = ev.get("classifications", [{}])[0].get("segment", {}).get("name", "Miscellaneous")
    if selected != "🌍 Hepsi" and f"{CAT_EMOJI.get(seg,'🎪')} {seg}" != selected:
        continue
    name = ev.get("name", "").lower()
    venue = ev.get("_embedded", {}).get("venues", [{}])[0].get("name", "").lower()
    if search and search.lower() not in name and search.lower() not in venue:
        continue
    filtered.append(ev)

st.markdown(f"<small style='color:#4a4e6a'>{len(filtered)} etkinlik</small>", unsafe_allow_html=True)
st.markdown("")

# Cards in 3 columns
cols = st.columns(3)
for i, ev in enumerate(filtered):
    seg = ev.get("classifications", [{}])[0].get("segment", {}).get("name", "Miscellaneous")
    color = CAT_COLORS.get(seg, "#5b7fff")
    emoji = CAT_EMOJI.get(seg, "🎪")
    venue = ev.get("_embedded", {}).get("venues", [{}])[0].get("name", "Dublin")
    price = format_price(ev)
    date = format_date(ev)
    link = ev.get("url", "")
    img = ""
    for im in ev.get("images", []):
        if im.get("ratio") == "16_9" and im.get("width", 0) > 400:
            img = im["url"]
            break

    with cols[i % 3]:
        st.markdown(f"""
        <div class="card" style="border-top-color:{color}">
            {"<img src='" + img + "' style='width:100%;height:130px;object-fit:cover;border-radius:4px;margin-bottom:10px;opacity:0.85' />" if img else ""}
            <div class="badge" style="background:{color}22;border:1px solid {color}44;color:{color}">{emoji} {seg}</div>
            {"<div style='float:right;color:#00e5a0;font-family:monospace;font-size:12px;margin-top:-28px'>" + price + "</div>" if price else ""}
            <div class="card-name">{ev.get('name','')}</div>
            <div class="card-date">📅 {date}</div>
            <div class="card-venue">📍 {venue}</div>
            {"<a href='" + link + "' target='_blank' style='color:" + color + ";font-size:11px;font-family:monospace;text-transform:uppercase;text-decoration:none;border-bottom:1px solid " + color + "66'>Bilet Al →</a>" if link else ""}
        </div>
        """, unsafe_allow_html=True)
```

else:
st.markdown(”””
<div style="text-align:center;padding:80px 0;color:#1e2035">
<div style="font-size:56px;opacity:0.3;margin-bottom:14px">🏙️</div>
<div style="font-size:18px">Dublin seni bekliyor</div>
<div style="font-size:13px;margin-top:6px">Butona bas, güncel etkinlikleri keşfet</div>
</div>
“””, unsafe_allow_html=True)
