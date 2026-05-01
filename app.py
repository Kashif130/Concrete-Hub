import streamlit as st
import random
import base64
from pathlib import Path
from PIL import Image
import io

# ── PAGE CONFIG ────────────────────────────────────────────
st.set_page_config(
    page_title="Concrete.xyz Hub 🗿",
    page_icon="🗿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── LANGUAGE SETUP ─────────────────────────────────────────
if "lang" not in st.session_state:
    st.session_state.lang = "en"

def t(en_text, ur_text):
    return en_text if st.session_state.lang == "en" else ur_text

# ── CUSTOM CSS ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Space+Grotesk:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: #07100E;
    color: #D0E8DF;
}

/* Main background */
.stApp {
    background: #07100E;
    background-image:
        radial-gradient(ellipse at 0% 0%, rgba(26,232,160,0.08) 0%, transparent 55%),
        radial-gradient(ellipse at 100% 100%, rgba(10,80,50,0.15) 0%, transparent 55%);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(7,16,14,0.97) !important;
    border-right: 1px solid rgba(26,232,160,0.1);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03);
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #4A7A6A;
    border-radius: 8px;
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    border: none;
    padding: 8px 18px;
}
.stTabs [aria-selected="true"] {
    background: #1AE8A0 !important;
    color: #0A1A14 !important;
}

/* Buttons */
.stButton > button {
    background: rgba(26,232,160,0.1);
    color: #1AE8A0;
    border: 1px solid rgba(26,232,160,0.3);
    border-radius: 8px;
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.06em;
    transition: all 0.2s;
    width: 100%;
}
.stButton > button:hover {
    background: rgba(26,232,160,0.2);
    border-color: #1AE8A0;
    color: #0A1A14;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: rgba(26,232,160,0.05);
    border: 1px solid rgba(26,232,160,0.15);
    border-radius: 12px;
    padding: 16px 20px;
}
[data-testid="stMetricValue"] {
    color: #1AE8A0;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 22px;
    font-weight: 800;
}
[data-testid="stMetricLabel"] {
    color: #4A7A6A;
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

/* Radio buttons */
[data-testid="stRadio"] label {
    color: #C0D8CF;
    font-size: 14px;
}

/* Selectbox */
[data-testid="stSelectbox"] > div {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(26,232,160,0.15);
    border-radius: 7px;
    color: #D0E8DF;
}

/* Text input */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(26,232,160,0.15);
    border-radius: 7px;
    color: #D0E8DF;
    font-family: 'Space Grotesk', sans-serif;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(26,232,160,0.02);
    border: 2px dashed rgba(26,232,160,0.25);
    border-radius: 12px;
    padding: 12px;
}

/* Divider */
hr {
    border-color: rgba(26,232,160,0.1);
}

/* Success / info / warning */
.stSuccess {
    background: rgba(26,232,160,0.07) !important;
    border: 1px solid rgba(26,232,160,0.3) !important;
    border-radius: 10px !important;
    color: #1AE8A0 !important;
}
.stInfo {
    background: rgba(77,166,255,0.07) !important;
    border: 1px solid rgba(77,166,255,0.3) !important;
    border-radius: 10px !important;
}
.stWarning {
    background: rgba(255,215,0,0.07) !important;
    border: 1px solid rgba(255,215,0,0.3) !important;
    border-radius: 10px !important;
}

/* Card style helper */
.concrete-card {
    background: rgba(10,24,18,0.85);
    border: 1px solid rgba(26,232,160,0.1);
    border-radius: 14px;
    padding: 22px 26px;
    margin-bottom: 16px;
    backdrop-filter: blur(8px);
}
.card-label {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: #1AE8A0;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 14px;
}
.vault-row {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 8px;
}
.badge-pill {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.08em;
}
</style>
""", unsafe_allow_html=True)

# ── DATA ───────────────────────────────────────────────────
CONCRETE_STATS = {
    "tvl": "$902.3M",
    "processed": "$11.25B",
    "audits": "6",
    "depositors": "100K+",
}

REAL_VAULTS = [
    {"name": "WeETH Vault",          "tvl": "$706M",   "apy": "Institutional", "asset": "weETH",    "chain": "Ethereum",  "badge": "🏦"},
    {"name": "Concrete DeFi USDT",   "tvl": "$62.4M",  "apy": "8.5%",          "asset": "USDT",     "chain": "Ethereum",  "badge": "💰"},
    {"name": "Berachain Bitcoin",     "tvl": "$59.2M",  "apy": "5%",            "asset": "LBTC/WBTC","chain": "Berachain", "badge": "₿"},
    {"name": "Ethena Bera",           "tvl": "$71.6M",  "apy": "0%→Rising",     "asset": "USDe",     "chain": "Berachain", "badge": "🌐"},
    {"name": "WBTC Vault",            "tvl": "$4.3M",   "apy": "7%",            "asset": "WBTC",     "chain": "Ethereum",  "badge": "₿"},
    {"name": "Berachain BERA",        "tvl": "$17K",    "apy": "142%",          "asset": "WBERA",    "chain": "Berachain", "badge": "🐻"},
]

BAGS_ACTIONS = [
    {"action": "Follow @ConcreteXYZ on X",         "bags": "50",      "category": "Social"},
    {"action": "Follow @nic_builds (CEO)",          "bags": "25",      "category": "Social"},
    {"action": "Follow @dill_sl",                   "bags": "25",      "category": "Social"},
    {"action": "Follow @crypttoji",                 "bags": "10",      "category": "Social"},
    {"action": "Join Concrete Discord",             "bags": "50",      "category": "Discord"},
    {"action": "Daily likes on X posts",            "bags": "Daily",   "category": "Social"},
    {"action": "Write quality article",             "bags": "300-500", "category": "Education"},
    {"action": "Create educational thread",         "bags": "200-400", "category": "Education"},
    {"action": "Refer a friend (10% of their bags)","bags": "Ongoing", "category": "Referral"},
    {"action": "Earn Moais role in Discord",        "bags": "Milestone","category": "Discord"},
]

COMMUNITY_TOOLS = [
    {
        "name": "Concrete Vault Intelligence Terminal",
        "url": "https://concrete-vault.streamlit.app",
        "desc": "Advanced vault analytics, yield simulation, TVL tracker, and on-chain data visualizations. Built for power users.",
        "badge": "🗿", "tag": "Analytics", "tag_color": "#1AE8A0",
        "features": ["Vault TVL Charts", "APY Simulator", "Risk Metrics", "On-chain Data"],
    },
    {
        "name": "Concrete Protocol Guide",
        "url": "https://concrete-assistant.streamlit.app/",
        "desc": "Bilingual (English + Urdu) complete knowledge base covering vaults, Bags campaign, airdrop strategies and more.",
        "badge": "🏛️", "tag": "Education", "tag_color": "#FFD700",
        "features": ["Bilingual (EN/UR)", "Bags Guide", "Airdrop Tips", "Full Knowledge Base"],
    },
    {
        "name": "Concrete 101 — Complete Guide",
        "url": "https://concrete-assistant.streamlit.app/",
        "desc": "Deep-dive reference: ct[Asset] tokens, yield strategies, Probability Engine and enterprise tools.",
        "badge": "📚", "tag": "Reference", "tag_color": "#4DA6FF",
        "features": ["ct[Asset] Tokens", "Probability Engine", "Enterprise Docs", "Vault Mechanics"],
    },
]

QUIZ_QUESTIONS = [
    {"id":1,"en_q":"What is the total value of assets on the Concrete platform?","ur_q":"Concrete پلیٹ فارم پر کل اثاثوں کی قیمت کیا ہے؟","options":["$200M","$902.3M","$50M","$1.5B"],"correct":"$902.3M","en_fact":"Concrete has $902.3M in assets on platform and has processed $11.25B total.","ur_fact":"Concrete پر $902.3M اثاثے ہیں اور کل $11.25B پروسیس ہو چکے ہیں۔"},
    {"id":2,"en_q":"Where do you track and earn your Concrete 'Bags'?","ur_q":"Concrete 'Bags' کہاں track اور earn کرتے ہیں؟","options":["Discord only","points.concrete.xyz","Twitter DMs","Etherscan"],"correct":"points.concrete.xyz","en_fact":"The official Bags dashboard is at points.concrete.xyz/home","ur_fact":"Bags کا آفیشل ڈیش بورڈ points.concrete.xyz/home پر ہے"},
    {"id":3,"en_q":"Which vault has the highest TVL on Concrete?","ur_q":"Concrete پر سب سے زیادہ TVL کس vault میں ہے؟","options":["WBTC Vault","Concrete DeFi USDT","WeETH Vault","Berachain Stables"],"correct":"WeETH Vault","en_fact":"The WeETH Vault holds $706M TVL — Concrete's flagship institutional product.","ur_fact":"WeETH Vault میں $706M TVL ہے — Concrete کی اہم institutional پروڈکٹ۔"},
    {"id":4,"en_q":"What does the Concrete Social 'Bags' Campaign reward you for?","ur_q":"Concrete Social 'Bags' Campaign کس چیز پر reward دیتی ہے؟","options":["Only depositing into vaults","X/Discord engagement, education & referrals","Trading volume on-chain","Holding NFTs"],"correct":"X/Discord engagement, education & referrals","en_fact":"Phase 1 rewards social tasks: follows, posts, Discord participation, articles & referrals.","ur_fact":"Phase 1 میں social tasks reward ہوتے ہیں: follows, posts, Discord، articles اور referrals۔"},
    {"id":5,"en_q":"Which firms have audited Concrete's smart contracts?","ur_q":"Concrete کے smart contracts کس نے audit کیے؟","options":["Only Certik","Cantina, Code4rena, Halborn, Zellic, Hypernative, zeroShadow","No audits yet","Just OpenZeppelin"],"correct":"Cantina, Code4rena, Halborn, Zellic, Hypernative, zeroShadow","en_fact":"Concrete is audited by 6 top firms — security is core to its institutional-grade infrastructure.","ur_fact":"Concrete کے 6 اداروں نے audit کیے — سیکیورٹی اس کا بنیادی ستون ہے۔"},
    {"id":6,"en_q":"What is the Concrete Earn app URL?","ur_q":"Concrete Earn app کا URL کیا ہے؟","options":["earn.concrete.io","app.concrete.xyz/earn","defi.concrete.xyz","vault.concrete.com"],"correct":"app.concrete.xyz/earn","en_fact":"The Earn app lives at app.concrete.xyz/earn — deposit once, earn automatically.","ur_fact":"Earn app app.concrete.xyz/earn پر ہے — ایک بار deposit کریں، خود بخود کمائیں۔"},
    {"id":7,"en_q":"Which investor is NOT a Concrete backer?","ur_q":"کون سا investor Concrete کا backer نہیں ہے؟","options":["Polychain Capital","VanEck","Binance Labs","Tribe Capital"],"correct":"Binance Labs","en_fact":"Concrete is backed by Polychain, VanEck, YZi Labs, Portal Ventures, Hashed & Tribe Capital.","ur_fact":"Concrete کو Polychain, VanEck, YZi Labs, Portal Ventures, Hashed اور Tribe Capital نے back کیا ہے۔"},
    {"id":8,"en_q":"What does Concrete's vault system do automatically after deposit?","ur_q":"Deposit کے بعد Concrete کا vault system خود بخود کیا کرتا ہے؟","options":["Locks funds for 1 year","Allocates, rebalances & compounds yield","Converts to stablecoins","Bridges to Solana"],"correct":"Allocates, rebalances & compounds yield","en_fact":"Deposit once — Concrete's quantitative system handles allocation, rebalancing and compounding.","ur_fact":"ایک بار deposit کریں — Concrete کا quantitative system باقی سب سنبھالتا ہے۔"},
    {"id":9,"en_q":"What token do you receive when depositing USDT into a Concrete vault?","ur_q":"Concrete vault میں USDT deposit کرنے پر کون سا token ملتا ہے؟","options":["vUSDT","ctUSDT","cxUSDT","xUSDT"],"correct":"ctUSDT","en_fact":"ct[Asset] tokens are yield-bearing vault shares that automatically grow as the vault earns.","ur_fact":"ct[Asset] tokens yield-bearing vault shares ہیں جو vault کی کمائی کے ساتھ خود بخود بڑھتے ہیں۔"},
    {"id":10,"en_q":"What is Concrete's internal risk system called?","ur_q":"Concrete کے internal risk system کا نام کیا ہے؟","options":["RiskGuard AI","Probability Engine","VaultShield","SafeYield Protocol"],"correct":"Probability Engine","en_fact":"The Probability Engine analyzes asset distribution, projects price movements and auto-shifts into protective strategies.","ur_fact":"Probability Engine اثاثوں کی تقسیم کا تجزیہ کرتا ہے اور حفاظتی strategies میں خودکار تبدیل ہوتا ہے۔"},
    {"id":11,"en_q":"Which DeFi protocols does Concrete's vault deploy capital to for lending?","ur_q":"Concrete کے vault کس DeFi protocols میں lending کے لیے سرمایہ لگاتے ہیں؟","options":["Uniswap, SushiSwap","Aave, Compound, Morpho","dYdX, GMX","Yearn, Beefy"],"correct":"Aave, Compound, Morpho","en_fact":"Concrete vaults use Aave, Compound and Morpho for lending — alongside Curve, Pendle, EigenLayer.","ur_fact":"Concrete vaults Aave, Compound اور Morpho استعمال کرتے ہیں — Curve, Pendle, EigenLayer کے ساتھ۔"},
    {"id":12,"en_q":"Which company developed the Concrete protocol?","ur_q":"Concrete protocol کس کمپنی نے بنایا؟","options":["Alchemy","Blueprint Finance","Paradigm Labs","Gauntlet"],"correct":"Blueprint Finance","en_fact":"Concrete is developed by Blueprint Finance — Glow Finance on Solana is its sister protocol.","ur_fact":"Concrete کو Blueprint Finance نے بنایا — Solana پر Glow Finance اس کا sister protocol ہے۔"},
]

# ── SESSION STATE ──────────────────────────────────────────
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = random.sample(QUIZ_QUESTIONS, 6)
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "score" not in st.session_state:
    st.session_state.score = 0
if "username" not in st.session_state:
    st.session_state.username = "Anonymous"
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = [
        {"name": "VaultKing.eth",  "score": 6, "total": 6, "tier": "🏆 Gold Vault Navigator"},
        {"name": "MoaiMaxi",       "score": 5, "total": 6, "tier": "🥈 Silver Navigator"},
        {"name": "ConcreteOG",     "score": 5, "total": 6, "tier": "🥈 Silver Navigator"},
        {"name": "BagHolder9k",    "score": 4, "total": 6, "tier": "🥉 Bronze Navigator"},
    ]
if "art_gallery" not in st.session_state:
    st.session_state.art_gallery = []

def get_tier(score, total):
    pct = (score / total) * 100
    if pct == 100: return "🏆 Gold Vault Navigator"
    if pct >= 75:  return "🥈 Silver Navigator"
    if pct >= 50:  return "🥉 Bronze Navigator"
    return "🗿 Apprentice Moai"

# ── SIDEBAR ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 16px 0 8px;'>
        <span style='font-size:32px;'>🗿</span>
        <div style='font-family:"Space Grotesk",sans-serif; font-weight:800; font-size:20px; color:#fff; margin-top:6px;'>
            concrete<span style='color:#1AE8A0;'>.xyz</span>
        </div>
        <div style='font-family:"Space Mono",monospace; font-size:9px; color:#4A7A6A; letter-spacing:0.12em; margin-top:4px;'>
            COMMUNITY HUB
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Language Toggle
    st.markdown("<div style='font-family:\"Space Mono\",monospace; font-size:10px; color:#1AE8A0; letter-spacing:0.18em; text-transform:uppercase; margin-bottom:10px;'>🌐 Language / زبان</div>", unsafe_allow_html=True)
    lang_col1, lang_col2 = st.columns(2)
    with lang_col1:
        if st.button("🇬🇧 English", use_container_width=True):
            st.session_state.lang = "en"
            st.rerun()
    with lang_col2:
        if st.button("🇵🇰 اردو", use_container_width=True):
            st.session_state.lang = "ur"
            st.rerun()

    active_lang = "🇬🇧 English" if st.session_state.lang == "en" else "🇵🇰 اردو"
    st.caption(f"Active: {active_lang}")

    st.markdown("---")

    # Navigator Name
    st.markdown("<div style='font-family:\"Space Mono\",monospace; font-size:10px; color:#1AE8A0; letter-spacing:0.18em; text-transform:uppercase; margin-bottom:8px;'>👤 Navigator Name</div>", unsafe_allow_html=True)
    username_input = st.text_input("", value=st.session_state.username, placeholder="Your wallet / name...", label_visibility="collapsed")
    st.session_state.username = username_input

    st.markdown("---")

    # Quick Links
    st.markdown("<div style='font-family:\"Space Mono\",monospace; font-size:10px; color:#1AE8A0; letter-spacing:0.18em; text-transform:uppercase; margin-bottom:10px;'>🔗 Quick Links</div>", unsafe_allow_html=True)
    links = [
        ("↗ Earn App", "https://app.concrete.xyz/earn"),
        ("↗ Points Dashboard", "https://points.concrete.xyz/home"),
        ("↗ Concrete.xyz", "https://concrete.xyz"),
        ("↗ Discord", "https://discord.gg/concretexyz"),
        ("↗ @ConcreteXYZ", "https://x.com/ConcreteXYZ"),
    ]
    for label, url in links:
        st.markdown(f'<a href="{url}" target="_blank" style="display:block; padding:7px 10px; margin-bottom:5px; background:rgba(26,232,160,0.04); border:1px solid rgba(26,232,160,0.1); border-radius:7px; color:#1AE8A0; font-family:\'Space Mono\',monospace; font-size:11px; text-decoration:none; letter-spacing:0.05em;">{label}</a>', unsafe_allow_html=True)

    st.markdown("---")

    # Builder card
    st.markdown("<div style='font-family:\"Space Mono\",monospace; font-size:10px; color:#1AE8A0; letter-spacing:0.18em; text-transform:uppercase; margin-bottom:10px;'>🎨 Builder</div>", unsafe_allow_html=True)
    
    # Load builder art from uploads
    art_path = Path("builder_art.jpg")
    if art_path.exists():
        st.image(str(art_path), use_container_width=True, caption="mkashifalikcp — Proof of Work")
    
    st.markdown("""
    <div style='background:rgba(26,232,160,0.04); border:1px solid rgba(26,232,160,0.1); border-radius:8px; padding:10px 12px; margin-top:8px;'>
        <div style='font-family:"Space Mono",monospace; font-size:11px; color:#1AE8A0; font-weight:700;'>mkashifalikcp</div>
        <div style='font-size:11px; color:#4A7A6A; line-height:1.6; margin-top:4px;'>Community contributor. Every tool built with the same precision as the protocol itself.</div>
    </div>
    """, unsafe_allow_html=True)


# ── HERO HEADER ────────────────────────────────────────────
st.markdown(f"""
<div style='text-align:center; padding: 20px 0 30px; animation: fadeIn 0.6s ease;'>
    <div style='font-size:64px; line-height:1;'>🗿</div>
    <h1 style='font-family:"Space Grotesk",sans-serif; font-size:36px; font-weight:800; color:#fff; margin: 12px 0 8px; letter-spacing:-0.03em;'>
        Moai <span style='color:#1AE8A0;'>Stability</span> Challenge
    </h1>
    <p style='font-family:"Space Mono",monospace; font-size:11px; color:#4A7A6A; letter-spacing:0.12em;'>
        // PROVE YOUR CONCRETE KNOWLEDGE · EARN YOUR NAVIGATOR STATUS · PACK YOUR BAGS
    </p>
</div>
""", unsafe_allow_html=True)

# ── LIVE STATS ─────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric(t("Assets on Platform","پلیٹ فارم پر اثاثے"), CONCRETE_STATS["tvl"])
c2.metric(t("Total Processed","کل پروسیس"), CONCRETE_STATS["processed"])
c3.metric(t("Security Audits","سیکیورٹی آڈٹ"), CONCRETE_STATS["audits"])
c4.metric(t("Depositors","صارفین"), CONCRETE_STATS["depositors"])

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ───────────────────────────────────────────────────
tab_labels = [
    t("📝 Quiz","📝 کوئز"),
    t("🏦 Vaults","🏦 والٹس"),
    t("🛠️ Tools","🛠️ ٹولز"),
    t("👜 Earn Bags","👜 Bags کمائیں"),
    t("🏅 Leaderboard","🏅 لیڈر بورڈ"),
    t("🎨 Art Gallery","🎨 آرٹ گیلری"),
]
tabs = st.tabs(tab_labels)


# ══════════════════════════════════════════════════════════
# TAB 1 — QUIZ
# ══════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown(f"""
    <div style='background:rgba(26,232,160,0.03); border:1px solid rgba(26,232,160,0.2); border-radius:14px; padding:18px 24px; margin-bottom:20px;'>
        <div style='font-family:"Space Mono",monospace; font-size:10px; color:#1AE8A0; letter-spacing:0.18em; text-transform:uppercase; margin-bottom:8px;'>📝 {t("Moai Stability Challenge","موئی استحکام چیلنج")}</div>
        <p style='font-size:13px; color:#4A7A6A; margin:0;'>
            {t("Answer 6 randomized questions about Concrete.xyz. Submit to see your score and rank on the leaderboard.",
               "Concrete.xyz کے بارے میں 6 سوالات کے جوابات دیں۔ اپنا score اور rank دیکھنے کے لیے submit کریں۔")}
        </p>
    </div>
    """, unsafe_allow_html=True)

    questions = st.session_state.quiz_questions
    answers = st.session_state.answers

    if not st.session_state.submitted:
        for i, q in enumerate(questions):
            question_text = q["ur_q"] if st.session_state.lang == "ur" else q["en_q"]
            st.markdown(f"""
            <div style='background:rgba(10,24,18,0.85); border:1px solid rgba(26,232,160,0.1); border-radius:12px; padding:20px 24px; margin-bottom:12px;'>
                <div style='font-family:"Space Mono",monospace; font-size:9px; color:#4A7A6A; letter-spacing:0.12em; margin-bottom:6px;'>
                    {t(f"QUESTION {i+1} OF {len(questions)}", f"سوال {i+1} از {len(questions)}")}
                </div>
                <div style='font-size:15px; font-weight:600; color:#E0F0E8; line-height:1.45;'>{question_text}</div>
            </div>
            """, unsafe_allow_html=True)

            selected = st.radio(
                f"q_{q['id']}",
                q["options"],
                key=f"radio_{q['id']}",
                label_visibility="collapsed",
                index=q["options"].index(answers[q["id"]]) if q["id"] in answers else None,
            )
            if selected:
                st.session_state.answers[q["id"]] = selected

        st.markdown("<br>", unsafe_allow_html=True)
        answered_count = len(st.session_state.answers)
        total_q = len(questions)
        st.progress(answered_count / total_q, text=t(f"{answered_count}/{total_q} answered", f"{answered_count}/{total_q} جواب دیے"))

        col_sub, col_rst = st.columns([2, 1])
        with col_sub:
            if answered_count == total_q:
                if st.button(t("🗿 Submit — Prove Your Knowledge", "🗿 جمع کریں — اپنا علم ثابت کریں"), use_container_width=True):
                    score = sum(1 for q in questions if st.session_state.answers.get(q["id"]) == q["correct"])
                    st.session_state.score = score
                    st.session_state.submitted = True
                    tier = get_tier(score, total_q)
                    st.session_state.leaderboard.append({
                        "name": st.session_state.username or "Anonymous",
                        "score": score, "total": total_q, "tier": tier
                    })
                    st.session_state.leaderboard = sorted(st.session_state.leaderboard, key=lambda x: -x["score"])[:10]
                    st.rerun()
            else:
                st.info(t(f"Answer all {total_q} questions to submit.", f"جمع کرنے کے لیے تمام {total_q} سوالات کے جوابات دیں۔"))
        with col_rst:
            if st.button(t("🔄 Reset Quiz", "🔄 کوئز دوبارہ شروع کریں"), use_container_width=True):
                st.session_state.quiz_questions = random.sample(QUIZ_QUESTIONS, 6)
                st.session_state.answers = {}
                st.session_state.submitted = False
                st.session_state.score = 0
                st.rerun()

    else:
        score = st.session_state.score
        total_q = len(questions)
        tier = get_tier(score, total_q)
        pct = int((score / total_q) * 100)

        # Result banner
        if score == total_q:
            st.success(f"🏆 {t('PERFECT SCORE! You are a true Concrete Moai!', 'مکمل score! آپ ایک حقیقی Concrete Moai ہیں!')}")
        elif score >= total_q * 0.75:
            st.success(f"🥈 {t('Excellent! Silver Navigator achieved!', 'شاندار! Silver Navigator حاصل کیا!')}")
        elif score >= total_q * 0.5:
            st.info(f"🥉 {t('Good effort! Bronze Navigator.', 'اچھی کوشش! Bronze Navigator.')}")
        else:
            st.warning(f"🗿 {t('Keep learning! Apprentice Moai.', 'سیکھتے رہیں! Apprentice Moai.')}")

        col1, col2, col3 = st.columns(3)
        col1.metric(t("Score","اسکور"), f"{score}/{total_q}")
        col2.metric(t("Accuracy","درستگی"), f"{pct}%")
        col3.metric(t("Rank","رینک"), tier)

        st.markdown("<br>", unsafe_allow_html=True)

        # Review answers
        st.markdown(f"<div style='font-family:\"Space Mono\",monospace; font-size:10px; color:#1AE8A0; letter-spacing:0.18em; text-transform:uppercase; margin-bottom:14px;'>📋 {t('Answer Review','جوابات کا جائزہ')}</div>", unsafe_allow_html=True)

        for q in questions:
            user_ans = st.session_state.answers.get(q["id"], "—")
            is_correct = user_ans == q["correct"]
            icon = "✅" if is_correct else "❌"
            qtext = q["ur_q"] if st.session_state.lang == "ur" else q["en_q"]
            fact = q["ur_fact"] if st.session_state.lang == "ur" else q["en_fact"]
            border_color = "rgba(26,232,160,0.3)" if is_correct else "rgba(255,107,107,0.3)"
            bg_color = "rgba(26,232,160,0.04)" if is_correct else "rgba(255,107,107,0.04)"

            st.markdown(f"""
            <div style='background:{bg_color}; border:1px solid {border_color}; border-radius:10px; padding:14px 18px; margin-bottom:10px;'>
                <div style='font-size:13px; font-weight:600; color:#D0E8DF; margin-bottom:6px;'>{icon} {qtext}</div>
                <div style='font-family:"Space Mono",monospace; font-size:11px; color:#4A7A6A; margin-bottom:4px;'>
                    {t("Your answer","آپ کا جواب")}: <span style='color:{"#1AE8A0" if is_correct else "#FF6B6B"};'>{user_ans}</span>
                    {"" if is_correct else f' → {t("Correct","درست")}: <span style="color:#1AE8A0;">{q["correct"]}</span>'}
                </div>
                <div style='font-family:"Space Mono",monospace; font-size:10px; color:#0D8A60; padding:6px 10px; background:rgba(26,232,160,0.05); border-radius:6px; border-left:2px solid #0D8A60; line-height:1.6;'>💡 {fact}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Share message
        share_msg = f"I scored {score}/{total_q} on the Concrete.xyz Moai Stability Challenge! {tier} — Packing my Bags at points.concrete.xyz 🗿🟢 @ConcreteXYZ"
        st.code(share_msg, language=None)

        col_x, col_r = st.columns(2)
        with col_x:
            st.link_button(t("🐦 Share on X","🐦 X پر شیئر کریں"), f"https://twitter.com/intent/tweet?text={share_msg.replace(' ', '%20')}", use_container_width=True)
        with col_r:
            if st.button(t("🔄 Try Again","🔄 دوبارہ کوشش کریں"), use_container_width=True):
                st.session_state.quiz_questions = random.sample(QUIZ_QUESTIONS, 6)
                st.session_state.answers = {}
                st.session_state.submitted = False
                st.session_state.score = 0
                st.rerun()


# ══════════════════════════════════════════════════════════
# TAB 2 — VAULTS
# ══════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown(f"""
    <div style='background:rgba(26,232,160,0.03); border:1px solid rgba(26,232,160,0.2); border-radius:14px; padding:18px 24px; margin-bottom:20px;'>
        <div style='font-family:"Space Mono",monospace; font-size:10px; color:#1AE8A0; letter-spacing:0.18em; text-transform:uppercase; margin-bottom:8px;'>🏦 {t("Live Vaults","لائیو والٹس")}</div>
        <p style='font-size:13px; color:#4A7A6A; margin:0;'>
            {t("Real-time vault data from Concrete.xyz. Deposit once — earn automatically.",
               "Concrete.xyz سے real-time vault ڈیٹا۔ ایک بار deposit کریں — خود بخود کمائیں۔")}
        </p>
    </div>
    """, unsafe_allow_html=True)

    chain_filter = st.selectbox(
        t("Filter by Chain","چین کے مطابق فلٹر کریں"),
        [t("All Chains","تمام چینز"), "Ethereum", "Berachain"],
    )

    for vault in REAL_VAULTS:
        if chain_filter not in [t("All Chains","تمام چینز"), vault["chain"]]:
            continue
        chain_color = "#1AE8A0" if vault["chain"] == "Ethereum" else "#FF6B35"
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06); border-radius:10px; padding:14px 18px; margin-bottom:10px; display:flex; align-items:center; gap:16px;'>
            <span style='font-size:24px;'>{vault["badge"]}</span>
            <div style='flex:1;'>
                <div style='font-weight:700; font-size:14px; color:#D0E8E0;'>{vault["name"]}</div>
                <div style='font-family:"Space Mono",monospace; font-size:11px; color:#4A7A6A; margin-top:3px;'>{vault["asset"]} · <span style='color:{chain_color};'>{vault["chain"]}</span></div>
            </div>
            <div style='text-align:right;'>
                <div style='font-family:"Space Mono",monospace; font-size:14px; color:#1AE8A0; font-weight:700;'>{vault["apy"]} APY</div>
                <div style='font-family:"Space Mono",monospace; font-size:11px; color:#4A7A6A;'>{vault["tvl"]} TVL</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button(t("🏦 Open Earn App → app.concrete.xyz/earn","🏦 Earn App کھولیں → app.concrete.xyz/earn"), "https://app.concrete.xyz/earn", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-family:\"Space Mono\",monospace; font-size:10px; color:#1AE8A0; letter-spacing:0.18em; text-transform:uppercase; margin-bottom:14px;'>💼 {t('Backed By','سرمایہ کار')}</div>", unsafe_allow_html=True)
    backers = ["Polychain Capital","VanEck","YZi Labs","Portal Ventures","Hashed","Tribe Capital","Auros","Presto","Hypersphere","Lightshift"]
    backer_html = " ".join([f'<span style="display:inline-block; margin:4px; padding:5px 12px; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07); border-radius:20px; font-family:\'Space Mono\',monospace; font-size:10px; color:#4A7A6A;">{b}</span>' for b in backers])
    st.markdown(f'<div style="background:rgba(10,24,18,0.85); border:1px solid rgba(26,232,160,0.1); border-radius:14px; padding:20px 24px;">{backer_html}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# TAB 3 — TOOLS
# ══════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown(f"""
    <div style='background:rgba(26,232,160,0.03); border:1px solid rgba(26,232,160,0.2); border-radius:14px; padding:18px 24px; margin-bottom:20px;'>
        <div style='font-family:"Space Mono",monospace; font-size:10px; color:#1AE8A0; letter-spacing:0.18em; text-transform:uppercase; margin-bottom:8px;'>🛠️ {t("Community-Built Tools","کمیونٹی کے بنائے ٹولز")}</div>
        <p style='font-size:13px; color:#4A7A6A; margin:0;'>
            {t("Built by mkashifalikcp to help navigate Concrete.xyz — from vault analytics to full protocol guides.",
               "mkashifalikcp نے بنائے — vault analytics سے لے کر مکمل protocol guides تک۔")}
        </p>
    </div>
    """, unsafe_allow_html=True)

    for tool in COMMUNITY_TOOLS:
        feat_html = " ".join([f'<span style="display:inline-block; margin:3px; padding:3px 10px; background:rgba(26,232,160,0.04); border:1px solid rgba(26,232,160,0.12); border-radius:6px; font-family:\'Space Mono\',monospace; font-size:10px; color:#4A8A70;">✓ {f}</span>' for f in tool["features"]])
        st.markdown(f"""
        <div style='background:rgba(10,24,18,0.85); border:1px solid rgba(26,232,160,0.1); border-radius:14px; padding:22px 24px; margin-bottom:14px;'>
            <div style='display:flex; align-items:flex-start; gap:16px; margin-bottom:14px;'>
                <span style='font-size:32px; line-height:1;'>{tool["badge"]}</span>
                <div style='flex:1;'>
                    <div style='display:flex; align-items:center; gap:10px; margin-bottom:6px; flex-wrap:wrap;'>
                        <span style='font-weight:700; font-size:15px; color:#E0F0E8;'>{tool["name"]}</span>
                        <span style='padding:2px 10px; border-radius:20px; background:{tool["tag_color"]}18; border:1px solid {tool["tag_color"]}40; font-family:"Space Mono",monospace; font-size:9px; color:{tool["tag_color"]}; letter-spacing:0.1em;'>{tool["tag"]}</span>
                    </div>
                    <p style='font-family:"Space Mono",monospace; font-size:12px; color:#4A7A6A; line-height:1.7; margin:0;'>{tool["desc"]}</p>
                </div>
            </div>
            <div style='margin-bottom:16px;'>{feat_html}</div>
            <a href="{tool["url"]}" target="_blank" style='display:inline-flex; align-items:center; gap:6px; padding:9px 20px; background:rgba(26,232,160,0.08); border:1px solid rgba(26,232,160,0.25); border-radius:8px; font-family:"Space Mono",monospace; font-size:11px; color:#1AE8A0; text-decoration:none; letter-spacing:0.06em;'>↗ Open Tool</a>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# TAB 4 — BAGS
# ══════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown(f"""
    <div style='background:rgba(10,24,18,0.85); border:1px solid rgba(26,232,160,0.1); border-radius:14px; padding:22px 26px; margin-bottom:16px;'>
        <div style='font-family:"Space Mono",monospace; font-size:10px; color:#1AE8A0; letter-spacing:0.18em; text-transform:uppercase; margin-bottom:12px;'>👜 {t("Concrete Bags Campaign — Phase 1","کانکریٹ Bags مہم — مرحلہ 1")}</div>
        <p style='font-size:13px; color:#4A7A6A; line-height:1.7; margin-bottom:12px;'>
            {t("Your actions = your Bags. Complete social & community tasks to earn Bags, which convert to Concrete Points — qualifying you for future rewards at TGE.",
               "آپ کے اقدامات = آپ کے Bags۔ Bags کمانے کے لیے سماجی اور کمیونٹی tasks مکمل کریں — جو Concrete Points میں تبدیل ہوں گے اور TGE پر مستقبل کے rewards کے لیے اہل بنائیں گے۔")}
        </p>
        <a href="https://points.concrete.xyz/home" target="_blank" style='font-family:"Space Mono",monospace; font-size:12px; color:#1AE8A0; text-decoration:none;'>→ points.concrete.xyz/home</a>
    </div>
    """, unsafe_allow_html=True)

    cat_colors = {"Social": "#1AE8A0", "Discord": "#5865F2", "Education": "#FFD700", "Referral": "#FF6B6B"}

    for item in BAGS_ACTIONS:
        color = cat_colors.get(item["category"], "#888")
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:12px; padding:10px 14px; background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.04); border-radius:8px; margin-bottom:7px;'>
            <div style='width:7px; height:7px; border-radius:50%; background:{color}; flex-shrink:0;'></div>
            <div style='flex:1; font-size:13px; color:#C0D8D0;'>{item["action"]}</div>
            <div style='font-family:"Space Mono",monospace; font-size:12px; color:{color}; white-space:nowrap;'>+{item["bags"]} 👜</div>
            <span style='padding:2px 8px; border-radius:10px; background:{color}18; border:1px solid {color}40; font-family:"Space Mono",monospace; font-size:9px; color:{color};'>{item["category"]}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='margin-top:18px; padding:14px 18px; background:rgba(26,232,160,0.05); border-radius:8px; border:1px solid rgba(26,232,160,0.12);'>
        <div style='font-family:"Space Mono",monospace; font-size:11px; color:#1AE8A0; margin-bottom:6px;'>💡 {t("Referral Bonus","ریفرل بونس")}</div>
        <div style='font-size:13px; color:#4A7A6A; line-height:1.6;'>
            {t("Earn 10% of Bags from direct referrals + 5% from their referrals. No cap. Stack infinitely.",
               "براہ راست referrals سے 10% Bags کمائیں + ان کے referrals سے 5%۔ کوئی حد نہیں۔ لامحدود stack کریں۔")}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.link_button(t("👜 Go to Bags Dashboard","👜 Bags Dashboard پر جائیں"), "https://points.concrete.xyz/home", use_container_width=True)
    with col_b:
        st.link_button(t("💬 Join Discord","💬 Discord میں شامل ہوں"), "https://discord.gg/concretexyz", use_container_width=True)


# ══════════════════════════════════════════════════════════
# TAB 5 — LEADERBOARD
# ══════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown(f"""
    <div style='font-family:"Space Mono",monospace; font-size:10px; color:#1AE8A0; letter-spacing:0.18em; text-transform:uppercase; margin-bottom:16px;'>🏅 {t("Top Vault Navigators","ٹاپ والٹ نیویگیٹرز")}</div>
    """, unsafe_allow_html=True)

    medals = ["🥇", "🥈", "🥉"]
    for idx, entry in enumerate(st.session_state.leaderboard):
        medal = medals[idx] if idx < 3 else f"#{idx+1}"
        bg = "rgba(255,215,0,0.05)" if idx == 0 else "rgba(255,255,255,0.02)"
        border = "rgba(255,215,0,0.2)" if idx == 0 else "rgba(255,255,255,0.05)"
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:12px; padding:12px 16px; background:{bg}; border:1px solid {border}; border-radius:9px; margin-bottom:8px;'>
            <div style='font-size:18px; width:32px; text-align:center;'>{medal}</div>
            <div style='flex:1; font-weight:700; font-size:14px; color:#D0E8E0;'>{entry["name"]}</div>
            <div style='font-family:"Space Mono",monospace; font-size:12px; color:#1AE8A0;'>{entry["score"]}/{entry["total"]}</div>
            <div style='font-size:13px; color:#4A7A6A;'>{entry["tier"]}</div>
        </div>
        """, unsafe_allow_html=True)

    if len(st.session_state.leaderboard) == 0:
        st.info(t("No entries yet. Take the quiz to claim rank #1!", "ابھی کوئی entry نہیں۔ کوئز دیں اور #1 بنیں!"))

    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button(t("📊 Track Real Bags → points.concrete.xyz","📊 Real Bags track کریں → points.concrete.xyz"), "https://points.concrete.xyz/home", use_container_width=True)


# ══════════════════════════════════════════════════════════
# TAB 6 — ART GALLERY
# ══════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown(f"""
    <div style='background:rgba(26,232,160,0.03); border:1px solid rgba(26,232,160,0.2); border-radius:14px; padding:18px 24px; margin-bottom:20px;'>
        <div style='font-family:"Space Mono",monospace; font-size:10px; color:#1AE8A0; letter-spacing:0.18em; text-transform:uppercase; margin-bottom:8px;'>🎨 {t("Community Art Gallery","کمیونٹی آرٹ گیلری")}</div>
        <p style='font-size:13px; color:#4A7A6A; line-height:1.7; margin:0;'>
            {t("Share your Concrete.xyz fan art, memes, sketches & creative work. Upload below and show your Proof of Work! 🗿",
               "اپنا Concrete.xyz فین آرٹ، میمز، اسکیچ اور تخلیقی کام شیئر کریں۔ نیچے اپلوڈ کریں اور Proof of Work دکھائیں! 🗿")}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Featured builder art ──
    featured_label = t("Featured: Builder's Proof of Work", "فیچرڈ: بلڈر کا Proof of Work")
    st.markdown(f"<div style='font-family:\"Space Mono\",monospace; font-size:10px; color:#1AE8A0; letter-spacing:0.18em; text-transform:uppercase; margin-bottom:12px;'>⭐ {featured_label}</div>", unsafe_allow_html=True)

    art_path = Path("builder_art.jpg")
    if art_path.exists():
        col_img, col_info = st.columns([2, 1])
        with col_img:
            st.image(str(art_path), use_container_width=True)
        with col_info:
            st.markdown(f"""
            <div style='background:rgba(10,24,18,0.85); border:1px solid rgba(26,232,160,0.15); border-radius:12px; padding:18px 20px; height:100%;'>
                <div style='font-family:"Space Mono",monospace; font-size:10px; color:#1AE8A0; letter-spacing:0.15em; margin-bottom:10px;'>🗿 FEATURED ART</div>
                <div style='font-weight:700; font-size:16px; color:#E0F0E8; margin-bottom:8px;'>
                    {t('"CONCRETE" Character Sketch', '"CONCRETE" کردار کا خاکہ')}
                </div>
                <div style='font-family:"Space Mono",monospace; font-size:11px; color:#4A7A6A; line-height:1.7; margin-bottom:14px;'>
                    {t("Hand-drawn Moai-inspired mascot with a 'C' jersey. Proof that community contribution goes beyond code.",
                       "ہاتھ سے بنا Moai-inspired کردار جس پر 'C' جرسی ہے۔ ثبوت کہ کمیونٹی کا حصہ صرف کوڈ تک محدود نہیں۔")}
                </div>
                <div style='padding:8px 12px; background:rgba(26,232,160,0.05); border-radius:8px; border:1px solid rgba(26,232,160,0.1);'>
                    <div style='font-family:"Space Mono",monospace; font-size:11px; color:#1AE8A0; font-weight:700;'>mkashifalikcp</div>
                    <div style='font-family:"Space Mono",monospace; font-size:10px; color:#4A7A6A; margin-top:3px;'>April 2026</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning(t("Builder art image not found.","بلڈر کی تصویر نہیں ملی۔"))

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    # ── Upload your art ──
    st.markdown(f"<div style='font-family:\"Space Mono\",monospace; font-size:10px; color:#1AE8A0; letter-spacing:0.18em; text-transform:uppercase; margin-bottom:12px;'>📤 {t('Upload Your Art','اپنا آرٹ اپلوڈ کریں')}</div>", unsafe_allow_html=True)

    upload_col, info_col = st.columns([2, 1])
    with upload_col:
        uploaded_files = st.file_uploader(
            t("Choose image(s)","تصویر(یں) منتخب کریں"),
            type=["png", "jpg", "jpeg", "gif", "webp"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )
        art_caption = st.text_input(
            t("Caption / Title (optional)","کیپشن / عنوان (اختیاری)"),
            placeholder=t("Describe your art...","اپنا آرٹ بیان کریں..."),
        )
        if st.button(t("📤 Submit to Gallery","📤 گیلری میں جمع کریں"), use_container_width=True):
            if uploaded_files:
                for uf in uploaded_files:
                    img = Image.open(uf)
                    buf = io.BytesIO()
                    img.save(buf, format="PNG")
                    b64 = base64.b64encode(buf.getvalue()).decode()
                    st.session_state.art_gallery.append({
                        "b64": b64,
                        "name": uf.name,
                        "caption": art_caption or t("Untitled","بے عنوان"),
                        "by": st.session_state.username or "Anonymous",
                    })
                st.success(t(f"✅ {len(uploaded_files)} image(s) added to gallery!",f"✅ {len(uploaded_files)} تصویر(یں) گیلری میں شامل کی گئیں!"))
                st.rerun()
            else:
                st.warning(t("Please select at least one image.","براہ کرم کم از کم ایک تصویر منتخب کریں۔"))

    with info_col:
        st.markdown(f"""
        <div style='background:rgba(26,232,160,0.03); border:1px solid rgba(26,232,160,0.12); border-radius:12px; padding:16px 18px;'>
            <div style='font-family:"Space Mono",monospace; font-size:10px; color:#1AE8A0; margin-bottom:10px;'>ℹ️ {t("GALLERY INFO","گیلری معلومات")}</div>
            <ul style='font-family:"Space Mono",monospace; font-size:11px; color:#4A7A6A; line-height:2; padding-left:16px;'>
                <li>{t("PNG, JPG, GIF, WEBP","PNG, JPG, GIF, WEBP")}</li>
                <li>{t("Max 200MB per file","فی فائل زیادہ سے زیادہ 200MB")}</li>
                <li>{t("Multiple files OK","متعدد فائلیں ٹھیک ہیں")}</li>
                <li>{t("Moai art appreciated 🗿","Moai آرٹ قدر کی نگاہ سے دیکھا جاتا ہے 🗿")}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # ── Community gallery ──
    if st.session_state.art_gallery:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-family:\"Space Mono\",monospace; font-size:10px; color:#1AE8A0; letter-spacing:0.18em; text-transform:uppercase; margin-bottom:14px;'>🖼️ {t('Community Submissions','کمیونٹی کی جمع کردہ تصاویر')} ({len(st.session_state.art_gallery)})</div>", unsafe_allow_html=True)

        cols = st.columns(3)
        for i, art in enumerate(st.session_state.art_gallery):
            with cols[i % 3]:
                st.markdown(f"""
                <div style='border:1px solid rgba(26,232,160,0.1); border-radius:10px; overflow:hidden; margin-bottom:12px;'>
                    <img src="data:image/png;base64,{art['b64']}" style='width:100%; display:block;' />
                    <div style='padding:10px 12px; background:rgba(10,24,18,0.85);'>
                        <div style='font-size:12px; font-weight:600; color:#D0E8DF;'>{art["caption"]}</div>
                        <div style='font-family:"Space Mono",monospace; font-size:10px; color:#1AE8A0; margin-top:3px;'>by {art["by"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='text-align:center; padding:40px 20px; border:2px dashed rgba(26,232,160,0.15); border-radius:14px; margin-top:16px;'>
            <div style='font-size:48px; margin-bottom:12px;'>🖼️</div>
            <div style='font-family:"Space Mono",monospace; font-size:12px; color:#4A7A6A;'>
                {t("No community art yet. Be the first to upload! 🗿","ابھی کوئی کمیونٹی آرٹ نہیں۔ پہلے اپلوڈ کریں! 🗿")}
            </div>
        </div>
        """, unsafe_allow_html=True)


# ── FOOTER ─────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; padding:20px 0; border-top:1px solid rgba(26,232,160,0.1); font-family:"Space Mono",monospace; font-size:10px; color:#1A3A2A; letter-spacing:0.1em;'>
    🗿 CONCRETE.XYZ · BUILT BY THE COMMUNITY · BACKED BY POLYCHAIN & VANECK · © 2026 BLUEPRINT FINANCE
</div>
""", unsafe_allow_html=True)
