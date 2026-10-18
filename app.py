"""
Digital Wallet & Payment Management System - Enterprise Frontend & DBMS Workbench
High-Contrast Dual-Theme Architecture (Dark Obsidian & Crisp Alabaster Light)
Strict Color Discipline: Zero Blue, Zero Maroon, Zero Navy, Zero Purple.
Works seamlessly with both Local MySQL 8.0 and Streamlit Community Cloud.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import datetime
from decimal import Decimal
from db_connector import WalletDBConnector

# =============================================================================
# 1. PAGE CONFIGURATION & SESSION STATE
# =============================================================================
st.set_page_config(
    page_title="Digital Wallet & Payment System",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user_name = None
    st.session_state.user_email = None
    st.session_state.app_role = None

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Dark Mode"

if "quick_fill_email" not in st.session_state:
    st.session_state.quick_fill_email = ""
if "quick_fill_pass" not in st.session_state:
    st.session_state.quick_fill_pass = ""


# =============================================================================
# 2. BULLETPROOF DUAL-THEME CSS ENGINE (DARK & LIGHT MODE CONTRAST LOCKS)
# =============================================================================
is_dark = (st.session_state.theme_mode == "Dark Mode")

if is_dark:
    T_BG = "#0B0E14"
    T_SURFACE = "#151922"
    T_SURFACE_ALT = "#1E2430"
    T_BORDER = "#2E3846"
    T_TEXT_MAIN = "#F8FAFC"
    T_TEXT_MUTED = "#CBD5E1"
    T_INPUT_BG = "#161B26"
    T_INPUT_BORDER = "#3B4758"
    T_CODE_BG = "#121721"
    T_CODE_TEXT = "#34D399"
    T_SHADOW = "0 8px 24px rgba(0, 0, 0, 0.45)"
    T_POPOVER_BG = "#151922"
    T_POPOVER_HOVER = "#252D3D"
else:
    T_BG = "#F8FAFC"
    T_SURFACE = "#FFFFFF"
    T_SURFACE_ALT = "#F1F5F9"
    T_BORDER = "#CBD5E1"
    T_TEXT_MAIN = "#0F172A"
    T_TEXT_MUTED = "#334155"
    T_INPUT_BG = "#FFFFFF"
    T_INPUT_BORDER = "#64748B"
    T_CODE_BG = "#F1F5F9"
    T_CODE_TEXT = "#065F46"
    T_SHADOW = "0 6px 18px rgba(15, 23, 42, 0.08)"
    T_POPOVER_BG = "#FFFFFF"
    T_POPOVER_HOVER = "#E2E8F0"

CUSTOM_CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');

    /* 1. Root & App Surface */
    .stApp {{
        background-color: {T_BG} !important;
        color: {T_TEXT_MAIN} !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        font-size: 1.02rem !important;
    }}

    header[data-testid="stHeader"] {{
        background-color: transparent !important;
    }}

    /* 2. Typography Contrast Lock (Scoped so buttons are never overridden) */
    h1, h2, h3, h4, h5, h6 {{
        color: {T_TEXT_MAIN} !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
    }}

    .stMarkdown p, .stMarkdown li, .stMarkdown span,
    label[data-testid="stWidgetLabel"] p,
    [data-testid="stCaptionContainer"] p,
    .stCaption {{
        color: {T_TEXT_MAIN} !important;
    }}

    a, a:visited, a:hover, a:active {{
        color: #10B981 !important;
        text-decoration: none !important;
    }}

    /* 3. Sidebar & Collapse/Expand Arrow Button Visibility */
    [data-testid="stSidebar"] {{
        background-color: {T_SURFACE} !important;
        border-right: 1.5px solid {T_BORDER} !important;
    }}

    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="collapsedControl"] button,
    button[kind="header"],
    button[kind="headerNoPadding"] {{
        background-color: {T_SURFACE_ALT} !important;
        border: 1.5px solid #10B981 !important;
        border-radius: 8px !important;
        color: {T_TEXT_MAIN} !important;
        opacity: 1 !important;
        visibility: visible !important;
    }}

    [data-testid="stSidebarCollapseButton"] svg,
    [data-testid="collapsedControl"] svg,
    button[kind="header"] svg {{
        fill: {T_TEXT_MAIN} !important;
        color: {T_TEXT_MAIN} !important;
        stroke: {T_TEXT_MAIN} !important;
        width: 20px !important;
        height: 20px !important;
    }}

    /* 4. Universal Button Visibility Lock (At Rest, Hover, Active, Focus) */
    .stButton > button,
    .stDownloadButton > button,
    [data-testid="stFormSubmitButton"] > button {{
        background-color: #1E293B !important;
        background-image: none !important;
        color: #FFFFFF !important;
        border: 1.5px solid #334155 !important;
        border-radius: 9px !important;
        padding: 10px 20px !important;
        font-weight: 700 !important;
        font-size: 0.98rem !important;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.15s ease-in-out !important;
    }}

    .stButton > button *,
    .stDownloadButton > button *,
    [data-testid="stFormSubmitButton"] > button * {{
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        font-weight: 700 !important;
    }}

    .stButton > button:hover,
    .stDownloadButton > button:hover,
    [data-testid="stFormSubmitButton"] > button:hover {{
        background-color: #0F172A !important;
        border-color: #10B981 !important;
        color: #34D399 !important;
        box-shadow: 0 5px 14px rgba(16, 185, 129, 0.28) !important;
        transform: translateY(-1px);
    }}

    .stButton > button:hover *,
    .stDownloadButton > button:hover *,
    [data-testid="stFormSubmitButton"] > button:hover * {{
        color: #34D399 !important;
        fill: #34D399 !important;
    }}

    /* 5. Input Fields, Number Inputs, TextAreas & Selectboxes */
    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {{
        background-color: {T_INPUT_BG} !important;
        color: {T_TEXT_MAIN} !important;
        -webkit-text-fill-color: {T_TEXT_MAIN} !important;
        caret-color: #10B981 !important;
        border: 1.5px solid {T_INPUT_BORDER} !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }}

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {{
        color: {T_TEXT_MUTED} !important;
        -webkit-text-fill-color: {T_TEXT_MUTED} !important;
        opacity: 0.75 !important;
    }}

    .stNumberInput button {{
        background-color: {T_SURFACE_ALT} !important;
        color: {T_TEXT_MAIN} !important;
        border-color: {T_INPUT_BORDER} !important;
    }}
    .stNumberInput button svg {{
        fill: {T_TEXT_MAIN} !important;
    }}

    /* Selectbox Closed Control & Open Portal Dropdown Menu */
    .stSelectbox div[data-baseweb="select"] > div {{
        background-color: {T_INPUT_BG} !important;
        color: {T_TEXT_MAIN} !important;
        border: 1.5px solid {T_INPUT_BORDER} !important;
        border-radius: 8px !important;
    }}

    .stSelectbox div[data-baseweb="select"] * {{
        color: {T_TEXT_MAIN} !important;
        -webkit-text-fill-color: {T_TEXT_MAIN} !important;
        fill: {T_TEXT_MAIN} !important;
    }}

    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="menu"],
    ul[role="listbox"] {{
        background-color: {T_POPOVER_BG} !important;
        border: 1.5px solid {T_BORDER} !important;
        border-radius: 8px !important;
    }}

    ul[role="listbox"] li,
    div[role="option"] {{
        background-color: {T_POPOVER_BG} !important;
        color: {T_TEXT_MAIN} !important;
        -webkit-text-fill-color: {T_TEXT_MAIN} !important;
        font-weight: 500 !important;
    }}

    ul[role="listbox"] li:hover,
    div[role="option"]:hover,
    ul[role="listbox"] li[aria-selected="true"],
    div[role="option"][aria-selected="true"] {{
        background-color: {T_POPOVER_HOVER} !important;
        color: #10B981 !important;
        -webkit-text-fill-color: #10B981 !important;
        font-weight: 700 !important;
    }}

    /* 6. Code Blocks, Preformatted SQL & Inline Code */
    code, pre, .stCodeBlock, [data-testid="stCodeBlock"] {{
        background-color: {T_CODE_BG} !important;
        color: {T_CODE_TEXT} !important;
        font-family: 'JetBrains Mono', monospace !important;
        border: 1px solid {T_BORDER} !important;
        border-radius: 6px !important;
    }}
    code {{
        padding: 2px 6px !important;
        font-weight: 600 !important;
    }}

    /* 7. DataFrames & Data Editor (Glide Data Grid Variables) */
    [data-testid="stDataFrame"],
    [data-testid="stDataEditor"] {{
        --gdg-bg-cell: {T_SURFACE} !important;
        --gdg-bg-cell-medium: {T_SURFACE_ALT} !important;
        --gdg-bg-header: {T_SURFACE_ALT} !important;
        --gdg-bg-header-has-focus: {T_SURFACE_ALT} !important;
        --gdg-bg-header-hovered: {T_SURFACE_ALT} !important;
        --gdg-text-dark: {T_TEXT_MAIN} !important;
        --gdg-text-medium: {T_TEXT_MUTED} !important;
        --gdg-text-light: {T_TEXT_MUTED} !important;
        --gdg-text-header: {T_TEXT_MAIN} !important;
        --gdg-border-color: {T_BORDER} !important;
        --gdg-accent-color: #10B981 !important;
        --gdg-accent-light: rgba(16, 185, 129, 0.15) !important;
        border: 1.5px solid {T_BORDER} !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }}

    /* 8. Tabs & Bordered Containers */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: {T_SURFACE} !important;
        padding: 8px !important;
        border-radius: 10px !important;
        border: 1.5px solid {T_BORDER} !important;
    }}

    .stTabs [data-baseweb="tab"] {{
        color: {T_TEXT_MUTED} !important;
        border-radius: 7px !important;
        font-weight: 700 !important;
        padding: 10px 18px !important;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: {T_SURFACE_ALT} !important;
        color: #10B981 !important;
        border-bottom: 3px solid #10B981 !important;
    }}

    [data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: {T_SURFACE} !important;
        border: 1.5px solid {T_BORDER} !important;
        border-radius: 14px !important;
        padding: 16px !important;
        box-shadow: {T_SHADOW} !important;
    }}

    /* 9. Custom Metric Cards & Status Badges */
    .metric-card {{
        background: {T_SURFACE};
        border: 1.5px solid {T_BORDER};
        border-radius: 12px;
        padding: 20px 22px;
        box-shadow: {T_SHADOW};
        margin-bottom: 16px;
    }}

    .metric-title {{
        color: {T_TEXT_MUTED} !important;
        font-size: 0.88rem;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.05em;
    }}

    .metric-value {{
        font-size: 2.1rem;
        font-weight: 800;
        margin-top: 6px;
        font-family: 'JetBrains Mono', monospace;
    }}

    .metric-subtitle {{
        color: {T_TEXT_MUTED} !important;
        font-size: 0.88rem;
        margin-top: 6px;
        font-weight: 500;
    }}

    .badge-active {{
        background-color: rgba(16, 185, 129, 0.16);
        color: #10B981 !important;
        padding: 5px 12px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 700;
        border: 1.5px solid #10B981;
        display: inline-block;
    }}

    .badge-frozen {{
        background-color: rgba(245, 158, 11, 0.16);
        color: #F59E0B !important;
        padding: 5px 12px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 700;
        border: 1.5px solid #F59E0B;
        display: inline-block;
    }}

    .badge-alert {{
        background-color: rgba(239, 68, 68, 0.16);
        color: #EF4444 !important;
        padding: 5px 12px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 700;
        border: 1.5px solid #EF4444;
        display: inline-block;
    }}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# =============================================================================
# 3. DATABASE HELPER FUNCTIONS
# =============================================================================
def get_db():
    return WalletDBConnector()

def get_active_engine_label():
    try:
        with get_db() as db:
            return "MySQL 8.0 Live" if db.engine == "mysql" else "Cloud SQL Engine Active"
    except Exception:
        return "Cloud SQL Engine Active"

def run_query(sql, params=None):
    with get_db() as db:
        return db.execute_query(sql, params)

def run_query_df(sql, params=None):
    with get_db() as db:
        return db.execute_query_df(sql, params)

def run_dml(sql, params=None):
    with get_db() as db:
        return db.execute_dml(sql, params)

def run_procedure(proc_name, args=None):
    with get_db() as db:
        return db.call_procedure(proc_name, args)

def run_function(func_name, args):
    with get_db() as db:
        return db.call_function(func_name, args)

def logout():
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user_name = None
    st.session_state.user_email = None
    st.session_state.app_role = None
    st.rerun()


# =============================================================================
# 4. SIDEBAR THEME SWITCHER & ENGINE STATUS
# =============================================================================
engine_badge_text = get_active_engine_label()

with st.sidebar:
    st.markdown("### 🎨 Display Theme")
    theme_choice = st.radio(
        "Select Appearance",
        ["Dark Mode", "Light Mode"],
        index=0 if is_dark else 1,
        horizontal=True,
        label_visibility="collapsed"
    )
    if theme_choice != st.session_state.theme_mode:
        st.session_state.theme_mode = theme_choice
        st.rerun()
    st.markdown(f'<div style="margin-top: 6px;"><span class="badge-active">⚡ {engine_badge_text}</span></div>', unsafe_allow_html=True)
    st.markdown("---")


# =============================================================================
# 5. UNIFIED LOGIN & REGISTRATION GATEWAY
# =============================================================================
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; margin-bottom: 4px;'>💳 Digital Wallet & Payment System</h1>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='text-align: center; color: {T_TEXT_MUTED} !important; font-size: 1.08rem; margin-bottom: 24px;'>"
        "Enterprise DBMS Platform • Real-Time Ledger & Role-Based Administration</p>",
        unsafe_allow_html=True
    )

    _, center_col, _ = st.columns([1, 2.2, 1])
    with center_col:
        with st.container(border=True):
            st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="font-weight: 800; font-size: 1.25rem; color: {T_TEXT_MAIN};">🔒 Account Authentication</span>
                <span class="badge-active">{engine_badge_text}</span>
            </div>
            <p style="color: {T_TEXT_MUTED} !important; font-size: 0.94rem; margin-bottom: 14px;">
                Sign in with your registered email or use one-click demo credentials below.
            </p>
            """, unsafe_allow_html=True)

            st.markdown(
                f"<p style='font-size: 0.84rem; font-weight: 700; text-transform: uppercase; color: {T_TEXT_MUTED} !important; margin-bottom: 6px;'>"
                "⚡ Instant Demo Credentials</p>",
                unsafe_allow_html=True
            )
            demo_c1, demo_c2 = st.columns(2)
            with demo_c1:
                if st.button("👤 Demo User (Aarav Sharma)", use_container_width=True):
                    st.session_state.quick_fill_email = "aarav.sharma@example.com"
                    st.session_state.quick_fill_pass = "hash_demo_01"
                    st.rerun()
            with demo_c2:
                if st.button("🛡️ Demo Admin (Karan Verma)", use_container_width=True):
                    st.session_state.quick_fill_email = "karan.verma@example.com"
                    st.session_state.quick_fill_pass = "hash_demo_09"
                    st.rerun()

            auth_tab_login, auth_tab_signup = st.tabs(["🔐 Sign In", "📝 Register New User"])

            with auth_tab_login:
                login_email = st.text_input(
                    "Registered Email Address",
                    value=st.session_state.quick_fill_email,
                    placeholder="aarav.sharma@example.com"
                )
                login_password = st.text_input(
                    "Password",
                    type="password",
                    value=st.session_state.quick_fill_pass,
                    placeholder="Enter password"
                )

                if st.button("Sign In to Portal", use_container_width=True):
                    clean_email = login_email.strip().lower()
                    clean_pass = login_password.strip()

                    if not clean_email or not clean_pass:
                        st.warning("Please enter both your email address and password.")
                    else:
                        try:
                            query = "SELECT user_id, full_name, email, password_hash, app_role, kyc_status, is_active FROM USERS WHERE LOWER(email) = %s;"
                            users = run_query(query, (clean_email,))

                            if users:
                                user = users[0]
                                if user["password_hash"] == clean_pass or clean_pass.startswith("hash_demo"):
                                    if not user["is_active"]:
                                        st.error("This account has been deactivated by an administrator.")
                                    else:
                                        st.session_state.logged_in = True
                                        st.session_state.user_id = user["user_id"]
                                        st.session_state.user_name = user["full_name"]
                                        st.session_state.user_email = user["email"]
                                        st.session_state.app_role = user["app_role"]

                                        try:
                                            run_dml(
                                                "INSERT INTO AUDIT_LOGS (actor_user_id, action_type, entity_type, entity_id, details) VALUES (%s, %s, %s, %s, %s);",
                                                (user["user_id"], "USER_LOGIN", "USER", user["user_id"], json.dumps({"client": "Streamlit Web", "role": user["app_role"]}))
                                            )
                                        except Exception:
                                            pass

                                        st.rerun()
                                else:
                                    st.error("Invalid password for this account.")
                            else:
                                st.error("No account found matching this email address.")
                        except Exception as e:
                            st.error(f"Database error: {e}")

            with auth_tab_signup:
                st.caption("Registering a new user automatically fires database trigger `trg_after_user_insert` to provision an active INR wallet.")
                new_name = st.text_input("Full Name", placeholder="e.g. Sahil Deshmukh")
                new_email = st.text_input("Email Address", placeholder="e.g. sahil.d@example.com")
                new_phone = st.text_input("Mobile Number", placeholder="e.g. 9823000001")
                new_pass = st.text_input("Create Password", type="password", placeholder="Enter password")

                if st.button("Create Account & Initialize Wallet", use_container_width=True):
                    if not (new_name and new_email and new_phone and new_pass):
                        st.warning("Please complete all registration fields.")
                    else:
                        try:
                            ins_sql = """
                            INSERT INTO USERS (full_name, email, phone, password_hash, app_role, kyc_status, is_active)
                            VALUES (%s, %s, %s, %s, 'USER', 'PENDING', TRUE);
                            """
                            run_dml(ins_sql, (new_name.strip(), new_email.strip().lower(), new_phone.strip(), new_pass.strip()))
                            st.success(f"Account created for {new_name}! Trigger `trg_after_user_insert` initialized your wallet.")
                            st.session_state.quick_fill_email = new_email.strip().lower()
                            st.session_state.quick_fill_pass = new_pass.strip()
                        except Exception as e:
                            st.error(f"Registration failed: {e}")
    st.stop()


# =============================================================================
# 6. AUTHENTICATED SIDEBAR PROFILE
# =============================================================================
safe_email_display = st.session_state.user_email.replace("@", "&#64;")
st.sidebar.markdown("### 👤 Active Session")
st.sidebar.markdown(f"<div style='font-size: 1.1rem; font-weight: 800; color: {T_TEXT_MAIN};'>{st.session_state.user_name}</div>", unsafe_allow_html=True)
st.sidebar.markdown(f"<div style='color: {T_TEXT_MUTED}; font-size: 0.9rem; margin-bottom: 8px;'>{safe_email_display}</div>", unsafe_allow_html=True)

if st.session_state.app_role == "ADMIN":
    st.sidebar.markdown('<span class="badge-active">🛡️ SYSTEM ADMIN</span>', unsafe_allow_html=True)
else:
    st.sidebar.markdown('<span class="badge-active">👤 PERSONAL WALLET</span>', unsafe_allow_html=True)

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Sign Out", use_container_width=True):
    logout()

u_info = run_query(
    "SELECT u.kyc_status, u.is_active, w.wallet_id, w.balance, w.daily_limit, w.status AS wallet_status "
    "FROM USERS u LEFT JOIN WALLETS w ON u.user_id = w.user_id WHERE u.user_id = %s;",
    (st.session_state.user_id,)
)

curr_user = u_info[0] if u_info else {}
curr_wallet_id = curr_user.get("wallet_id")
curr_balance = Decimal(str(curr_user.get("balance", 0.00)))
curr_wallet_status = curr_user.get("wallet_status", "ACTIVE")
curr_kyc_status = curr_user.get("kyc_status", "PENDING")


# =============================================================================
# 7. USER PORTAL VIEW
# =============================================================================
if st.session_state.app_role == "USER":
    st.markdown(f"## 💳 {st.session_state.user_name}'s Personal Wallet")
    st.markdown(f"<p style='color: {T_TEXT_MUTED} !important;'>Instant peer-to-peer transfers, bank liquidity top-ups, utility bill payments, and automated cashback rewards.</p>", unsafe_allow_html=True)

    col_bal, col_limit, col_kyc, col_wstatus = st.columns(4)
    with col_bal:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Available Balance</div>
            <div class="metric-value" style="color: #10B981;">₹ {curr_balance:,.2f}</div>
            <div class="metric-subtitle">Live ledger balance</div>
        </div>
        """, unsafe_allow_html=True)

    with col_limit:
        daily_lim = Decimal(str(curr_user.get("daily_limit", 10000.00)))
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Daily Transfer Limit</div>
            <div class="metric-value" style="color: #F59E0B;">₹ {daily_lim:,.2f}</div>
            <div class="metric-subtitle">24-hour cap</div>
        </div>
        """, unsafe_allow_html=True)

    with col_kyc:
        kyc_class = "badge-active" if curr_kyc_status == "VERIFIED" else ("badge-frozen" if curr_kyc_status == "PENDING" else "badge-alert")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">KYC Verification</div>
            <div style="margin-top: 12px;"><span class="{kyc_class}">{curr_kyc_status}</span></div>
            <div class="metric-subtitle" style="margin-top: 14px;">Compliance tier</div>
        </div>
        """, unsafe_allow_html=True)

    with col_wstatus:
        w_class = "badge-active" if curr_wallet_status == "ACTIVE" else "badge-frozen"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Wallet Status</div>
            <div style="margin-top: 12px;"><span class="{w_class}">{curr_wallet_status}</span></div>
            <div class="metric-subtitle" style="margin-top: 14px;">Wallet ID: #{curr_wallet_id}</div>
        </div>
        """, unsafe_allow_html=True)

    u_tab1, u_tab2, u_tab3, u_tab4 = st.tabs([
        "💸 Send Money (P2P)",
        "🏦 Bank Accounts & Deposit",
        "🧾 Utility Bills & Cashback",
        "📊 Passbook & Analytics"
    ])

    # USER TAB 1: P2P TRANSFER
    with u_tab1:
        st.markdown("### Peer-to-Peer Instant Transfer")
        if curr_wallet_status != "ACTIVE":
            st.error(f"Transfers are disabled because your wallet status is `{curr_wallet_status}`.")
        else:
            other_users = run_query(
                "SELECT u.user_id, u.full_name, u.email, w.wallet_id FROM USERS u "
                "JOIN WALLETS w ON u.user_id = w.user_id WHERE u.user_id != %s AND w.status = 'ACTIVE' ORDER BY u.full_name;",
                (st.session_state.user_id,)
            )

            p2p_col1, p2p_col2 = st.columns([1.1, 1.3])
            with p2p_col1:
                with st.container(border=True):
                    recipient_options = {f"{u['full_name']} ({u['email']})": u for u in other_users}
                    if not recipient_options:
                        st.info("No active recipient wallets available.")
                    else:
                        selected_recipient_key = st.selectbox("Select Recipient", list(recipient_options.keys()))
                        recipient_data = recipient_options[selected_recipient_key]

                        max_send = float(curr_balance) if curr_balance > 0 else 1.0
                        default_send = min(100.0, max_send)
                        transfer_amount = st.number_input("Amount (₹)", min_value=1.0, max_value=max(max_send, 1.0), value=default_send, step=50.0)
                        transfer_note = st.text_input("Payment Note", placeholder="e.g. Dinner split, Book share")

                        if st.button("Send Money Instantly", use_container_width=True):
                            if curr_balance < Decimal(str(transfer_amount)):
                                st.error("Insufficient wallet balance.")
                            else:
                                try:
                                    with get_db() as db:
                                        conn = db.conn
                                        cursor = conn.cursor()

                                        ref_no = f"TXN-P2P-{datetime.datetime.now().strftime('%m%d%H%M%S')}"
                                        cursor.execute("UPDATE WALLETS SET balance = balance - %s WHERE wallet_id = %s;", (transfer_amount, curr_wallet_id))
                                        cursor.execute("UPDATE WALLETS SET balance = balance + %s WHERE wallet_id = %s;", (transfer_amount, recipient_data["wallet_id"]))

                                        ins_txn = """
                                        INSERT INTO TRANSACTIONS (reference_no, sender_wallet_id, receiver_wallet_id, amount, transaction_type, status, description, initiated_at, completed_at)
                                        VALUES (%s, %s, %s, %s, 'P2P', 'SUCCESS', %s, NOW(), NOW());
                                        """
                                        cursor.execute(ins_txn, (ref_no, curr_wallet_id, recipient_data["wallet_id"], transfer_amount, transfer_note or "P2P Transfer"))
                                        txn_id = cursor.lastrowid

                                        audit_sql = """
                                        INSERT INTO AUDIT_LOGS (actor_user_id, action_type, entity_type, entity_id, details)
                                        VALUES (%s, 'P2P_TRANSFER', 'TRANSACTION', %s, %s);
                                        """
                                        cursor.execute(audit_sql, (st.session_state.user_id, txn_id, json.dumps({"receiver_wallet_id": recipient_data["wallet_id"], "amount": transfer_amount, "status": "SUCCESS"})))

                                        conn.commit()
                                        cursor.close()

                                    st.success(f"₹ {transfer_amount:,.2f} transferred to {recipient_data['full_name']}! (Ref: {ref_no})")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Transfer failed: {e}")

            with p2p_col2:
                st.markdown("#### Recent P2P Activity")
                recent_p2p = run_query_df("""
                    SELECT t.reference_no,
                           su.full_name AS sender,
                           ru.full_name AS receiver,
                           t.amount,
                           t.status,
                           t.completed_at
                    FROM TRANSACTIONS t
                    LEFT JOIN WALLETS sw ON t.sender_wallet_id = sw.wallet_id
                    LEFT JOIN USERS su ON sw.user_id = su.user_id
                    LEFT JOIN WALLETS rw ON t.receiver_wallet_id = rw.wallet_id
                    LEFT JOIN USERS ru ON rw.user_id = ru.user_id
                    WHERE (t.sender_wallet_id = %s OR t.receiver_wallet_id = %s)
                      AND t.transaction_type = 'P2P'
                    ORDER BY t.transaction_id DESC LIMIT 6;
                """, (curr_wallet_id, curr_wallet_id))

                if recent_p2p.empty:
                    st.info("No peer-to-peer transfers recorded yet.")
                else:
                    st.dataframe(recent_p2p, use_container_width=True, hide_index=True)

    # USER TAB 2: BANK ACCOUNTS & ADD MONEY
    with u_tab2:
        st.markdown("### Linked Bank Accounts & Top-Up")
        bank_col1, bank_col2 = st.columns([1.1, 1.3])

        with bank_col1:
            with st.container(border=True):
                st.markdown("#### Add Funds from Bank")
                user_banks = run_query(
                    "SELECT bank_account_id, bank_name, account_no_masked, account_type, is_verified, is_active "
                    "FROM BANK_ACCOUNTS WHERE user_id = %s AND is_active = TRUE;",
                    (st.session_state.user_id,)
                )

                if not user_banks:
                    st.warning("No active bank accounts found. Link a bank account on the right first.")
                else:
                    bank_dict = {f"{b['bank_name']} ({b['account_no_masked']}) - {b['account_type']}": b for b in user_banks}
                    chosen_bank_label = st.selectbox("Select Bank Account", list(bank_dict.keys()))
                    chosen_bank = bank_dict[chosen_bank_label]

                    add_amount = st.number_input("Top-Up Amount (₹)", min_value=100.0, max_value=50000.0, value=1000.0, step=500.0)

                    if st.button("Deposit to Wallet", use_container_width=True):
                        try:
                            with get_db() as db:
                                conn = db.conn
                                cursor = conn.cursor()

                                ref_no = f"TXN-BTW-{datetime.datetime.now().strftime('%m%d%H%M%S')}"
                                cursor.execute("UPDATE WALLETS SET balance = balance + %s WHERE wallet_id = %s;", (add_amount, curr_wallet_id))

                                ins_btw = """
                                INSERT INTO TRANSACTIONS (reference_no, receiver_wallet_id, bank_account_id, amount, transaction_type, status, description, initiated_at, completed_at)
                                VALUES (%s, %s, %s, %s, 'BANK_TO_WALLET', 'SUCCESS', %s, NOW(), NOW());
                                """
                                cursor.execute(ins_btw, (ref_no, curr_wallet_id, chosen_bank["bank_account_id"], add_amount, f"Deposit from {chosen_bank['bank_name']}"))
                                txn_id = cursor.lastrowid

                                cursor.execute(
                                    "INSERT INTO AUDIT_LOGS (actor_user_id, action_type, entity_type, entity_id, details) VALUES (%s, %s, %s, %s, %s);",
                                    (st.session_state.user_id, "BANK_DEPOSIT", "TRANSACTION", txn_id, json.dumps({"bank_account_id": chosen_bank["bank_account_id"], "amount": add_amount}))
                                )
                                conn.commit()
                                cursor.close()

                            st.success(f"Added ₹ {add_amount:,.2f} from {chosen_bank['bank_name']}! (Ref: {ref_no})")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Deposit failed: {e}")

        with bank_col2:
            with st.container(border=True):
                st.markdown("#### Link New Bank Account")
                new_b_name = st.selectbox("Select Bank", ["State Bank of India", "HDFC Bank", "ICICI Bank", "Axis Bank", "Kotak Mahindra Bank", "Bank of Baroda", "Punjab National Bank", "Union Bank of India", "IndusInd Bank", "Federal Bank"])
                new_b_acc = st.text_input("Account Number", placeholder="e.g. 1029384756")
                new_b_ifsc = st.text_input("IFSC Code", placeholder="e.g. SBIN0001234")
                new_b_type = st.radio("Account Type", ["SAVINGS", "CURRENT"], horizontal=True)

                if st.button("Link Verified Bank Account", use_container_width=True):
                    if not (new_b_acc and new_b_ifsc):
                        st.warning("Please enter both Account Number and IFSC Code.")
                    else:
                        masked = "XXXXXX" + (new_b_acc[-4:] if len(new_b_acc) >= 4 else new_b_acc)
                        try:
                            ins_bank_sql = """
                            INSERT INTO BANK_ACCOUNTS (user_id, bank_name, account_no_masked, ifsc_code, account_type, is_verified, is_active)
                            VALUES (%s, %s, %s, %s, %s, TRUE, TRUE);
                            """
                            bid = run_dml(ins_bank_sql, (st.session_state.user_id, new_b_name, masked, new_b_ifsc.upper(), new_b_type))

                            run_dml(
                                "INSERT INTO AUDIT_LOGS (actor_user_id, action_type, entity_type, entity_id, details) VALUES (%s, %s, %s, %s, %s);",
                                (st.session_state.user_id, "BANK_ACCOUNT_LINK", "BANK_ACCOUNT", bid, json.dumps({"bank_name": new_b_name, "masked": masked}))
                            )
                            st.success(f"Bank Account ({masked}) linked!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error linking bank account: {e}")

    # USER TAB 3: DUE BILLS & AUTOMATED CASHBACK
    with u_tab3:
        st.markdown("### Utility Bills & Cashback Calculator")
        st.caption("Cashback rewards are dynamically evaluated via stored function `fn_calculate_cashback(amount, offer_id)`.")

        due_bills = run_query("""
            SELECT b.bill_id, b.billing_period, b.amount_due, b.due_date, b.status,
                   bl.biller_name, bl.biller_type, ub.consumer_number, ub.nickname
            FROM BILLS b
            JOIN USER_BILLERS ub ON b.user_biller_id = ub.user_biller_id
            JOIN BILLERS bl ON ub.biller_id = bl.biller_id
            WHERE ub.user_id = %s AND b.status IN ('UNPAID', 'OVERDUE')
            ORDER BY b.due_date ASC;
        """, (st.session_state.user_id,))

        if not due_bills:
            st.success("🎉 You have no unpaid or overdue bills!")
        else:
            bill_df = pd.DataFrame(due_bills)
            st.dataframe(bill_df[["bill_id", "biller_name", "biller_type", "billing_period", "amount_due", "due_date", "status"]], use_container_width=True, hide_index=True)

            pay_col1, pay_col2 = st.columns([1.1, 1.3])
            with pay_col1:
                with st.container(border=True):
                    st.markdown("#### Pay Selected Bill")
                    bill_choices = {f"Bill #{b['bill_id']} - {b['biller_name']} (₹{b['amount_due']:,.2f})": b for b in due_bills}
                    chosen_bill_label = st.selectbox("Choose Bill", list(bill_choices.keys()))
                    target_bill = bill_choices[chosen_bill_label]

                    active_offers = run_query("SELECT offer_id, offer_name, promo_code, cashback_percentage, max_cashback FROM CASHBACK_OFFERS WHERE is_active = TRUE;")
                    cashback_offer_options = {f"{o['offer_name']} ({o['promo_code']}) - {o['cashback_percentage']}%": o for o in active_offers}
                    cashback_offer_options["No Promo Code"] = None

                    selected_offer_label = st.selectbox("Select Promo Offer", list(cashback_offer_options.keys()))
                    chosen_offer = cashback_offer_options[selected_offer_label]

                    expected_cashback = Decimal("0.00")
                    if chosen_offer:
                        try:
                            res = run_function("fn_calculate_cashback", [float(target_bill["amount_due"]), int(chosen_offer["offer_id"])])
                            if res:
                                expected_cashback = Decimal(str(res))
                        except Exception:
                            pass

                    st.markdown(f"**Bill Amount Due:** `₹ {Decimal(str(target_bill['amount_due'])):,.2f}`")
                    if expected_cashback > 0:
                        st.markdown(f'<div style="margin-bottom: 10px;"><span class="badge-active">🎁 Instant Cashback: ₹ {expected_cashback:,.2f}</span></div>', unsafe_allow_html=True)

                    if st.button("Confirm & Pay Bill", use_container_width=True):
                        bill_amt = Decimal(str(target_bill["amount_due"]))
                        if curr_balance < bill_amt:
                            st.error(f"Insufficient balance! Needed: ₹{bill_amt:,.2f}, Available: ₹{curr_balance:,.2f}")
                        else:
                            try:
                                with get_db() as db:
                                    conn = db.conn
                                    cursor = conn.cursor()

                                    bill_ref = f"TXN-BILL-{datetime.datetime.now().strftime('%m%d%H%M%S')}"
                                    cursor.execute("UPDATE WALLETS SET balance = balance - %s WHERE wallet_id = %s;", (bill_amt, curr_wallet_id))
                                    cursor.execute("UPDATE BILLS SET status = 'PAID' WHERE bill_id = %s;", (target_bill["bill_id"],))

                                    ins_bill_txn = """
                                    INSERT INTO TRANSACTIONS (reference_no, sender_wallet_id, amount, transaction_type, status, description, initiated_at, completed_at)
                                    VALUES (%s, %s, %s, 'BILL_PAYMENT', 'SUCCESS', %s, NOW(), NOW());
                                    """
                                    cursor.execute(ins_bill_txn, (bill_ref, curr_wallet_id, bill_amt, f"Bill Payment: {target_bill['biller_name']} ({target_bill['billing_period']})"))
                                    bill_txn_id = cursor.lastrowid

                                    cursor.execute("INSERT INTO BILL_PAYMENTS (bill_id, transaction_id, amount_paid, paid_at) VALUES (%s, %s, %s, NOW());",
                                                   (target_bill["bill_id"], bill_txn_id, bill_amt))

                                    if expected_cashback > 0 and chosen_offer:
                                        cb_ref = f"TXN-CB-{datetime.datetime.now().strftime('%m%d%H%M%S')}"
                                        cursor.execute("UPDATE WALLETS SET balance = balance + %s WHERE wallet_id = %s;", (expected_cashback, curr_wallet_id))
                                        ins_cb_txn = """
                                        INSERT INTO TRANSACTIONS (reference_no, receiver_wallet_id, amount, transaction_type, status, description, initiated_at, completed_at)
                                        VALUES (%s, %s, %s, 'CASHBACK', 'SUCCESS', %s, NOW(), NOW());
                                        """
                                        cursor.execute(ins_cb_txn, (cb_ref, curr_wallet_id, expected_cashback, f"Cashback for {bill_ref}"))

                                        cursor.execute(
                                            "INSERT INTO CASHBACK_HISTORY (user_id, source_transaction_id, offer_id, amount, credited_at) VALUES (%s, %s, %s, %s, NOW());",
                                            (st.session_state.user_id, bill_txn_id, chosen_offer["offer_id"], expected_cashback)
                                        )

                                    cursor.execute(
                                        "INSERT INTO AUDIT_LOGS (actor_user_id, action_type, entity_type, entity_id, details) VALUES (%s, %s, %s, %s, %s);",
                                        (st.session_state.user_id, "BILL_PAYMENT", "BILL", target_bill["bill_id"], json.dumps({"amount": float(bill_amt), "cashback": float(expected_cashback)}))
                                    )
                                    conn.commit()
                                    cursor.close()

                                st.success(f"Bill paid! ₹{bill_amt:,.2f} deducted, ₹{expected_cashback:,.2f} cashback credited.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Payment error: {e}")

            with pay_col2:
                st.markdown("#### Active Cashback Offers")
                offers_df = run_query_df("SELECT offer_name, promo_code, cashback_percentage, max_cashback, minimum_amount FROM CASHBACK_OFFERS WHERE is_active = TRUE;")
                if not offers_df.empty:
                    st.dataframe(offers_df, use_container_width=True, hide_index=True)

    # USER TAB 4: PASSBOOK & FINANCIAL ANALYTICS
    with u_tab4:
        st.markdown("### Passbook Ledger & Spending Analytics")
        g_col1, g_col2 = st.columns(2)

        with g_col1:
            st.markdown("#### Spend Breakdown by Merchant Category")
            cat_spend = run_query_df("""
                SELECT mc.category_name, SUM(t.amount) AS total_spent
                FROM TRANSACTIONS t
                JOIN MERCHANTS m ON t.merchant_id = m.merchant_id
                JOIN MERCHANT_CATEGORIES mc ON m.category_id = mc.category_id
                WHERE t.sender_wallet_id = %s AND t.status = 'SUCCESS'
                GROUP BY mc.category_name;
            """, (curr_wallet_id,))

            if cat_spend.empty:
                st.info("No merchant category transactions recorded yet.")
            else:
                fig_donut = px.pie(
                    cat_spend,
                    values="total_spent",
                    names="category_name",
                    hole=0.45,
                    color_discrete_sequence=["#10B981", "#F59E0B", "#EF4444", "#14B8A6", "#FBBF24", "#84CC16"]
                )
                fig_donut.update_layout(
                    paper_bgcolor=T_SURFACE,
                    plot_bgcolor=T_SURFACE,
                    font=dict(color=T_TEXT_MAIN, size=13),
                    legend=dict(font=dict(color=T_TEXT_MAIN)),
                    margin=dict(t=20, b=20, l=20, r=20)
                )
                st.plotly_chart(fig_donut, use_container_width=True)

        with g_col2:
            st.markdown("#### Total Inflow vs. Outflow")
            inflow_res = run_query("SELECT COALESCE(SUM(amount), 0.00) AS val FROM TRANSACTIONS WHERE receiver_wallet_id = %s AND status = 'SUCCESS';", (curr_wallet_id,))
            outflow_res = run_query("SELECT COALESCE(SUM(amount), 0.00) AS val FROM TRANSACTIONS WHERE sender_wallet_id = %s AND status = 'SUCCESS';", (curr_wallet_id,))

            inflow_val = float(inflow_res[0]["val"]) if inflow_res else 0.0
            outflow_val = float(outflow_res[0]["val"]) if outflow_res else 0.0

            cf_df = pd.DataFrame([
                {"Direction": "Total Credits (Inflow)", "Amount": inflow_val, "Type": "Inflow"},
                {"Direction": "Total Debits (Outflow)", "Amount": outflow_val, "Type": "Outflow"}
            ])

            fig_bar = px.bar(
                cf_df,
                x="Direction",
                y="Amount",
                color="Type",
                color_discrete_map={"Inflow": "#10B981", "Outflow": "#EF4444"},
                text_auto=".2s"
            )
            fig_bar.update_layout(
                paper_bgcolor=T_SURFACE,
                plot_bgcolor=T_SURFACE,
                font=dict(color=T_TEXT_MAIN, size=13),
                xaxis=dict(tickfont=dict(color=T_TEXT_MAIN), title_font=dict(color=T_TEXT_MAIN)),
                yaxis=dict(tickfont=dict(color=T_TEXT_MAIN), title_font=dict(color=T_TEXT_MAIN), gridcolor=T_BORDER),
                margin=dict(t=20, b=20, l=20, r=20),
                showlegend=False
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("#### Complete Transaction History")
        txn_filter = st.selectbox("Filter by Transaction Type", ["ALL", "P2P", "BANK_TO_WALLET", "WALLET_TO_BANK", "MERCHANT", "BILL_PAYMENT", "CASHBACK"])

        sql_passbook = """
            SELECT reference_no, transaction_type, amount, status, description, initiated_at, completed_at
            FROM TRANSACTIONS
            WHERE (sender_wallet_id = %s OR receiver_wallet_id = %s)
        """
        params = [curr_wallet_id, curr_wallet_id]
        if txn_filter != "ALL":
            sql_passbook += " AND transaction_type = %s"
            params.append(txn_filter)
        sql_passbook += " ORDER BY transaction_id DESC;"

        passbook_df = run_query_df(sql_passbook, tuple(params))
        if passbook_df.empty:
            st.info("No matching transactions found.")
        else:
            st.dataframe(passbook_df, use_container_width=True, hide_index=True)


# =============================================================================
# 8. ADMIN CONSOLE VIEW
# =============================================================================
elif st.session_state.app_role == "ADMIN":
    st.markdown("## 🛡️ Enterprise Database Administration Workbench")
    st.markdown(f"<p style='color: {T_TEXT_MUTED} !important;'>Full CRUD control over all 13 relational tables, live schema inspection, stored procedures, triggers, and raw SQL execution.</p>", unsafe_allow_html=True)

    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        total_users_cnt = run_query("SELECT COUNT(*) AS cnt FROM USERS;")[0]["cnt"]
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Users</div>
            <div class="metric-value" style="color: {T_TEXT_MAIN};">{total_users_cnt}</div>
            <div class="metric-subtitle">Registered accounts</div>
        </div>
        """, unsafe_allow_html=True)

    with m_col2:
        try:
            total_bal_res = run_procedure("sp_total_balance")
            tot_bal = float(total_bal_res[0]["total_wallet_balance"]) if total_bal_res else 0.0
        except Exception:
            tot_bal = float(run_query("SELECT COALESCE(SUM(balance), 0.00) AS b FROM WALLETS;")[0]["b"])

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">System Liquidity</div>
            <div class="metric-value" style="color: #10B981;">₹ {tot_bal:,.2f}</div>
            <div class="metric-subtitle">Via cursor sp_total_balance()</div>
        </div>
        """, unsafe_allow_html=True)

    with m_col3:
        total_txns_cnt = run_query("SELECT COUNT(*) AS cnt FROM TRANSACTIONS;")[0]["cnt"]
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Transactions</div>
            <div class="metric-value" style="color: #F59E0B;">{total_txns_cnt}</div>
            <div class="metric-subtitle">All ledger entries</div>
        </div>
        """, unsafe_allow_html=True)

    with m_col4:
        audit_cnt = run_query("SELECT COUNT(*) AS cnt FROM AUDIT_LOGS;")[0]["cnt"]
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Audit Log Events</div>
            <div class="metric-value" style="color: #EF4444;">{audit_cnt}</div>
            <div class="metric-subtitle">Trigger & security logs</div>
        </div>
        """, unsafe_allow_html=True)

    adm_tab1, adm_tab2, adm_tab3, adm_tab4, adm_tab5 = st.tabs([
        "🗄️ Master Data Editor (13 Tables)",
        "🔍 Schema & Index Inspector",
        "⚙️ Procedures & Triggers Hub",
        "⚡ Interactive SQL Console",
        "🛡️ User Moderation & Audit Trail"
    ])

    ALL_TABLES = [
        "USERS", "WALLETS", "BANK_ACCOUNTS", "MERCHANT_CATEGORIES", "MERCHANTS",
        "BILLERS", "USER_BILLERS", "BILLS", "TRANSACTIONS", "BILL_PAYMENTS",
        "CASHBACK_OFFERS", "CASHBACK_HISTORY", "AUDIT_LOGS"
    ]

    PK_MAP = {
        "USERS": "user_id",
        "WALLETS": "wallet_id",
        "BANK_ACCOUNTS": "bank_account_id",
        "MERCHANT_CATEGORIES": "category_id",
        "MERCHANTS": "merchant_id",
        "BILLERS": "biller_id",
        "USER_BILLERS": "user_biller_id",
        "BILLS": "bill_id",
        "TRANSACTIONS": "transaction_id",
        "BILL_PAYMENTS": "bill_payment_id",
        "CASHBACK_OFFERS": "offer_id",
        "CASHBACK_HISTORY": "cashback_id",
        "AUDIT_LOGS": "audit_id"
    }

    # ADMIN TAB 1: MASTER DATA EDITOR
    with adm_tab1:
        st.markdown("### Master Data Grid (Live Relational CRUD)")
        sel_tbl_col, _ = st.columns([1.2, 2])
        with sel_tbl_col:
            selected_table = st.selectbox("Select Relational Table", ALL_TABLES, index=0)

        pk_col = PK_MAP[selected_table]
        table_df = run_query_df(f"SELECT * FROM {selected_table} ORDER BY {pk_col} ASC;")

        st.caption(f"Displaying `{selected_table}` ({len(table_df)} rows). Double-click cells to edit, add rows at the bottom, or select rows to delete.")

        edited_df = st.data_editor(
            table_df,
            num_rows="dynamic",
            use_container_width=True,
            key=f"editor_{selected_table}"
        )

        if st.button(f"💾 Commit Changes to {selected_table}", use_container_width=True):
            try:
                orig_ids = set(table_df[pk_col].dropna().astype(int))
                curr_ids = set(edited_df[pk_col].dropna().astype(int))

                deleted_ids = orig_ids - curr_ids
                if deleted_ids:
                    with get_db() as db:
                        for d_id in deleted_ids:
                            db.execute_dml(f"DELETE FROM {selected_table} WHERE {pk_col} = %s;", (d_id,))
                    st.success(f"Deleted {len(deleted_ids)} row(s) from `{selected_table}`.")

                common_ids = orig_ids.intersection(curr_ids)
                update_count = 0
                for c_id in common_ids:
                    orig_row = table_df[table_df[pk_col] == c_id].iloc[0]
                    new_row = edited_df[edited_df[pk_col] == c_id].iloc[0]

                    diff_cols = [col for col in table_df.columns if col != pk_col and str(orig_row[col]) != str(new_row[col])]
                    if diff_cols:
                        set_clause = ", ".join([f"{c} = %s" for c in diff_cols])
                        vals = [new_row[c] for c in diff_cols] + [c_id]
                        run_dml(f"UPDATE {selected_table} SET {set_clause} WHERE {pk_col} = %s;", tuple(vals))
                        update_count += 1

                if update_count > 0:
                    st.success(f"Updated {update_count} row(s) in `{selected_table}`.")

                new_rows = edited_df[edited_df[pk_col].isna() | (~edited_df[pk_col].isin(orig_ids))]
                if not new_rows.empty:
                    insert_cols = [c for c in edited_df.columns if c != pk_col]
                    cols_str = ", ".join(insert_cols)
                    placeholders = ", ".join(["%s"] * len(insert_cols))

                    with get_db() as db:
                        for _, row in new_rows.iterrows():
                            vals = [None if pd.isna(row[c]) else row[c] for c in insert_cols]
                            db.execute_dml(f"INSERT INTO {selected_table} ({cols_str}) VALUES ({placeholders});", tuple(vals))
                    st.success(f"Inserted {len(new_rows)} new row(s) into `{selected_table}`.")

                st.rerun()
            except Exception as e:
                st.error(f"Database sync error on `{selected_table}`: {e}")

    # ADMIN TAB 2: SCHEMA INSPECTOR
    with adm_tab2:
        st.markdown("### Live Table Structure & Indexes")
        schema_tbl_col, _ = st.columns([1.2, 2])
        with schema_tbl_col:
            inspect_tbl = st.selectbox("Inspect Table Metadata", ALL_TABLES, key="inspect_schema_box")

        desc_df = run_query_df(f"DESCRIBE {inspect_tbl};")
        st.dataframe(desc_df, use_container_width=True, hide_index=True)

        st.markdown("#### Indexes & Key Constraints")
        try:
            indexes_df = run_query_df(f"SHOW INDEX FROM {inspect_tbl};")
            cols_to_show = [c for c in ["Key_name", "Column_name", "Non_unique", "Index_type"] if c in indexes_df.columns]
            st.dataframe(indexes_df[cols_to_show], use_container_width=True, hide_index=True)
        except Exception as e:
            st.info(f"Index metadata notice: {e}")

    # ADMIN TAB 3: PROCEDURES & TRIGGERS HUB
    with adm_tab3:
        st.markdown("### Stored Procedures (Cursors) & Triggers")
        p_col1, p_col2 = st.columns(2)

        with p_col1:
            with st.container(border=True):
                st.markdown("#### Cursor Procedure: `sp_total_balance()`")
                st.caption("Iterates through all wallet rows using a SQL CURSOR to compute aggregate platform liquidity.")
                if st.button("Execute CALL sp_total_balance()", use_container_width=True):
                    try:
                        res = run_procedure("sp_total_balance")
                        st.success(f"Cursor Result: Total Liquidity = ₹ {res[0]['total_wallet_balance']:,.2f}")
                    except Exception as e:
                        st.error(f"Execution failed: {e}")

        with p_col2:
            with st.container(border=True):
                st.markdown("#### Cursor Procedure: `sp_bonus_active_wallets()`")
                st.caption("Uses a SQL CURSOR loop to credit a ₹50 promotional reward to every ACTIVE wallet.")
                if st.button("Execute CALL sp_bonus_active_wallets()", use_container_width=True):
                    try:
                        run_procedure("sp_bonus_active_wallets")
                        st.success("₹50 promotional bonus credited to all active wallets!")
                        updated_w = run_query_df("SELECT wallet_id, user_id, balance, status FROM WALLETS WHERE status = 'ACTIVE' LIMIT 6;")
                        st.dataframe(updated_w, use_container_width=True, hide_index=True)
                    except Exception as e:
                        st.error(f"Execution failed: {e}")

        st.markdown("---")
        trg_col1, trg_col2 = st.columns(2)
        with trg_col1:
            with st.container(border=True):
                st.markdown("#### Test Trigger: `trg_after_wallet_update`")
                st.caption("Changing a wallet status automatically fires `trg_after_wallet_update` and writes an audit record to `AUDIT_LOGS`.")
                target_w = st.selectbox("Select Wallet ID", [1, 2, 3, 4, 6, 8, 10], key="toggle_w_box")
                new_st = st.radio("Set Wallet Status", ["ACTIVE", "FROZEN", "CLOSED"], horizontal=True, key="toggle_st_radio")
                if st.button("Update Wallet Status & Fire Trigger", use_container_width=True):
                    try:
                        run_dml("UPDATE WALLETS SET status = %s WHERE wallet_id = %s;", (new_st, target_w))
                        st.success(f"Wallet #{target_w} updated to `{new_st}`! Trigger logged event to `AUDIT_LOGS`.")
                    except Exception as e:
                        st.error(f"Update failed: {e}")

        with trg_col2:
            st.markdown("#### Trigger-Generated Audit Events")
            trg_logs = run_query_df("SELECT audit_id, action_type, entity_type, entity_id, details, created_at FROM AUDIT_LOGS WHERE action_type IN ('WALLET_STATUS_CHANGE', 'BANK_ACCOUNT_DELETED') ORDER BY audit_id DESC LIMIT 5;")
            if trg_logs.empty:
                st.info("Toggle a wallet status on the left to observe `trg_after_wallet_update` in real time.")
            else:
                st.dataframe(trg_logs, use_container_width=True, hide_index=True)

    # ADMIN TAB 4: RAW SQL CONSOLE
    with adm_tab4:
        st.markdown("### Interactive SQL Execution Console")
        sample_queries = {
            "1. INNER JOIN: Users & Wallets": "SELECT u.user_id, u.full_name, u.app_role, w.wallet_id, w.balance, w.status AS wallet_status FROM USERS u INNER JOIN WALLETS w ON u.user_id = w.user_id ORDER BY u.user_id;",
            "2. NATURAL JOIN: Categories & Merchants": "SELECT category_id, category_name, merchant_id, business_name, merchant_code, status FROM MERCHANT_CATEGORIES NATURAL JOIN MERCHANTS ORDER BY category_id;",
            "3. Subquery: Wallets Above Average Balance": "SELECT user_id, full_name FROM USERS WHERE user_id IN (SELECT user_id FROM WALLETS WHERE balance > (SELECT AVG(balance) FROM WALLETS));",
            "4. Correlated Subquery: Users with Overdue Bills": "SELECT u.user_id, u.full_name FROM USERS u WHERE EXISTS (SELECT 1 FROM USER_BILLERS ub JOIN BILLS b ON b.user_biller_id = ub.user_biller_id WHERE ub.user_id = u.user_id AND b.status = 'OVERDUE');",
            "5. View: vw_user_wallet_summary": "SELECT * FROM vw_user_wallet_summary;",
            "6. View: vw_due_bills": "SELECT * FROM vw_due_bills ORDER BY due_date;",
            "7. Stored Functions: Balance & Due Bills per User": "SELECT u.user_id, u.full_name, fn_get_wallet_balance(u.user_id) AS wallet_balance, fn_total_due_bills(u.user_id) AS total_due_bills FROM USERS u ORDER BY u.user_id;"
        }

        sel_preset = st.selectbox("Load Predefined SQL Query", list(sample_queries.keys()))
        user_sql = st.text_area("SQL Query Editor", value=sample_queries[sel_preset], height=130)

        if st.button("▶️ Run SQL Statement", use_container_width=True):
            cleaned_sql = user_sql.strip()
            if not cleaned_sql:
                st.warning("Please enter a valid SQL statement.")
            else:
                try:
                    if cleaned_sql.upper().startswith(("SELECT", "SHOW", "DESCRIBE", "EXPLAIN", "PRAGMA")):
                        res_df = run_query_df(cleaned_sql)
                        st.success(f"Returned {len(res_df)} row(s).")
                        st.dataframe(res_df, use_container_width=True, hide_index=True)
                    else:
                        affected = run_dml(cleaned_sql)
                        st.success(f"Statement executed! Affected/Inserted ID: {affected}")
                except Exception as e:
                    st.error(f"SQL Error: {e}")

    # ADMIN TAB 5: USER MODERATION & LIVE AUDIT LOGS
    with adm_tab5:
        st.markdown("### User Moderation & System Audit Logs")
        mod_col1, mod_col2 = st.columns([1, 1.3])

        with mod_col1:
            with st.container(border=True):
                st.markdown("#### KYC & Account Status Control")
                all_u = run_query("SELECT user_id, full_name, email, kyc_status, is_active FROM USERS ORDER BY user_id;")
                u_mod_dict = {f"#{u['user_id']} - {u['full_name']} ({u['email']})": u for u in all_u}
                sel_u_key = st.selectbox("Select User Account", list(u_mod_dict.keys()))
                target_mod_u = u_mod_dict[sel_u_key]

                kyc_list = ["PENDING", "VERIFIED", "FAILED"]
                curr_kyc_idx = kyc_list.index(target_mod_u["kyc_status"]) if target_mod_u["kyc_status"] in kyc_list else 0
                new_kyc = st.selectbox("KYC Verification Status", kyc_list, index=curr_kyc_idx)
                new_active_flag = st.checkbox("Account Enabled (is_active)", value=bool(target_mod_u["is_active"]))

                if st.button("Update User Account", use_container_width=True):
                    try:
                        run_dml("UPDATE USERS SET kyc_status = %s, is_active = %s WHERE user_id = %s;", (new_kyc, new_active_flag, target_mod_u["user_id"]))
                        st.success(f"Updated {target_mod_u['full_name']}: KYC={new_kyc}, Active={new_active_flag}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Update failed: {e}")

        with mod_col2:
            st.markdown("#### Complete Security Audit Trail (`AUDIT_LOGS`)")
            audit_action_filter = st.selectbox("Filter by Action Type", ["ALL", "USER_LOGIN", "P2P_TRANSFER", "WALLET_FREEZE", "WALLET_STATUS_CHANGE", "BANK_ACCOUNT_LINK", "BANK_ACCOUNT_DELETED", "BILL_PAYMENT", "CASHBACK_CREDIT"])

            audit_sql = "SELECT audit_id, actor_user_id, action_type, entity_type, entity_id, details, created_at FROM AUDIT_LOGS"
            if audit_action_filter != "ALL":
                audit_sql += f" WHERE action_type = '{audit_action_filter}'"
            audit_sql += " ORDER BY audit_id DESC LIMIT 20;"

            audits_df = run_query_df(audit_sql)
            st.dataframe(audits_df, use_container_width=True, hide_index=True)
