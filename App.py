import streamlit as st
import requests
from datetime import datetime

TM_KEY = "1bGiDDiTIvBAYBy68aiAAZ9TjnPZ7Vtl"
SG_CLIENT_ID = "MjE3NjUxNDl8MTczODA2NTYwNy4xNDc3OTE2"

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
</style>
""", unsafe_allow_html=True)

CAT_COLORS = {
    "Music": "#ff6b35",
    "Arts & Theatre": "#a855f7",
    "Sports": "#ffd84d",
    "Family": "#f040a0",
    "Miscellaneous": "#5b7fff",
    "Concert": "#ff6b35",
    "Theater": "#a855f7",
    "Other": "#5b7fff",
}
CAT_EMOJI = {
    "Music": "🎵",
    "Arts & Theatre": "🎭",
    "Sports": "⚽",
    "Family": "👨‍👩‍👧",
    "Miscellaneous": "🎪",
    "Concert": "🎵",
    "Theater": "🎭",
    "Other": "🎪",
}

def fetch_ticketmaster():
    try:
        url = "https://app.ticketmaster.com/discovery/v2/events.json"
        params = {
            "apikey": TM_KEY,
            "city": "Dublin",
            "countryCode": "IE",
            "size": 50,
            "sort": "date,asc"
        }
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
            if date_str:
                try:
                    dt = datetime.strptime(date_str, "%Y-%m-%d")
                    date_fmt = dt.strftime("%d %B %Y")
                    if time_str:
                        date_fmt += " - " + time_str[:5]
                except Exception:
                    date_fmt = date_str
            pr = ev.get("priceRanges", [])
            price = ""
            if pr:
                mn = round(pr[0].get("min", 0))
                mx = round(pr[0].get("max", 0))
                price = "EUR" + str(mn) if mn == mx else "EUR" + str(mn) + "-" + str(mx)
            img = ""
            for im in ev.get("images", []):
                if im.get("ratio") == "16_9" and im.get("width", 0) > 400:
                    img = im["url"]
                    break
            result.append({
                "name": ev.get("name", ""),
                "date": date_fmt,
                "venue": venue,
                "category": seg,
                "price": price,
                "url": ev.get("url", ""),
                "img": img,
                "source": "Ticketmaster"
            })
        return result, ""
    except Exception as e:
        return [], "Ticketmaster: " + str(e)

def fetch_seatgeek():
    try:
        url = "https://api.seatgeek.com/2/events"
        params = {
            "venue.city": "Dublin",
            "venue.country": "IE",
            "per_page": 50,
            "sort": "datetime_local.asc",
            "client_id": SG_CLIENT_ID
        }
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
        events = data.get("events", [])
        result = []
        for ev in events:
            cat = ev.get("type", "other").replace("_", " ").title()
            venue_obj = ev.get("venue", {})
            venue = venue_obj.get("name", "Dublin")
            dt_str = ev.get("datetime_local", "")
            date_fmt = ""
            if dt_str:
                try:
                    dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S")
                    date_fmt = dt.strftime("%d %B %Y - %H:%M")
                except Exception:
                    date_fmt = dt_str
            stats = ev.get("stats", {})
            mn = stats.get("lowest_price")
            price = ("EUR" + str(round(mn))) if mn else ""
            performers = ev.get("performers", [])
            img = performers[0].get("image", "") if performers else ""
            result.append({
                "name": ev.get("title", ""),
                "date": date_fmt,
                "venue": venue,
                "category": cat,
                "price": price,
                "url": ev.get("url", ""),
                "img": img,
                "source": "SeatGeek"
            })
        return result, ""
    except Exception as e:
        return [], "SeatGeek: " + str(e)

st.title("Dublin Events")
st.markdown("<p style='text-align:center;color:#4a4e6a;letter-spacing:0.1em'>Konser - Tiyatro - Spor - Festival</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    fetch = st.button("🔍 Guncel Etkinlikleri Getir")

st.markdown("---")

if fetch:
    with st.spinner("Ticketmaster ve SeatGeek taranıyor..."):
        tm_events, tm_err = fetch_ticketmaster()
        sg_events, sg_err = fetch_seatgeek()
        seen = set()
        all_events = []
        for ev in tm_events + sg_events:
            key = ev["name"].lower().strip()
            if key not in seen:
                seen.add(key)
                all_events.append(ev)
        st.session_state["events"] = all_events
        st.session_state["fetched_at"] = datetime.now().strftime("%d.%m.%Y %H:%M")
        if tm_err:
            st.warning("⚠️ " + tm_err)
        if sg_err:
            st.warning("⚠️ " + sg_err)
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Toplam", str(len(all_events)) + " etkinlik")
        col_b.metric("Ticketmaster", str(len(tm_events)))
        col_c.metric("SeatGeek", str(len(sg_events)))

if "events" in st.session_state and st.session_state["events"]:
    events = st.session_state["events"]
    st.caption("Son guncelleme: " + st.session_state.get("fetched_at", "") + " - " + str(len(events)) + " etkinlik")

    col_f, col_s = st.columns([1, 2])
    with col_f:
        all_cats = sorted(set(ev["category"] for ev in events))
        selected = st.selectbox("Kategori", ["Hepsi"] + all_cats)
    with col_s:
        search = st.text_input("Etkinlik veya mekan ara")

    source_filter = st.radio("Kaynak", ["Hepsi", "Ticketmaster", "SeatGeek"], horizontal=True)

    filtered = []
    for ev in events:
        if selected != "Hepsi" and ev["category"] != selected:
            continue
        if source_filter != "Hepsi" and ev["source"] != source_filter:
            continue
        q = search.lower()
        if q and q not in ev["name"].lower() and q not in ev["venue"].lower():
            continue
        filtered.append(ev)

    st.write(str(len(filtered)) + " etkinlik gosteriliyor")
    st.markdown("---")

    cols = st.columns(3)
    for i, ev in enumerate(filtered):
        color = CAT_COLORS.get(ev["category"], "#5b7fff")
        emoji = CAT_EMOJI.get(ev["category"], "🎪")
        src_badge = "🔵 TM" if ev["source"] == "Ticketmaster" else "🟠 SG"

        with cols[i % 3]:
            if ev["img"]:
                st.image(ev["img"], use_container_width=True)
            st.markdown(
                "<div style='background:#0e1018;border:1px solid #1c1f2e;border-top:2px solid "
                + color
                + ";border-radius:6px;padding:14px;margin-bottom:12px'>"
                + "<div style='display:flex;justify-content:space-between;margin-bottom:8px'>"
                + "<span style='background:" + color + "22;color:" + color + ";font-size:10px;padding:2px 8px;border-radius:3px'>"
                + emoji + " " + ev["category"] + "</span>"
                + "<span style='color:#555;font-size:10px'>" + src_badge + "</span>"
                + "</div>"
                + ("<div style='color:#00e5a0;font-size:12px;font-family:monospace'>" + ev["price"] + "</div>" if ev["price"] else "")
                + "<div style='font-size:15px;font-weight:700;color:#fff;margin:6px 0;line-height:1.3'>" + ev["name"] + "</div>"
                + "<div style='color:#5b7fff;font-size:11px;font-family:monospace'>📅 " + ev["date"] + "</div>"
                + "<div style='color:#4a4e6a;font-size:11px;margin-top:3px;margin-bottom:10px'>📍 " + ev["venue"] + "</div>"
                + ("<a href='" + ev["url"] + "' target='_blank' style='color:" + color + ";font-size:11px;font-family:monospace'>Bilet Al →</a>" if ev["url"] else "")
                + "</div>",
                unsafe_allow_html=True
            )
else:
    st.markdown("<div style='text-align:center;padding:60px 0'><div style='font-size:56px'>🏙️</div><div style='color:#333;font-size:16px;margin-top:10px'>Butona bas, etkinlikleri kesfet</div></div>", unsafe_allow_html=True)
