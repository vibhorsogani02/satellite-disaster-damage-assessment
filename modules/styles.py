"""
UI styling for the Satellite Disaster Damage Assessment dashboard.

Usage (in app.py, right after st.set_page_config):

    from modules.styles import inject_css, apply_chart_theme, render_hero
    inject_css()
    apply_chart_theme()
    render_hero()
"""

import streamlit as st
import matplotlib.pyplot as plt


# ------------------------------------------------------------------
# Colour palette (single place to tweak the whole look)
# ------------------------------------------------------------------
BG = "#0b1120"
SURFACE = "#111a2e"
SURFACE_2 = "#16223b"
BORDER = "rgba(148, 163, 184, 0.16)"
TEXT = "#e2e8f0"
MUTED = "#94a3b8"
ACCENT = "#22d3ee"      # cyan
ACCENT_2 = "#6366f1"    # indigo
CHART_COLORS = ["#22d3ee", "#6366f1", "#f59e0b", "#ef4444", "#10b981"]


CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap');

:root {{
    --bg: {BG};
    --surface: {SURFACE};
    --surface-2: {SURFACE_2};
    --border: {BORDER};
    --text: {TEXT};
    --muted: {MUTED};
    --accent: {ACCENT};
    --accent-2: {ACCENT_2};
    --radius: 16px;
}}

/* ---------- Base ---------- */
html, body, [class*="css"], .stApp {{
    font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif;
}}

.stApp {{
    background:
        radial-gradient(900px 500px at 8% -10%, rgba(34, 211, 238, 0.10), transparent 60%),
        radial-gradient(800px 500px at 100% 0%, rgba(99, 102, 241, 0.12), transparent 60%),
        var(--bg);
    color: var(--text);
}}

/* Hide default Streamlit chrome */
#MainMenu, footer {{ visibility: hidden; }}
[data-testid="stHeader"] {{ background: transparent; }}

.block-container {{
    max-width: 1180px;
    padding-top: 2.2rem;
    padding-bottom: 4rem;
}}

/* ---------- Hero ---------- */
.hero {{
    position: relative;
    overflow: hidden;
    padding: 2.4rem 2.6rem;
    margin-bottom: 1.6rem;
    border-radius: 22px;
    border: 1px solid var(--border);
    background:
        linear-gradient(135deg, rgba(34, 211, 238, 0.14), rgba(99, 102, 241, 0.18)),
        var(--surface);
    box-shadow: 0 20px 50px -20px rgba(0, 0, 0, 0.65);
}}
.hero::after {{
    content: "";
    position: absolute;
    right: -60px; top: -60px;
    width: 260px; height: 260px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(34, 211, 238, 0.28), transparent 70%);
    pointer-events: none;
}}
.hero-badge {{
    display: inline-block;
    padding: 0.28rem 0.8rem;
    margin-bottom: 0.9rem;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent);
    background: rgba(34, 211, 238, 0.10);
    border: 1px solid rgba(34, 211, 238, 0.35);
    border-radius: 999px;
}}
.hero h1 {{
    margin: 0 0 0.6rem 0;
    padding: 0;
    font-size: 2.4rem;
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: -0.02em;
    background: linear-gradient(90deg, #ffffff 0%, #a5f3fc 60%, #c7d2fe 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}}
.hero p {{
    margin: 0;
    max-width: 680px;
    font-size: 1.02rem;
    line-height: 1.65;
    color: var(--muted);
}}
.hero-steps {{
    display: flex; flex-wrap: wrap; gap: 0.6rem;
    margin-top: 1.4rem;
}}
.hero-chip {{
    padding: 0.35rem 0.85rem;
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--text);
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--border);
    border-radius: 999px;
}}

/* ---------- Headings ---------- */
h1, h2, h3, h4 {{
    font-family: 'Inter', sans-serif;
    color: #f8fafc;
    letter-spacing: -0.01em;
}}

h2 {{
    position: relative;
    margin-top: 2.6rem !important;
    padding: 0.2rem 0 0.2rem 1rem !important;
    font-size: 1.55rem !important;
    font-weight: 700 !important;
}}
h2::before {{
    content: "";
    position: absolute;
    left: 0; top: 0.35rem; bottom: 0.35rem;
    width: 4px;
    border-radius: 4px;
    background: linear-gradient(180deg, var(--accent), var(--accent-2));
}}

h3 {{ font-size: 1.15rem !important; font-weight: 600 !important; color: #e2e8f0; }}

hr {{
    margin: 2rem 0 !important;
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(148, 163, 184, 0.35), transparent) !important;
}}

/* ---------- File uploader ---------- */
[data-testid="stFileUploader"] label p {{
    font-weight: 600;
    color: var(--text);
}}
[data-testid="stFileUploader"] section {{
    padding: 1.3rem;
    background: var(--surface);
    border: 2px dashed rgba(34, 211, 238, 0.35);
    border-radius: var(--radius);
    transition: all 0.2s ease;
}}
[data-testid="stFileUploader"] section:hover {{
    border-color: var(--accent);
    background: var(--surface-2);
    box-shadow: 0 0 0 4px rgba(34, 211, 238, 0.08);
}}
[data-testid="stFileUploader"] button {{
    border-radius: 10px;
    border: 1px solid rgba(34, 211, 238, 0.5);
    color: var(--accent);
    background: transparent;
}}

/* ---------- Metric cards ---------- */
[data-testid="stMetric"] {{
    padding: 1.1rem 1.3rem;
    background: linear-gradient(160deg, var(--surface-2), var(--surface));
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: 0 10px 25px -15px rgba(0, 0, 0, 0.7);
    transition: transform 0.18s ease, border-color 0.18s ease;
}}
[data-testid="stMetric"]:hover {{
    transform: translateY(-3px);
    border-color: rgba(34, 211, 238, 0.45);
}}
[data-testid="stMetricLabel"] p {{
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--muted) !important;
}}
[data-testid="stMetricValue"] {{
    font-size: 1.9rem !important;
    font-weight: 800 !important;
    color: var(--accent) !important;
}}

/* ---------- Images ---------- */
[data-testid="stImage"] img {{
    border-radius: 14px;
    border: 1px solid var(--border);
    box-shadow: 0 14px 30px -18px rgba(0, 0, 0, 0.85);
}}
[data-testid="stImageCaption"], [data-testid="stCaptionContainer"] {{
    color: var(--muted);
    font-size: 0.82rem;
    text-align: center;
}}

/* ---------- Buttons ---------- */
.stButton > button,
[data-testid="stDownloadButton"] > button {{
    padding: 0.6rem 1.4rem;
    font-weight: 600;
    color: #06202a;
    background: linear-gradient(90deg, var(--accent), #38bdf8);
    border: none;
    border-radius: 12px;
    box-shadow: 0 8px 20px -8px rgba(34, 211, 238, 0.6);
    transition: all 0.18s ease;
}}
.stButton > button:hover,
[data-testid="stDownloadButton"] > button:hover {{
    color: #06202a;
    transform: translateY(-2px);
    box-shadow: 0 12px 26px -8px rgba(34, 211, 238, 0.85);
    filter: brightness(1.08);
}}
.stButton > button p,
[data-testid="stDownloadButton"] > button p {{ color: #06202a; font-weight: 700; }}

/* ---------- Alerts ---------- */
[data-testid="stAlert"] {{
    border-radius: 14px;
    border: 1px solid var(--border);
    backdrop-filter: blur(6px);
}}

/* ---------- Tables ---------- */
[data-testid="stDataFrame"] {{
    padding: 4px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
}}

/* ---------- Charts (matplotlib) ---------- */
[data-testid="stImage"] + div, .stPlotlyChart, [data-testid="stPyplot"] {{
    border-radius: var(--radius);
}}

/* ---------- Spinner / misc ---------- */
.stSpinner > div {{ border-top-color: var(--accent) !important; }}
code {{ font-family: 'JetBrains Mono', monospace; color: var(--accent); }}

/* ---------- Scrollbar ---------- */
::-webkit-scrollbar {{ width: 10px; height: 10px; }}
::-webkit-scrollbar-track {{ background: var(--bg); }}
::-webkit-scrollbar-thumb {{
    background: #1f2d4a;
    border-radius: 8px;
}}
::-webkit-scrollbar-thumb:hover {{ background: #2c4170; }}

/* ---------- Mobile ---------- */
@media (max-width: 640px) {{
    .hero {{ padding: 1.6rem 1.3rem; }}
    .hero h1 {{ font-size: 1.7rem; }}
    h2 {{ font-size: 1.3rem !important; }}
}}
</style>
"""



PREMIUM_CSS = """
<style>
.block-container {max-width:1440px;padding-left:2.4rem;padding-right:2.4rem;}
[data-testid="stSidebar"] {background:linear-gradient(180deg,#080d1b 0%,#101a30 55%,#0b1222 100%);border-right:1px solid rgba(148,163,184,.16);}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,[data-testid="stSidebar"] label {color:#cbd5e1;}
.status-ribbon {display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:0 0 1.3rem;padding:.72rem 1rem;border:1px solid rgba(148,163,184,.16);border-radius:12px;background:linear-gradient(90deg,rgba(34,211,238,.08),rgba(99,102,241,.08));color:#a5b4c8;font-size:.68rem;font-weight:800;letter-spacing:.13em;}
.status-dot {width:8px;height:8px;border-radius:50%;background:#34d399;box-shadow:0 0 12px #34d399;}
.ribbon-separator {color:#475569;}.ribbon-spacer {flex:1;}.live-label {color:#6ee7b7;letter-spacing:.08em;}
.section-kicker {margin-top:1.4rem;color:#67e8f9;font-size:.68rem;font-weight:800;letter-spacing:.2em;}
.kpi-grid {display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:1rem 0 1.35rem;}
.kpi-card {min-height:135px;padding:20px 20px 16px;border-radius:17px;border:1px solid rgba(148,163,184,.17);background:linear-gradient(145deg,rgba(30,41,69,.92),rgba(13,22,41,.96));box-shadow:0 14px 35px rgba(0,0,0,.20);position:relative;overflow:hidden;}
.kpi-card:after {content:"";position:absolute;right:-28px;top:-38px;width:110px;height:110px;border-radius:50%;background:rgba(34,211,238,.07);}
.kpi-label {font-size:.66rem;font-weight:800;letter-spacing:.14em;color:#94a3b8;}
.kpi-value {margin-top:13px;color:#f8fafc;font-size:2rem;font-weight:850;line-height:1.1;letter-spacing:-.04em;}
.kpi-value span {font-size:1.05rem;color:#67e8f9;margin-left:3px;}.kpi-foot {margin-top:9px;color:#8191aa;font-size:.73rem;}
.severity-row {margin:0 0 16px;}.severity-head {display:flex;justify-content:space-between;gap:10px;color:#cbd5e1;font-size:.82rem;margin-bottom:7px;}
.severity-head strong {color:#f8fafc;font-size:.78rem;}.severity-track {height:8px;background:#1e293b;border-radius:99px;overflow:hidden;}
.severity-fill {height:100%;border-radius:99px;box-shadow:0 0 12px rgba(255,255,255,.12);}
.info-panel {padding:15px 17px;border:1px solid rgba(148,163,184,.16);border-radius:14px;background:rgba(15,23,42,.68);}
.info-panel div {display:flex;justify-content:space-between;gap:12px;padding:9px 0;border-bottom:1px solid rgba(148,163,184,.10);font-size:.78rem;}
.info-panel div:last-child {border:0;}.info-panel span {color:#94a3b8;}.info-panel strong {color:#e2e8f0;text-align:right;}
[data-testid="stTabs"] button {font-weight:700;}
[data-testid="stExpander"] {border:1px solid rgba(148,163,184,.17);border-radius:14px;background:rgba(15,23,42,.45);}
.stProgress > div > div > div > div {background:linear-gradient(90deg,#22d3ee,#818cf8);}
@media(max-width:900px){.kpi-grid{grid-template-columns:repeat(2,minmax(0,1fr));}.block-container{padding-left:1rem;padding-right:1rem;}}
@media(max-width:520px){.kpi-grid{grid-template-columns:1fr;}.status-ribbon{font-size:.58rem;}}
</style>
"""

def inject_css():
    """Inject the dashboard stylesheet into the Streamlit page."""
    st.markdown(CSS + PREMIUM_CSS, unsafe_allow_html=True)


def apply_chart_theme():
    """Make every matplotlib chart match the dark dashboard theme."""
    plt.rcParams.update({
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "axes.edgecolor": "#334155",
        "axes.labelcolor": TEXT,
        "axes.titlecolor": "#f8fafc",
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.titlepad": 14,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": "#22304f",
        "grid.linestyle": "--",
        "grid.alpha": 0.7,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "text.color": TEXT,
        "font.family": "sans-serif",
        "axes.prop_cycle": plt.cycler(color=CHART_COLORS),
    })


def render_hero():
    """Top banner shown above the uploaders."""
    st.markdown(
        """
        <div class="hero">
            <span class="hero-badge">🛰️ Remote Sensing · Computer Vision</span>
            <h1>Satellite-Based Disaster Damage Assessment</h1>
            <p>
                Upload before and after disaster satellite images to detect changes,
                identify affected regions, and classify disaster damage.
            </p>
            <div class="hero-steps">
                <span class="hero-chip">① Register</span>
                <span class="hero-chip">② Enhance</span>
                <span class="hero-chip">③ Detect Changes</span>
                <span class="hero-chip">④ Segment</span>
                <span class="hero-chip">⑤ Classify Damage</span>
                <span class="hero-chip">⑥ Report</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
