<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Dublin'de Ne Var?</title>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet" />
  <style>
    :root {
      --bg: #07080f;
      --surface: #0e1018;
      --border: #1c1f2e;
      --text: #e2e4f0;
      --muted: #4a4e6a;
      --accent: #5b7fff;
      --green: #00e5a0;
      --orange: #ff6b35;
      --pink: #f040a0;
      --yellow: #ffd84d;
      --purple: #a855f7;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: 'DM Sans', sans-serif;
      min-height: 100vh;
    }

    /* HEADER */
    header {
      padding: 48px 24px 40px;
      text-align: center;
      position: relative;
      overflow: hidden;
      border-bottom: 1px solid var(--border);
    }
    header::before {
      content: '';
      position: absolute;
      inset: 0;
      background:
        radial-gradient(ellipse at 20% 50%, rgba(91,127,255,0.12) 0%, transparent 55%),
        radial-gradient(ellipse at 80% 50%, rgba(168,85,247,0.10) 0%, transparent 55%),
        radial-gradient(ellipse at 50% 100%, rgba(0,229,160,0.06) 0%, transparent 50%);
      pointer-events: none;
    }
    .label {
      font-family: 'DM Sans', sans-serif;
      font-size: 11px;
      font-weight: 500;
      letter-spacing: 0.3em;
      color: var(--accent);
      text-transform: uppercase;
      margin-bottom: 14px;
    }
    h1 {
      font-family: 'Playfair Display', serif;
      font-size: clamp(32px, 7vw, 58px);
      font-weight: 700;
      color: #fff;
      line-height: 1.1;
      margin-bottom: 10px;
    }
    .subtitle {
      color: var(--muted);
      font-size: 14px;
      font-weight: 300;
      letter-spacing: 0.08em;
      margin-bottom: 32px;
    }

    /* BUTTON */
    #fetchBtn {
      background: linear-gradient(135deg, var(--accent), var(--purple));
      border: none;
      border-radius: 6px;
      color: #fff;
      cursor: pointer;
      font-family: 'DM Sans', sans-serif;
      font-size: 14px;
      font-weight: 500;
      letter-spacing: 0.1em;
      padding: 14px 36px;
      text-transform: uppercase;
      box-shadow: 0 0 32px rgba(91,127,255,0.35);
      transition: all 0.25s;
      position: relative;
    }
    #fetchBtn:hover { transform: translateY(-1px); box-shadow: 0 0 48px rgba(91,127,255,0.5); }
    #fetchBtn:disabled { background: var(--surface); color: var(--muted); box-shadow: none; cursor: not-allowed; transform: none; }
    .spinner { display: inline-block; animation: spin 0.9s linear infinite; margin-right: 8px; }
    @keyframes spin { to { transform: rotate(360deg); } }

    #lastUpdated {
      margin-top: 10px;
      font-size: 11px;
      color: var(--muted);
      letter-spacing: 0.05em;
    }

    /* FILTERS */
    #filters {
      display: none;
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      padding: 12px 20px;
      gap: 6px;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
    }
    #filters.visible { display: flex; }
    .filter-btn {
      background: transparent;
      border: 1px solid var(--border);
      border-radius: 20px;
      color: var(--muted);
      cursor: pointer;
      font-family: 'DM Sans', sans-serif;
      font-size: 12px;
      padding: 5px 14px;
      white-space: nowrap;
      transition: all 0.2s;
    }
    .filter-btn.active {
      background: rgba(91,127,255,0.15);
      border-color: var(--accent);
      color: #a0b4ff;
    }

    /* SEARCH */
    #searchWrap {
      display: none;
      background: var(--surface);
      padding: 12px 20px;
      border-bottom: 1px solid var(--border);
    }
    #searchWrap.visible { display: block; }
    #searchInput {
      background: rgba(255,255,255,0.04);
      border: 1px solid var(--border);
      border-radius: 6px;
      color: var(--text);
      font-family: 'DM Sans', sans-serif;
      font-size: 13px;
      outline: none;
      padding: 9px 16px;
      width: 100%;
      max-width: 360px;
      transition: border-color 0.2s;
    }
    #searchInput:focus { border-color: var(--accent); }
    #searchInput::placeholder { color: var(--muted); }

    /* MAIN */
    main { padding: 24px 20px; max-width: 1120px; margin: 0 auto; }

    #statusMsg {
      display: none;
      text-align: center;
      padding: 70px 0;
    }
    #statusMsg .icon { font-size: 52px; animation: pulse 1.4s ease-in-out infinite; margin-bottom: 16px; }
    #statusMsg .text { color: var(--accent); font-size: 15px; }
    @keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.3; } }

    #errorMsg {
      display: none;
      background: rgba(255,80,80,0.08);
      border: 1px solid rgba(255,80,80,0.2);
      border-radius: 6px;
      color: #ff9999;
      font-size: 13px;
      padding: 14px 18px;
      margin-bottom: 20px;
    }

    #countLabel {
      font-size: 11px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.1em;
      margin-bottom: 16px;
    }

    /* GRID */
    #grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
      gap: 14px;
    }

    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 6px;
      overflow: hidden;
      transition: transform 0.15s, box-shadow 0.15s;
      cursor: default;
    }
    .card:hover { transform: translateY(-3px); box-shadow: 0 10px 36px rgba(0,0,0,0.5); }
    .card-img {
      width: 100%;
      height: 140px;
      object-fit: cover;
      display: block;
      opacity: 0.85;
    }
    .card-body { padding: 16px; }
    .card-top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 10px;
    }
    .badge {
      border-radius: 3px;
      font-size: 10px;
      font-family: monospace;
      letter-spacing: 0.08em;
      padding: 2px 8px;
      text-transform: uppercase;
    }
    .price {
      font-family: monospace;
      font-size: 12px;
      color: var(--green);
      flex-shrink: 0;
      margin-left: 8px;
    }
    .card-name {
      font-family: 'Playfair Display', serif;
      font-size: 15px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 7px;
      line-height: 1.3;
    }
    .card-date {
      font-size: 11px;
      font-family: monospace;
      color: var(--accent);
      margin-bottom: 4px;
    }
    .card-venue {
      font-size: 11px;
      color: var(--muted);
      margin-bottom: 12px;
    }
    .card-link {
      font-size: 11px;
      font-family: monospace;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      text-decoration: none;
      padding-bottom: 1px;
    }

    /* EMPTY */
    #empty {
      display: none;
      text-align: center;
      padding: 80px 0;
      color: #1e2035;
    }
    #empty .icon { font-size: 56px; opacity: 0.3; margin-bottom: 14px; }
    #empty .text { font-size: 16px; }
    #empty .sub { font-size: 13px; margin-top: 6px; }

    ::-webkit-scrollbar { height: 3px; width: 3px; }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
  </style>
</head>
<body>

<header>
  <div class="label">◈ Dublin Event Tracker ◈</div>
  <h1>Dublin'de Ne Var?</h1>
  <p class="subtitle">Konser &nbsp;·&nbsp; Tiyatro &nbsp;·&nbsp; Sergi &nbsp;·&nbsp; Spor &nbsp;·&nbsp; Festival</p>
  <button id="fetchBtn" onclick="fetchEvents()">🔍 &nbsp;Güncel Etkinlikleri Getir</button>
  <div id="lastUpdated"></div>
</header>

<div id="searchWrap">
  <input id="searchInput" type="text" placeholder="Etkinlik veya mekan ara..." oninput="renderCards()" />
</div>

<div id="filters">
  <button class="filter-btn active" data-cat="all" onclick="setFilter(this)">🌍 Hepsi</button>
  <button class="filter-btn" data-cat="Music" onclick="setFilter(this)">🎵 Konser</button>
  <button class="filter-btn" data-cat="Arts &amp; Theatre" onclick="setFilter(this)">🎭 Tiyatro</button>
  <button class="filter-btn" data-cat="Sports" onclick="setFilter(this)">⚽ Spor</button>
  <button class="filter-btn" data-cat="Family" onclick="setFilter(this)">👨‍👩‍👧 Aile</button>
  <button class="filter-btn" data-cat="Miscellaneous" onclick="setFilter(this)">🎪 Diğer</button>
</div>

<main>
  <div id="statusMsg"><div class="icon">🗺️</div><div class="text">Ticketmaster'dan veriler çekiliyor...</div></div>
  <div id="errorMsg"></div>
  <div id="countLabel"></div>
  <div id="grid"></div>
  <div id="empty">
    <div class="icon">🏙️</div>
    <div class="text">Dublin seni bekliyor</div>
    <div class="sub">Butona bas, güncel etkinlikleri keşfet</div>
  </div>
</main>

<script>
  const API_KEY = "1bGiDDiTIvBAYBy68aiAAZ9TjnPZ7Vtl";
  let allEvents = [];
  let activeFilter = "all";

  const CAT_COLORS = {
    "Music": "#ff6b35",
    "Arts & Theatre": "#a855f7",
    "Sports": "#ffd84d",
    "Family": "#f040a0",
    "Miscellaneous": "#5b7fff",
  };

  function getColor(seg) { return CAT_COLORS[seg] || "#5b7fff"; }

  async function fetchEvents() {
    const btn = document.getElementById("fetchBtn");
    const statusMsg = document.getElementById("statusMsg");
    const errorMsg = document.getElementById("errorMsg");
    const emptyEl = document.getElementById("empty");

    btn.disabled = true;
    btn.innerHTML = '<span class="spinner">◎</span> Yükleniyor...';
    statusMsg.style.display = "block";
    errorMsg.style.display = "none";
    emptyEl.style.display = "none";
    document.getElementById("grid").innerHTML = "";
    document.getElementById("countLabel").textContent = "";

    try {
      // Use allorigins CORS proxy to bypass CORS
      const tmUrl = `https://app.ticketmaster.com/discovery/v2/events.json?apikey=${API_KEY}&city=Dublin&countryCode=IE&size=50&sort=date,asc`;
      const proxyUrl = `https://api.allorigins.win/get?url=${encodeURIComponent(tmUrl)}`;

      const res = await fetch(proxyUrl);
      if (!res.ok) throw new Error("Bağlantı hatası: " + res.status);

      const wrapper = await res.json();
      const data = JSON.parse(wrapper.contents);

      if (data.fault) throw new Error("API hatası: " + (data.fault.faultstring || "Geçersiz key"));

      allEvents = (data?._embedded?.events || []);

      if (allEvents.length === 0) {
        statusMsg.style.display = "none";
        emptyEl.style.display = "block";
        return;
      }

      document.getElementById("filters").classList.add("visible");
      document.getElementById("searchWrap").classList.add("visible");
      document.getElementById("lastUpdated").textContent =
        `Son güncelleme: ${new Date().toLocaleString("tr-TR")} · ${allEvents.length} etkinlik`;

      renderCards();

    } catch (err) {
      errorMsg.textContent = "⚠️ " + err.message;
      errorMsg.style.display = "block";
    } finally {
      statusMsg.style.display = "none";
      btn.disabled = false;
      btn.innerHTML = "🔄 &nbsp;Yenile";
    }
  }

  function setFilter(el) {
    document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
    el.classList.add("active");
    activeFilter = el.dataset.cat;
    renderCards();
  }

  function renderCards() {
    const q = (document.getElementById("searchInput")?.value || "").toLowerCase();
    const grid = document.getElementById("grid");
    const countLabel = document.getElementById("countLabel");

    const filtered = allEvents.filter(ev => {
      const seg = ev.classifications?.[0]?.segment?.name || "Miscellaneous";
      const matchCat = activeFilter === "all" || seg === activeFilter;
      const name = (ev.name || "").toLowerCase();
      const venue = (ev._embedded?.venues?.[0]?.name || "").toLowerCase();
      const matchSearch = !q || name.includes(q) || venue.includes(q);
      return matchCat && matchSearch;
    });

    countLabel.textContent = filtered.length + " etkinlik";
    grid.innerHTML = "";

    filtered.forEach(ev => {
      const seg = ev.classifications?.[0]?.segment?.name || "Miscellaneous";
      const color = getColor(seg);
      const venue = ev._embedded?.venues?.[0]?.name || "Dublin";
      const dateStr = ev.dates?.start?.localDate || "";
      const timeStr = ev.dates?.start?.localTime || "";
      const dateFormatted = dateStr
        ? new Date(dateStr + "T" + (timeStr || "00:00")).toLocaleDateString("tr-TR", {
            weekday: "short", day: "numeric", month: "long", year: "numeric"
          }) + (timeStr ? " · " + timeStr.slice(0,5) : "")
        : "Tarih belirtilmemiş";
      const img = ev.images?.find(i => i.ratio === "16_9" && i.width > 400)?.url || ev.images?.[0]?.url || "";
      const pr = ev.priceRanges?.[0];
      const price = pr ? `€${Math.round(pr.min)}${pr.max !== pr.min ? "–€" + Math.round(pr.max) : ""}` : "";

      const card = document.createElement("div");
      card.className = "card";
      card.style.borderTop = `2px solid ${color}`;
      card.innerHTML = `
        ${img ? `<img class="card-img" src="${img}" alt="${ev.name}" loading="lazy" />` : ""}
        <div class="card-body">
          <div class="card-top">
            <span class="badge" style="background:${color}18;border:1px solid ${color}35;color:${color}">${seg}</span>
            ${price ? `<span class="price">${price}</span>` : ""}
          </div>
          <div class="card-name">${ev.name}</div>
          <div class="card-date">📅 ${dateFormatted}</div>
          <div class="card-venue">📍 ${venue}</div>
          ${ev.url ? `<a class="card-link" href="${ev.url}" target="_blank" rel="noopener" style="color:${color};border-bottom:1px solid ${color}40">Bilet Al →</a>` : ""}
        </div>
      `;
      grid.appendChild(card);
    });

    if (filtered.length === 0) {
      grid.innerHTML = `<div style="color:#2a2d45;font-size:14px;padding:40px 0;text-align:center">Sonuç bulunamadı</div>`;
    }
  }

  // Show empty on load
  document.getElementById("empty").style.display = "block";
</script>
</body>
</html>
