import streamlit as st


def inject_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

        :root {
            --bg-main: #040914;
            --bg-soft: rgba(11, 21, 38, 0.84);
            --bg-card: rgba(10, 19, 34, 0.72);
            --line-soft: rgba(157, 179, 204, 0.16);
            --text-main: #f4f8ff;
            --text-soft: #9fb2ca;
            --accent: #87f5d3;
            --danger: #ff8b9f;
            --warning: #ffd287;
        }

        html, body, [class*="css"] {
            font-family: 'Manrope', sans-serif !important;
            color: var(--text-main) !important;
            background:
                radial-gradient(circle at top left, rgba(135, 245, 211, 0.11), transparent 24%),
                radial-gradient(circle at top right, rgba(133, 168, 255, 0.16), transparent 28%),
                linear-gradient(180deg, #07111d 0%, var(--bg-main) 46%, #03070f 100%) !important;
        }

        .stApp {
            background: transparent !important;
        }

        .main .block-container {
            max-width: 100%;
            padding: 1.4rem 1.9rem 2.6rem 1.9rem;
        }

        #MainMenu, footer, header { visibility: hidden; }
        .stDeployButton, [data-testid="stToolbar"] { display: none !important; }

        [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] {
            gap: 0.65rem;
        }

        [data-testid="stSelectbox"] > div > div,
        [data-testid="stBaseButton-secondary"],
        [data-testid="stBaseButton-primary"],
        .stButton > button {
            border-radius: 18px !important;
        }

        [data-testid="stSelectbox"] > div > div {
            min-height: 52px;
            background: rgba(8, 17, 31, 0.84) !important;
            border: 1px solid var(--line-soft) !important;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.04), 0 16px 32px rgba(0,0,0,0.22) !important;
            color: var(--text-main) !important;
        }

        [data-testid="stSelectbox"] > div > div:hover {
            border-color: rgba(135, 245, 211, 0.42) !important;
        }

        [data-testid="stSelectbox"] label {
            display: none !important;
        }

        .stButton > button {
            min-height: 50px;
            border: 1px solid var(--line-soft) !important;
            background: linear-gradient(180deg, rgba(12, 22, 39, 0.88), rgba(8, 15, 27, 0.92)) !important;
            color: var(--text-main) !important;
            font-weight: 700 !important;
            letter-spacing: 0.01em;
            transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease !important;
            box-shadow: 0 12px 26px rgba(0, 0, 0, 0.24) !important;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            border-color: rgba(135, 245, 211, 0.34) !important;
            box-shadow: 0 18px 36px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(135, 245, 211, 0.08) inset !important;
        }

        .stButton > button[kind="primary"] {
            color: #06111a !important;
            border-color: rgba(135, 245, 211, 0.65) !important;
            background: linear-gradient(135deg, #87f5d3 0%, #a7ffe2 45%, #d8fff4 100%) !important;
            box-shadow: 0 18px 44px rgba(135, 245, 211, 0.22) !important;
        }

        .stButton > button[kind="primary"]:hover {
            border-color: rgba(215, 255, 244, 0.9) !important;
        }

        [data-testid="stExpander"] {
            background: rgba(8, 17, 31, 0.72) !important;
            border: 1px solid var(--line-soft) !important;
            border-radius: 24px !important;
            overflow: hidden;
            backdrop-filter: blur(18px);
        }

        [data-testid="stExpander"] summary {
            padding: 1rem 1.1rem !important;
            font-weight: 700 !important;
            color: var(--text-main) !important;
        }

        [data-testid="stExpanderDetails"] {
            padding: 0.3rem 1rem 1rem 1rem !important;
        }

        [data-testid="stJson"] {
            background: rgba(4, 10, 18, 0.96) !important;
            border: 1px solid var(--line-soft) !important;
            border-radius: 18px !important;
            font-family: 'IBM Plex Mono', monospace !important;
        }

        .stSpinner > div {
            border-color: var(--accent) !important;
        }

        [data-testid="stAlert"] {
            border-radius: 18px !important;
            border: 1px solid var(--line-soft) !important;
            background: rgba(12, 22, 39, 0.86) !important;
        }

        iframe {
            border: 1px solid rgba(157, 179, 204, 0.16) !important;
            border-radius: 28px !important;
            box-shadow: 0 24px 60px rgba(0,0,0,0.32) !important;
        }

        .hero-shell,
        .glass-panel,
        .signal-card,
        .disclaimer-card,
        .mode-caption,
        .detail-card,
        .news-card,
        .empty-news {
            border: 1px solid var(--line-soft);
            background: linear-gradient(180deg, rgba(11, 20, 36, 0.78), rgba(7, 14, 26, 0.88));
            box-shadow: 0 18px 48px rgba(0, 0, 0, 0.28), inset 0 1px 0 rgba(255,255,255,0.03);
            backdrop-filter: blur(18px);
        }

        .hero-shell {
            display: grid;
            grid-template-columns: 1.7fr 1fr;
            gap: 1rem;
            padding: 1.5rem;
            margin-bottom: 0.6rem;
            border-radius: 30px;
            position: relative;
            overflow: hidden;
        }

        .hero-shell::before {
            content: "";
            position: absolute;
            inset: -30% auto auto -10%;
            width: 240px;
            height: 240px;
            background: radial-gradient(circle, rgba(135,245,211,0.18), transparent 68%);
            pointer-events: none;
        }

        .hero-left h1 {
            margin: 0.2rem 0 0.55rem 0;
            font-size: 2.5rem;
            line-height: 1.05;
            letter-spacing: -0.04em;
        }

        .hero-left p,
        .hero-substat,
        .mode-caption-copy,
        .detail-desc,
        .disclaimer-card p,
        .news-card p,
        .empty-news-copy {
            color: var(--text-soft);
            line-height: 1.6;
            margin: 0;
        }

        .eyebrow,
        .panel-label,
        .section-label,
        .signal-label,
        .mode-caption-label,
        .fullscreen-label {
            color: var(--text-soft);
            text-transform: uppercase;
            font-size: 0.72rem;
            letter-spacing: 0.16em;
            font-weight: 800;
        }

        .hero-right {
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 0.7rem;
            align-items: flex-start;
        }

        .hero-badge,
        .hero-stat {
            padding: 0.72rem 0.95rem;
            border-radius: 16px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.06);
        }

        .hero-badge {
            color: var(--accent);
            font-weight: 800;
        }

        .hero-stat {
            font-size: 0.95rem;
            color: var(--text-main);
            font-weight: 700;
        }

        .mode-caption {
            border-radius: 24px;
            padding: 1rem 1.15rem;
            margin-bottom: 0.4rem;
        }

        .glass-panel,
        .disclaimer-card {
            border-radius: 26px;
            padding: 1.05rem 1.1rem;
            margin-bottom: 0.45rem;
        }

        .overview-symbol {
            font-size: 1.65rem;
            font-weight: 800;
            margin: 0.2rem 0 0.75rem 0;
            letter-spacing: -0.03em;
        }

        .overview-row,
        .news-top,
        .news-bottom,
        .detail-header,
        .signal-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.6rem;
        }

        .overview-row {
            padding: 0.62rem 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            font-size: 0.92rem;
        }

        .overview-row:last-child {
            border-bottom: none;
            padding-bottom: 0;
        }

        .overview-row span,
        .signal-grid span,
        .signal-score span,
        .signal-foot span,
        .news-meta {
            color: var(--text-soft);
        }

        .overview-row strong,
        .signal-grid strong,
        .signal-score strong,
        .signal-foot strong {
            font-weight: 700;
        }

        .signal-card {
            margin-top: 0.75rem;
            border-radius: 30px;
            padding: 1.3rem;
            position: relative;
            overflow: hidden;
        }

        .signal-card::before {
            content: "";
            position: absolute;
            inset: 0 auto auto 0;
            width: 100%;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--signal-accent), transparent);
        }

        .signal-action {
            font-size: 3rem;
            line-height: 1;
            font-weight: 800;
            margin-top: 0.35rem;
            color: var(--signal-accent);
            letter-spacing: -0.05em;
        }

        .signal-score {
            min-width: 148px;
            padding: 0.95rem 1rem;
            border-radius: 22px;
            background: var(--signal-wash);
            text-align: right;
        }

        .signal-score strong {
            display: block;
            font-size: 2rem;
            color: var(--signal-accent);
        }

        .signal-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.8rem;
            margin: 1rem 0;
        }

        .signal-grid > div,
        .signal-foot > div {
            padding: 0.9rem 0.95rem;
            border-radius: 20px;
            background: rgba(255,255,255,0.035);
            border: 1px solid rgba(255,255,255,0.05);
        }

        .signal-grid strong,
        .signal-foot strong {
            display: block;
            margin-top: 0.32rem;
            color: var(--text-main);
        }

        .signal-note {
            padding: 0.9rem 1rem;
            border-radius: 20px;
            background: rgba(255,255,255,0.035);
            border: 1px solid rgba(255,255,255,0.05);
            color: var(--text-main);
            margin-bottom: 0.95rem;
        }

        .signal-foot {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.8rem;
        }

        .detail-card,
        .news-card,
        .empty-news {
            border-radius: 24px;
            padding: 0.95rem 1rem;
            margin-bottom: 0.6rem;
        }

        .detail-title,
        .news-card h4 {
            font-size: 1rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin: 0;
        }

        .detail-badge,
        .news-badge {
            border: 1px solid;
            border-radius: 999px;
            padding: 0.28rem 0.62rem;
            font-size: 0.72rem;
            font-weight: 800;
        }

        .detail-meter {
            height: 6px;
            border-radius: 999px;
            background: rgba(255,255,255,0.06);
            margin-top: 0.8rem;
            overflow: hidden;
        }

        .detail-meter span {
            display: block;
            height: 100%;
            border-radius: inherit;
        }

        .news-card h4 {
            margin: 0.75rem 0 0.4rem 0;
            line-height: 1.35;
        }

        .news-bottom {
            margin-top: 0.8rem;
            font-size: 0.84rem;
        }

        .news-bottom a {
            color: var(--accent);
            text-decoration: none;
            font-weight: 700;
        }

        .empty-news-title {
            font-size: 1rem;
            font-weight: 800;
            margin-bottom: 0.35rem;
        }

        .fullscreen-label {
            padding-top: 0.65rem;
        }

        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(157, 179, 204, 0.24);
            border-radius: 999px;
        }

        @media (max-width: 1100px) {
            .hero-shell,
            .signal-foot,
            .signal-grid {
                grid-template-columns: 1fr !important;
            }

            .hero-left h1 {
                font-size: 2rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
