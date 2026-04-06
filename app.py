from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf

from modules.ai_signals import AISignalEngine
from modules.news_fetcher import NewsFetcher
from modules.pattern_detection import PatternDetector
from modules.styles import inject_custom_css
from modules.technical_analysis import TechnicalAnalyzer
from modules.trading_schools import TradingSchoolsAnalyzer

st.set_page_config(
    page_title="NEXUS Trading Intelligence",
    page_icon="N",
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_custom_css()

NEWS_FETCHER = NewsFetcher()

SYMBOLS = {
    "EUR/USD": "FX:EURUSD",
    "GBP/USD": "FX:GBPUSD",
    "USD/JPY": "FX:USDJPY",
    "BTC/USDT": "BINANCE:BTCUSDT",
    "ETH/USDT": "BINANCE:ETHUSDT",
    "AAPL": "NASDAQ:AAPL",
    "TSLA": "NASDAQ:TSLA",
}
YF_SYMBOLS = {
    "FX:EURUSD": "EURUSD=X",
    "FX:GBPUSD": "GBPUSD=X",
    "FX:USDJPY": "JPY=X",
    "BINANCE:BTCUSDT": "BTC-USD",
    "BINANCE:ETHUSDT": "ETH-USD",
    "NASDAQ:AAPL": "AAPL",
    "NASDAQ:TSLA": "TSLA",
}
TV_INTERVALS = {"1m": "1", "5m": "5", "15m": "15", "1h": "60", "4h": "240", "1D": "D"}
YF_INTERVALS = {"1m": "1m", "5m": "5m", "15m": "15m", "1h": "1h", "4h": "1h", "1D": "1d"}
MODES = {
    "SMART": {"label": "Smart AI", "icon": "Fusion", "color": "#87f5d3"},
    "SMC": {"label": "SMC", "icon": "Structure", "color": "#85a8ff"},
    "ICT": {"label": "ICT", "icon": "Flow", "color": "#d1b4ff"},
    "SK": {"label": "SK", "icon": "Trend", "color": "#ffd287"},
}


def init_state() -> None:
    defaults = {
        "active_mode": "SMART",
        "analysis_result": None,
        "analysis_details": None,
        "news_data": [],
        "news_summary": {},
        "current_page": "dashboard",
        "selected_pair": "EUR/USD",
        "selected_tf": "1h",
        "last_analysis_key": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


@st.cache_data(ttl=180)
def load_ohlcv(symbol: str, interval: str) -> pd.DataFrame:
    ticker = yf.Ticker(symbol)
    df = ticker.history(period="6mo", interval=interval)
    if df.empty:
        return pd.DataFrame()
    df.columns = [col.lower() for col in df.columns]
    output = df[["open", "high", "low", "close", "volume"]].dropna()
    return output


@st.cache_data(ttl=300, show_spinner=False)
def fetch_news_cached(symbol: str) -> tuple[list[dict], dict]:
    items = NEWS_FETCHER.get_news(symbol)
    summary = NEWS_FETCHER.summarize_news(symbol, items)
    return items, summary


def build_tradingview_html(symbol: str, interval: str, height: int) -> str:
    return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <style>
    html, body {{
      margin: 0;
      padding: 0;
      width: 100%;
      height: 100%;
      overflow: hidden;
      background:
        radial-gradient(circle at top, rgba(118, 255, 214, 0.15), transparent 36%),
        linear-gradient(180deg, #07111d 0%, #050913 100%);
    }}
    #tv-wrap {{
      width: 100%;
      height: 100%;
      min-height: {height}px;
      border-radius: 28px;
      overflow: hidden;
    }}
    #tv-chart {{
      width: 100%;
      height: 100%;
    }}
    .tv-fallback {{
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: Arial, sans-serif;
      color: #d6e3f5;
      background: linear-gradient(180deg, rgba(6, 15, 28, 0.96), rgba(4, 10, 20, 0.98));
      text-align: center;
      padding: 24px;
    }}
    .tv-fallback a {{
      color: #87f5d3;
    }}
  </style>
</head>
<body>
  <div id="tv-wrap">
    <div id="tv-chart"></div>
  </div>
  <script>
    function renderFallback() {{
      const wrap = document.getElementById("tv-wrap");
      wrap.innerHTML = '<div class="tv-fallback"><div><div style="font-size:20px;font-weight:700;margin-bottom:10px;">TradingView chart failed to load</div><div style="font-size:13px;opacity:0.8;margin-bottom:12px;">Open the symbol directly on TradingView while the app stays usable.</div><a href="https://www.tradingview.com/chart/?symbol={symbol}" target="_blank">Open {symbol} on TradingView</a></div></div>';
    }}

    function bootChart() {{
      if (!window.TradingView) {{
        renderFallback();
        return;
      }}
      new TradingView.widget({{
        autosize: true,
        symbol: "{symbol}",
        interval: "{interval}",
        timezone: "Etc/UTC",
        theme: "dark",
        style: "1",
        locale: "en",
        enable_publishing: false,
        allow_symbol_change: true,
        withdateranges: true,
        hide_side_toolbar: false,
        details: true,
        hotlist: false,
        calendar: false,
        studies: ["RSI@tv-basicstudies", "MACD@tv-basicstudies", "BB@tv-basicstudies"],
        container_id: "tv-chart",
      }});
    }}

    const script = document.createElement("script");
    script.src = "https://s3.tradingview.com/tv.js";
    script.async = true;
    script.onload = bootChart;
    script.onerror = renderFallback;
    document.head.appendChild(script);
  </script>
</body>
</html>
"""


def resolve_symbol_context(pair_name: str, tf_name: str) -> tuple[str, str]:
    return SYMBOLS[pair_name], YF_SYMBOLS[SYMBOLS[pair_name]]


def analyze_market(pair_name: str, tf_name: str, mode: str) -> tuple[dict | None, dict | None]:
    symbol_tv, symbol_yf = resolve_symbol_context(pair_name, tf_name)
    market = load_ohlcv(symbol_yf, YF_INTERVALS[tf_name])
    if market.empty:
        return None, None

    news_items, news_summary = fetch_news_cached(pair_name)
    technical = TechnicalAnalyzer(market)
    patterns = PatternDetector(market)
    schools = TradingSchoolsAnalyzer(market)
    engine = AISignalEngine(market, technical, patterns, schools, news_summary)
    signal = engine.generate_signal(mode=mode)

    details = {
        "technical_snapshot": technical.get_indicators_snapshot(),
        "support_levels": technical.support_levels,
        "resistance_levels": technical.resistance_levels,
        "trendline": technical.trendline,
        "patterns": patterns.detected_patterns,
        "schools": {
            "smc": schools.smc_analysis,
            "ict": schools.ict_analysis,
            "sk": schools.sk_analysis,
            "ta": schools.ta_summary,
        },
        "news_summary": news_summary,
    }
    st.session_state.news_data = news_items
    st.session_state.news_summary = news_summary
    return signal, details


def refresh_news_if_needed(pair_name: str) -> None:
    if st.session_state.get("selected_pair") != pair_name or not st.session_state.news_data:
        items, summary = fetch_news_cached(pair_name)
        st.session_state.news_data = items
        st.session_state.news_summary = summary


def render_app_header(pair_name: str, tf_name: str, mode_cfg: dict) -> None:
    timestamp = datetime.now(timezone.utc).strftime("%A, %d %B %Y · %H:%M UTC")
    st.markdown(
        f"""
        <section class="hero-shell">
          <div class="hero-left">
            <div class="eyebrow">NEXUS TRADING INTELLIGENCE</div>
            <h1>Future-grade discretionary dashboard.</h1>
            <p>Live charting, pair-aware market news, and transparent confluence analysis built around {pair_name} on {tf_name}.</p>
          </div>
          <div class="hero-right">
            <div class="hero-badge">Mode · {mode_cfg["label"]}</div>
            <div class="hero-stat">{timestamp}</div>
            <div class="hero-substat">Aggressive signal policy with explicit conflict visibility</div>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_signal_card(result: dict, summary: dict) -> None:
    decision = result["decision"]
    palette = {
        "BUY": ("#87f5d3", "rgba(135,245,211,0.18)", "Bullish opportunity"),
        "SELL": ("#ff8b9f", "rgba(255,139,159,0.18)", "Bearish opportunity"),
        "WAIT": ("#ffd287", "rgba(255,210,135,0.18)", "Wait for alignment"),
    }
    accent, wash, label = palette.get(decision, palette["WAIT"])
    st.markdown(
        f"""
        <section class="signal-card" style="--signal-accent:{accent}; --signal-wash:{wash};">
          <div class="signal-top">
            <div>
              <div class="signal-label">{label}</div>
              <div class="signal-action">{decision}</div>
            </div>
            <div class="signal-score">
              <span>Confidence</span>
              <strong>{result["confidence"]}%</strong>
            </div>
          </div>
          <div class="signal-grid">
            <div><span>Bias</span><strong>{result["bias"]}</strong></div>
            <div><span>Confluence</span><strong>{result["confluence_score"]}</strong></div>
            <div><span>R/R</span><strong>1:{result["rr"]}</strong></div>
            <div><span>News Impact</span><strong>{result["news_impact"]}</strong></div>
            <div><span>Entry</span><strong>{result["entry"]}</strong></div>
            <div><span>Entry Zone</span><strong>{result["entry_zone"]}</strong></div>
            <div><span>Stop Loss</span><strong>{result["sl"]}</strong></div>
            <div><span>Take Profit</span><strong>{result["tp"]}</strong></div>
          </div>
          <div class="signal-note">{result["reason"]}</div>
          <div class="signal-foot">
            <div><span>Invalidation</span><strong>{result["invalidations"]}</strong></div>
            <div><span>TP/SL Logic</span><strong>{result["tp_sl_rationale"]}</strong></div>
            <div><span>News Headline</span><strong>{summary.get("headline", "No reliable live news available right now.")}</strong></div>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_signal_details(details: list[dict]) -> None:
    for item in details:
        direction = item.get("direction", "conflict")
        accent = {"bullish": "#87f5d3", "bearish": "#ff8b9f", "conflict": "#9db3cc"}.get(direction, "#9db3cc")
        badge = {"bullish": "Bullish", "bearish": "Bearish", "conflict": "Mixed"}.get(direction, "Mixed")
        width = min(100, max(10, item.get("strength", 0)))
        st.markdown(
            f"""
            <div class="detail-card">
              <div class="detail-header">
                <div class="detail-title">{item.get("signal", "")}</div>
                <div class="detail-badge" style="color:{accent}; border-color:{accent}40; background:{accent}18;">{badge}</div>
              </div>
              <div class="detail-desc">{item.get("desc", "")}</div>
              <div class="detail-meter"><span style="width:{width}%; background:{accent};"></span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_news(news_items: list[dict]) -> None:
    if not news_items:
        st.markdown(
            """
            <div class="empty-news">
              <div class="empty-news-title">No reliable live news available right now.</div>
              <div class="empty-news-copy">The dashboard will keep the analysis available, but it will not fabricate headlines when the feed is unavailable.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    sentiment_map = {
        "positive": ("#87f5d3", "Bullish"),
        "negative": ("#ff8b9f", "Bearish"),
        "neutral": ("#ffd287", "Neutral"),
    }
    for item in news_items[:5]:
        color, label = sentiment_map.get(item.get("sentiment", "neutral"), sentiment_map["neutral"])
        description = item.get("description", "").strip() or "Open the source article for more context."
        link = item.get("url", "")
        cta = f'<a href="{link}" target="_blank">Source</a>' if link else "<span>Source unavailable</span>"
        st.markdown(
            f"""
            <article class="news-card">
              <div class="news-top">
                <span class="news-badge" style="color:{color}; border-color:{color}55; background:{color}18;">{label}</span>
                <span class="news-meta">{item.get("impact_label", "Low")} impact · {item.get("published", "Recent")}</span>
              </div>
              <h4>{item.get("title", "")}</h4>
              <p>{description[:180]}</p>
              <div class="news-bottom">
                <span>{item.get("source", "News")}</span>
                {cta}
              </div>
            </article>
            """,
            unsafe_allow_html=True,
        )


def render_mode_caption(active_mode: str) -> None:
    copy = {
        "SMART": "Fuses structure, momentum, harmonics, and live news into one aggressive decision stack.",
        "SMC": "Focuses on BOS, order blocks, liquidity context, and institutional structure cues.",
        "ICT": "Prioritizes imbalance, structure shifts, and entry timing logic through ICT-style context.",
        "SK": "Keeps trend and pullback logic cleaner with momentum-following structure confirmation.",
    }
    st.markdown(
        f"""
        <div class="mode-caption">
          <div class="mode-caption-label">{MODES[active_mode]["icon"]} mode</div>
          <div class="mode-caption-copy">{copy[active_mode]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


init_state()

if st.session_state.current_page == "chart":
    col_back, col_title, col_pair, col_tf = st.columns([0.8, 2.7, 1.5, 1.2])
    with col_back:
        if st.button("Back", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()
    with col_title:
        st.markdown('<div class="fullscreen-label">Immersive TradingView workspace</div>', unsafe_allow_html=True)
    with col_pair:
        pair_name = st.selectbox("Pair", list(SYMBOLS.keys()), key="fs_pair", label_visibility="collapsed")
    with col_tf:
        tf_name = st.selectbox("TF", list(TV_INTERVALS.keys()), index=3, key="fs_tf", label_visibility="collapsed")

    symbol_tv = SYMBOLS[pair_name]
    components.html(build_tradingview_html(symbol_tv, TV_INTERVALS[tf_name], 930), height=930, scrolling=False)
    st.stop()


c1, c2, c3, c4, c5, c6, c7 = st.columns([2.2, 1.1, 0.85, 0.85, 0.85, 0.85, 1.05])
with c1:
    pair_name = st.selectbox("Symbol", list(SYMBOLS.keys()), index=list(SYMBOLS.keys()).index(st.session_state.selected_pair), label_visibility="collapsed")
with c2:
    tf_name = st.selectbox("Timeframe", list(TV_INTERVALS.keys()), index=list(TV_INTERVALS.keys()).index(st.session_state.selected_tf), label_visibility="collapsed")
with c3:
    if st.button("Smart", use_container_width=True, type="primary" if st.session_state.active_mode == "SMART" else "secondary"):
        st.session_state.active_mode = "SMART"
        st.session_state.analysis_result = None
with c4:
    if st.button("SMC", use_container_width=True, type="primary" if st.session_state.active_mode == "SMC" else "secondary"):
        st.session_state.active_mode = "SMC"
        st.session_state.analysis_result = None
with c5:
    if st.button("ICT", use_container_width=True, type="primary" if st.session_state.active_mode == "ICT" else "secondary"):
        st.session_state.active_mode = "ICT"
        st.session_state.analysis_result = None
with c6:
    if st.button("SK", use_container_width=True, type="primary" if st.session_state.active_mode == "SK" else "secondary"):
        st.session_state.active_mode = "SK"
        st.session_state.analysis_result = None
with c7:
    if st.button("Full Chart", use_container_width=True):
        st.session_state.current_page = "chart"
        st.rerun()

if pair_name != st.session_state.selected_pair or tf_name != st.session_state.selected_tf:
    st.session_state.selected_pair = pair_name
    st.session_state.selected_tf = tf_name
    st.session_state.analysis_result = None
    st.session_state.analysis_details = None

refresh_news_if_needed(pair_name)
mode_cfg = MODES[st.session_state.active_mode]
render_app_header(pair_name, tf_name, mode_cfg)
render_mode_caption(st.session_state.active_mode)

symbol_tv, _ = resolve_symbol_context(pair_name, tf_name)
chart_col, side_col = st.columns([2.35, 1.05], gap="large")

with chart_col:
    st.markdown('<div class="section-label">Live chart</div>', unsafe_allow_html=True)
    components.html(build_tradingview_html(symbol_tv, TV_INTERVALS[tf_name], 760), height=760, scrolling=False)

    analyze_key = f"{pair_name}|{tf_name}|{st.session_state.active_mode}"
    if st.button(f"Run {mode_cfg['label']} Analysis", type="primary", use_container_width=True):
        with st.spinner("Building live market context and recalculating confluence..."):
            result, details = analyze_market(pair_name, tf_name, st.session_state.active_mode)
            if not result:
                st.error("Failed to load market data for this symbol/timeframe.")
            else:
                st.session_state.analysis_result = result
                st.session_state.analysis_details = details
                st.session_state.last_analysis_key = analyze_key

    if st.session_state.analysis_result and st.session_state.last_analysis_key == analyze_key:
        render_signal_card(st.session_state.analysis_result, st.session_state.news_summary)
        with st.expander("Signal breakdown", expanded=True):
            render_signal_details(st.session_state.analysis_result.get("details", []))
        with st.expander("Raw market context"):
            st.json(st.session_state.analysis_details)

with side_col:
    st.markdown(
        f"""
        <section class="glass-panel">
          <div class="panel-label">Market overview</div>
          <div class="overview-symbol">{pair_name}</div>
          <div class="overview-row"><span>TradingView</span><strong>{symbol_tv}</strong></div>
          <div class="overview-row"><span>Timeframe</span><strong>{tf_name}</strong></div>
          <div class="overview-row"><span>Mode</span><strong style="color:{mode_cfg['color']};">{mode_cfg['label']}</strong></div>
          <div class="overview-row"><span>News bias</span><strong>{st.session_state.news_summary.get('sentiment', 'neutral').title()}</strong></div>
          <div class="overview-row"><span>News impact</span><strong>{st.session_state.news_summary.get('impact_label', 'Unknown')}</strong></div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.analysis_result:
        result = st.session_state.analysis_result
        st.markdown(
            f"""
            <section class="glass-panel">
              <div class="panel-label">Execution snapshot</div>
              <div class="overview-row"><span>Decision</span><strong>{result['decision']}</strong></div>
              <div class="overview-row"><span>Confidence</span><strong>{result['confidence']}%</strong></div>
              <div class="overview-row"><span>Confluence</span><strong>{result['confluence_score']}</strong></div>
              <div class="overview-row"><span>Conflicts</span><strong>{result['conflicts']}</strong></div>
              <div class="overview-row"><span>Entry zone</span><strong>{result['entry_zone']}</strong></div>
              <div class="overview-row"><span>Invalidation</span><strong>{result['invalidations']}</strong></div>
            </section>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-label">Relevant market news</div>', unsafe_allow_html=True)
    render_news(st.session_state.news_data)

    st.markdown(
        """
        <section class="disclaimer-card">
          <div class="panel-label">Risk disclosure</div>
          <p>This dashboard improves signal quality and transparency, but it is still not guaranteed financial advice. Always confirm the setup, size risk carefully, and avoid relying on one model output alone.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
