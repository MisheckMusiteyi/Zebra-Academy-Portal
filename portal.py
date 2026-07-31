import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date, timedelta
import time
import json
import base64
from PIL import Image
import io
import re
import random

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Zebra Academy Portal",
    page_icon="ZA",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# BRANDING
# ============================================================
SCHOOL_NAME = "Zebra Academy"
SCHOOL_LOGO_URL = "https://raw.githubusercontent.com/MisheckMusiteyi/Zebra-Academy-Portal/main/Zebra%20Academy.jpg"
SHEET_NAME = "Zebra Academy"

# Colors (from logo)
MAROON = "#6B1F32"
MAROON_DARK = "#5C1A29"
MAROON_TEXT = "#1A0A0E"
WHITE = "#FFFFFF"
OFF_WHITE = "#FAFAFA"
CARD_BORDER = "#E0D5D8"
CARD_ALT_ROW = "#F8F4F5"
GREEN = "#4CAF50"
RED = "#E74C3C"
SKY_BLUE = "#5C1A29"
LIGHT_GREY = "#E0D5D8"

# ============================================================
# CSS - ZEBRA ACADEMY MAROON THEME (STREAMLIT OVERRIDES FIXED)
# ============================================================
def inject_css():
    st.markdown(f"""
    <style>
        /* ============================================= */
        /* FORCE LIGHT THEME - OVERRIDE EVERYTHING */
        /* ============================================= */
        
        :root, [data-theme="light"], [data-theme="dark"] {{
            --background-color: {OFF_WHITE} !important;
            --text-color: {MAROON_TEXT} !important;
            --font: 'Georgia', 'Times New Roman', serif !important;
            --primary-color: {MAROON} !important;
        }}
        
        html, body, [data-testid="stAppViewContainer"], .main, .block-container {{
            background-color: {OFF_WHITE} !important;
            color: {MAROON_TEXT} !important;
        }}
        
        html, body, div, p, span, a, li, td, th, label, input, select, textarea, button {{
            font-family: 'Georgia', 'Times New Roman', serif !important;
        }}
        
        [style*="Material Symbols"], .material-symbols-outlined, .material-symbols-rounded,
        .material-symbols-sharp, [data-testid="stMarkdownContainer"] span[style*="font-family: Material"] {{
            font-family: 'Material Symbols Rounded', 'Material Symbols Outlined',
                         'Material Symbols Sharp', sans-serif !important;
        }}
        
        /* ============================================= */
        /* BUTTONS */
        /* ============================================= */
        .stButton > button {{
            background-color: {MAROON} !important;
            color: {WHITE} !important;
            border: none !important;
            border-radius: 6px !important;
            font-weight: bold !important;
        }}
        .stButton > button:hover {{
            background-color: {MAROON_DARK} !important;
            color: {WHITE} !important;
        }}
        .stButton > button p, .stButton > button span, .stButton > button div,
        .stButton > button label, .stButton > button * {{
            color: {WHITE} !important;
            font-family: 'Georgia', 'Times New Roman', serif !important;
        }}
        
        /* ============================================= */
        /* TABS */
        /* ============================================= */
        .stTabs [aria-selected="true"] {{
            background-color: {MAROON} !important;
            color: {WHITE} !important;
        }}
        .stTabs [aria-selected="true"] p, .stTabs [aria-selected="true"] span,
        .stTabs [aria-selected="true"] div, .stTabs [aria-selected="true"] * {{
            color: {WHITE} !important;
        }}
        .stTabs [aria-selected="false"] {{
            color: {MAROON_TEXT} !important;
        }}
        .stTabs [aria-selected="false"] p, .stTabs [aria-selected="false"] span {{
            color: {MAROON_TEXT} !important;
        }}
        
        /* ============================================= */
        /* SIDEBAR */
        /* ============================================= */
        [data-testid="stSidebar"] {{
            background-color: {MAROON} !important;
            min-width: 300px !important;
            max-width: 300px !important;
        }}
        [data-testid="stSidebar"] * {{
            color: {WHITE} !important;
        }}
        [data-testid="stSidebar"] button {{
            background-color: {MAROON_DARK} !important;
            border: none !important;
            border-radius: 6px !important;
            color: {WHITE} !important;
        }}
        [data-testid="stSidebar"] button:hover {{
            background-color: #4A1522 !important;
        }}
        [data-testid="stSidebar"] button p, [data-testid="stSidebar"] button span,
        [data-testid="stSidebar"] button div, [data-testid="stSidebar"] button * {{
            color: {WHITE} !important;
        }}
        [data-testid="collapsedControl"] {{
            display: none;
        }}
        
        /* ============================================= */
        /* HEADERS */
        /* ============================================= */
        h1, h2, h3, h4, h5, h6 {{
            color: {MAROON} !important;
            font-family: 'Georgia', 'Times New Roman', serif !important;
        }}
        
        /* ============================================= */
        /* INPUT FIELDS */
        /* ============================================= */
        input, textarea, select {{
            color: {MAROON_TEXT} !important;
            background-color: {WHITE} !important;
            border: 1px solid {CARD_BORDER} !important;
        }}
        label, .stTextInput label, .stNumberInput label, .stSelectbox label, .stDateInput label {{
            color: {MAROON_TEXT} !important;
        }}
        
        /* ============================================= */
        /* DATA FRAMES & TABLES */
        /* ============================================= */
        [data-testid="stDataFrame"] td, [data-testid="stTable"] td,
        .stDataFrame td, .dataframe td {{
            color: {MAROON_TEXT} !important;
        }}
        [data-testid="stDataFrame"] th, [data-testid="stTable"] th,
        .stDataFrame th, .dataframe th {{
            color: {WHITE} !important;
            background-color: {MAROON} !important;
        }}
        
        /* ============================================= */
        /* METRICS */
        /* ============================================= */
        [data-testid="stMetricValue"] {{
            color: {MAROON} !important;
        }}
        [data-testid="stMetricLabel"] {{
            color: {MAROON_TEXT} !important;
        }}
        
        /* ============================================= */
        /* ALERTS */
        /* ============================================= */
        .stAlert, [data-testid="stAlert"] {{
            color: {MAROON_TEXT} !important;
        }}
        .stAlert p, [data-testid="stAlert"] p {{
            color: {MAROON_TEXT} !important;
        }}
        
        /* ============================================= */
        /* SELECTBOX DROPDOWN */
        /* ============================================= */
        .stSelectbox div[data-baseweb="select"] > div {{
            color: {MAROON_TEXT} !important;
            background-color: {WHITE} !important;
        }}
        
        /* ============================================= */
        /* RADIO BUTTONS */
        /* ============================================= */
        .stRadio label, .stRadio p, .stRadio span {{
            color: {MAROON_TEXT} !important;
        }}
        
        /* ============================================= */
        /* CHECKBOX */
        /* ============================================= */
        .stCheckbox label, .stCheckbox p, .stCheckbox span {{
            color: {MAROON_TEXT} !important;
        }}
        
        /* ============================================= */
        /* EXPANDER */
        /* ============================================= */
        .streamlit-expanderHeader {{
            color: {MAROON_TEXT} !important;
        }}
        
        /* ============================================= */
        /* CUSTOM COMPONENTS */
        /* ============================================= */
        .top-banner {{
            background-color: {MAROON};
            padding: 20px 40px;
            display: flex;
            align-items: center;
            gap: 20px;
            margin: -100px -100px 30px -100px;
        }}
        .top-banner img {{
            height: 60px;
            border-radius: 8px;
        }}
        .top-banner h1 {{
            color: {WHITE} !important;
            margin: 0;
            font-size: 28px;
        }}
        
        .login-container {{
            max-width: 450px;
            margin: 0 auto;
            background: {WHITE};
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            border: 1px solid {CARD_BORDER};
        }}
        .login-container h3 {{
            color: {MAROON} !important;
        }}
        .login-container label {{
            color: {MAROON_TEXT} !important;
        }}
        
        .bottom-footer {{
            background-color: {MAROON};
            color: {WHITE};
            text-align: center;
            padding: 15px;
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            font-size: 13px;
        }}
        
        .dash-card {{
            background: {WHITE};
            border-radius: 10px;
            border: 1px solid {CARD_BORDER};
            margin-bottom: 20px;
            overflow: hidden;
        }}
        .dash-card-header {{
            background-color: {MAROON};
            color: {WHITE} !important;
            padding: 14px 20px;
            font-size: 16px;
            font-weight: bold;
        }}
        .dash-card-body {{
            padding: 20px;
        }}
        .dash-card-body p, .dash-card-body span, .dash-card-body div,
        .dash-card-body label, .dash-card-body li {{
            color: {MAROON_TEXT} !important;
        }}
        
        .metric-card {{
            background: {WHITE};
            border-radius: 10px;
            border: 1px solid {CARD_BORDER};
            padding: 20px;
            text-align: center;
        }}
        .metric-value {{
            font-size: 32px;
            font-weight: bold;
            color: {MAROON};
        }}
        .metric-label {{
            font-size: 13px;
            color: {SKY_BLUE};
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .dash-card table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .dash-card th {{
            background-color: {MAROON} !important;
            color: {WHITE} !important;
            padding: 10px 15px;
            text-align: left;
        }}
        .dash-card td {{
            padding: 10px 15px;
            border-bottom: 1px solid {CARD_BORDER};
            color: {MAROON_TEXT} !important;
        }}
        .dash-card tr:nth-child(even) {{
            background-color: {CARD_ALT_ROW};
        }}
        
        .positive {{
            color: {GREEN} !important;
            font-weight: bold;
        }}
        .negative {{
            color: {RED} !important;
            font-weight: bold;
        }}
        
        .avatar-circle {{
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background-color: {MAROON};
            color: {WHITE};
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 36px;
            font-weight: bold;
            margin: 0 auto;
        }}
        
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        [data-testid="stFileUploadDropzone"] {{
            position: relative;
        }}
        [data-testid="stFileUploadDropzone"]::before {{
            content: "Click or drag image here";
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: {MAROON};
            font-family: 'Georgia', serif;
            z-index: 1;
        }}
        [data-testid="stFileUploadDropzone"] small {{
            display: none !important;
        }}
        
        .lifetime-badge {{
            display: inline-block;
            background-color: {MAROON};
            color: {WHITE} !important;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            margin-left: 8px;
        }}
        .term-badge {{
            display: inline-block;
            background-color: {SKY_BLUE};
            color: {WHITE} !important;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            margin-left: 8px;
        }}
        
        hr, .section-divider {{
            border: none;
            border-top: 2px solid {MAROON};
            margin: 30px 0;
        }}
        
        /* ============================================= */
        /* MULTISELECT */
        /* ============================================= */
        .stMultiSelect label {{
            color: {MAROON_TEXT} !important;
        }}
        .stMultiSelect div[data-baseweb="select"] > div {{
            color: {MAROON_TEXT} !important;
        }}
        
        /* ============================================= */
        /* DATE INPUT */
        /* ============================================= */
        .stDateInput label {{
            color: {MAROON_TEXT} !important;
        }}
        .stDateInput input {{
            color: {MAROON_TEXT} !important;
        }}
    </style>
    """, unsafe_allow_html=True)

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
def init_session():
    defaults = {
        'logged_in': False,
        'user_type': None,
        'student_name': None,
        'username': None,
        'student_class': None,
        'current_page': "My Dashboard",
        'admin_page': "Overview",
        'overview_term_filter': "All Time",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# ============================================================
# GOOGLE SHEETS CONNECTION
# ============================================================
@st.cache_resource
def connect_to_sheets():
    """Connect to Google Sheets using Streamlit secrets or local credentials."""
    try:
        creds_dict = dict(st.secrets["connections"]["gsheet"])
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            creds_dict,
            scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        )
    except Exception:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            "credentials.json",
            scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        )
    
    client = gspread.authorize(credentials)
    return client

def load_data(sheet_name):
    """Load data from a specific worksheet with retry logic and column stripping."""
    client = connect_to_sheets()
    for attempt in range(3):
        try:
            sheet = client.open(SHEET_NAME).worksheet(sheet_name)
            df = pd.DataFrame(sheet.get_all_records())
            df.columns = df.columns.astype(str).str.strip()
            return df
        except Exception as e:
            if attempt < 2:
                connect_to_sheets.clear()
                client = connect_to_sheets()
                time.sleep(1)
            else:
                st.error(f"Failed to load '{sheet_name}': {e}")
                return pd.DataFrame()

def write_data(sheet_name, data):
    """Append a row to a worksheet."""
    client = connect_to_sheets()
    for attempt in range(3):
        try:
            sheet = client.open(SHEET_NAME).worksheet(sheet_name)
            sheet.append_row(data)
            return True
        except Exception as e:
            if attempt < 2:
                connect_to_sheets.clear()
                client = connect_to_sheets()
                time.sleep(1)
            else:
                st.error(f"Failed to write to '{sheet_name}': {e}")
                return False

def update_cell(sheet_name, row, col, value):
    """Update a specific cell."""
    client = connect_to_sheets()
    try:
        sheet = client.open(SHEET_NAME).worksheet(sheet_name)
        sheet.update_cell(row, col, value)
        return True
    except Exception as e:
        st.error(f"Failed to update cell: {e}")
        return False

# ============================================================
# IMAGE HELPERS
# ============================================================
def image_to_base64(image_file, max_size=300, quality=60):
    """Convert uploaded image to compressed Base64 string."""
    try:
        img = Image.open(image_file)
        img = img.convert("RGB")
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
            img = img.resize(new_size, Image.LANCZOS)
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=quality)
        b64_str = base64.b64encode(buffer.getvalue()).decode()
        if len(b64_str) > 45000:
            st.warning("Image may be too large. Try a smaller photo (under 300px).")
        return b64_str
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None

def get_initials(name):
    """Get initials from a name."""
    parts = name.strip().split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    elif len(parts) == 1:
        return parts[0][0].upper()
    return "ZA"

# ============================================================
# LOGIN PAGE
# ============================================================
def login_page():
    st.markdown(f"""
    <div class="top-banner">
        <img src="{SCHOOL_LOGO_URL}" alt="Zebra Academy Logo">
        <h1>{SCHOOL_NAME} Portal</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Student Login", "Admin Login"])
        
        with tab1:
            st.markdown("### Student Login")
            username = st.text_input("Username", key="student_user")
            password = st.text_input("Password", type="password", key="student_pass")
            
            if st.button("Login", key="student_login_btn", use_container_width=True):
                df_logins = load_data("Student Logins")
                if not df_logins.empty:
                    df_logins.columns = df_logins.columns.astype(str).str.strip()
                    match = df_logins[
                        (df_logins["Username"].astype(str).str.strip() == username.strip()) &
                        (df_logins["Password"].astype(str).str.strip() == password.strip())
                    ]
                    if not match.empty:
                        student = match.iloc[0]
                        st.session_state.logged_in = True
                        st.session_state.user_type = "student"
                        st.session_state.username = username.strip()
                        st.session_state.student_name = str(student["Student Name"]).strip()
                        st.session_state.student_class = str(student["Class"]).strip()
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
                else:
                    st.error("Unable to load login data.")
        
        with tab2:
            st.markdown("### Admin Login")
            admin_pass = st.text_input("Admin Password", type="password", key="admin_pass")
            
            if st.button("Login", key="admin_login_btn", use_container_width=True):
                if admin_pass == "admin2026":
                    st.session_state.logged_in = True
                    st.session_state.user_type = "admin"
                    st.session_state.username = "admin"
                    st.session_state.student_name = "Administrator"
                    st.rerun()
                else:
                    st.error("Invalid admin password.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="bottom-footer">
        &copy; {datetime.now().year} {SCHOOL_NAME}. All rights reserved.
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# STUDENT DASHBOARD
# ============================================================
def student_dashboard():
    student_name = st.session_state.student_name
    student_class = st.session_state.student_class
    
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0;">
            <img src="{SCHOOL_LOGO_URL}" style="width: 80px; border-radius: 8px; margin-bottom: 10px;">
            <h3 style="color: white; margin: 0;">{SCHOOL_NAME}</h3>
            <p style="color: #E0D5D8; margin: 5px 0;">Student Portal</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        df_profiles = load_data("Student Profiles")
        photo_b64 = None
        if not df_profiles.empty:
            df_profiles.columns = df_profiles.columns.astype(str).str.strip()
            profile = df_profiles[df_profiles["Username"].astype(str).str.strip() == st.session_state.username.strip()]
            if not profile.empty:
                photo_b64 = profile.iloc[0].get("Profile Photo", "")
                if pd.notna(photo_b64) and str(photo_b64).strip():
                    photo_b64 = str(photo_b64).strip()
        
        if photo_b64 and len(photo_b64) > 10:
            st.markdown(f"""
            <div style="text-align: center;">
                <img src="data:image/jpeg;base64,{photo_b64}" 
                     style="width: 100px; height: 100px; border-radius: 50%; object-fit: cover; border: 3px solid {WHITE};">
            </div>
            """, unsafe_allow_html=True)
        else:
            initials = get_initials(student_name)
            st.markdown(f"""
            <div style="text-align: center;">
                <div class="avatar-circle">{initials}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <p style="text-align: center; color: {WHITE}; font-size: 16px; margin-top: 10px;"><strong>{student_name}</strong></p>
        <p style="text-align: center; color: #E0D5D8; font-size: 13px;">{student_class}</p>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        pages = ["My Dashboard", "My Performance", "My Fees", "My Attendance", "Profile Settings"]
        for page in pages:
            if st.button(page, key=f"nav_{page}", use_container_width=True):
                st.session_state.current_page = page
                st.rerun()
        
        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    page = st.session_state.current_page
    
    if page == "My Dashboard":
        student_dashboard_home(student_name, student_class)
    elif page == "My Performance":
        student_performance(student_name, student_class)
    elif page == "My Fees":
        student_fees(student_name, student_class)
    elif page == "My Attendance":
        student_attendance(student_name, student_class)
    elif page == "Profile Settings":
        student_profile_settings()

def student_dashboard_home(student_name, student_class):
    st.markdown(f"## Welcome, {student_name}!")
    st.markdown(f"**Class:** {student_class}")
    
    df_students = load_data("Students")
    student_info = pd.DataFrame()
    if not df_students.empty:
        df_students.columns = df_students.columns.astype(str).str.strip()
        student_info = df_students[df_students["Student Name"].astype(str).str.strip() == student_name.strip()]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="dash-card"><div class="dash-card-header">My Details</div><div class="dash-card-body">', unsafe_allow_html=True)
        if not student_info.empty:
            s = student_info.iloc[0]
            details = [
                ("Student Number", s.get("Student Number", "N/A")),
                ("Date of Birth", s.get("Date of Birth", "N/A")),
                ("Gender", s.get("Gender", "N/A")),
                ("Address", s.get("Address", "N/A")),
                ("Guardian", s.get("Guardian Name", "N/A")),
                ("Guardian Phone", s.get("Guardian Phone", "N/A")),
                ("Enrollment Date", s.get("Enrollment Date", "N/A")),
            ]
            for label, value in details:
                st.markdown(f"**{label}:** {value}")
        else:
            st.info("No details found.")
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="dash-card"><div class="dash-card-header">Fee Status</div><div class="dash-card-body">', unsafe_allow_html=True)
        df_fee_status = load_data("Fee Status")
        if not df_fee_status.empty:
            df_fee_status.columns = df_fee_status.columns.astype(str).str.strip()
            fee_row = df_fee_status[df_fee_status["Student Name"].astype(str).str.strip() == student_name.strip()]
            if not fee_row.empty:
                for col in fee_row.columns:
                    if col != "Student Name":
                        val = fee_row.iloc[0][col]
                        st.markdown(f"**{col}:** {val}")
            else:
                st.info("No fee data available.")
        else:
            st.info("No fee data available.")
        st.markdown('</div></div>', unsafe_allow_html=True)

def student_performance(student_name, student_class):
    st.markdown("## My Performance")
    
    df_perf = load_data("Performance")
    if df_perf.empty:
        st.info("No performance records found.")
        return
    
    df_perf.columns = df_perf.columns.astype(str).str.strip()
    df_perf["Student Name"] = df_perf["Student Name"].astype(str).str.strip()
    my_perf = df_perf[df_perf["Student Name"] == student_name.strip()]
    
    if my_perf.empty:
        st.info("No results found for you yet.")
        return
    
    terms = my_perf["Term"].unique()
    for term in sorted(terms, reverse=True):
        term_data = my_perf[my_perf["Term"] == term]
        st.markdown(f"### {term}")
        
        display_cols = ["Subject", "Mark", "Grade", "Comment"]
        display_data = term_data[[c for c in display_cols if c in term_data.columns]]
        
        st.markdown('<div class="dash-card"><div class="dash-card-body">', unsafe_allow_html=True)
        st.dataframe(display_data, use_container_width=True, hide_index=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

def student_fees(student_name, student_class):
    st.markdown("## My Fees")
    
    df_payments = load_data("Fee Payments")
    df_fee_status = load_data("Fee Status")
    
    if not df_fee_status.empty:
        df_fee_status.columns = df_fee_status.columns.astype(str).str.strip()
        fee_row = df_fee_status[df_fee_status["Student Name"].astype(str).str.strip() == student_name.strip()]
        
        st.markdown('<div class="dash-card"><div class="dash-card-header">Fee Summary</div><div class="dash-card-body">', unsafe_allow_html=True)
        if not fee_row.empty:
            for col in fee_row.columns:
                if col != "Student Name":
                    val = fee_row.iloc[0][col]
                    st.markdown(f"**{col}:** {val}")
        else:
            st.info("No fee summary available.")
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    if not df_payments.empty:
        df_payments.columns = df_payments.columns.astype(str).str.strip()
        my_payments = df_payments[df_payments["Student Name"].astype(str).str.strip() == student_name.strip()]
        
        st.markdown('<div class="dash-card"><div class="dash-card-header">Payment History</div><div class="dash-card-body">', unsafe_allow_html=True)
        if not my_payments.empty:
            st.dataframe(my_payments, use_container_width=True, hide_index=True)
        else:
            st.info("No payments recorded yet.")
        st.markdown('</div></div>', unsafe_allow_html=True)

def student_attendance(student_name, student_class):
    st.markdown("## My Attendance")
    
    df_att = load_data("Attendance View")
    if df_att.empty:
        st.info("No attendance records found.")
        return
    
    df_att.columns = df_att.columns.astype(str).str.strip()
    my_att = df_att[df_att["Student Name"].astype(str).str.strip() == student_name.strip()]
    
    st.markdown('<div class="dash-card"><div class="dash-card-header">Last 5 Working Days</div><div class="dash-card-body">', unsafe_allow_html=True)
    if not my_att.empty:
        def style_attendance(val):
            if val == "Present":
                return f'<span style="color: {GREEN}; font-weight: bold;">Present</span>'
            elif val == "Absent":
                return f'<span style="color: {RED}; font-weight: bold;">Absent</span>'
            return val
        
        row = my_att.iloc[0]
        html = '<table style="width:100%; border-collapse:collapse;">'
        html += '<tr style="background-color:' + MAROON + '; color:' + WHITE + ';">'
        for col in my_att.columns:
            html += f'<th style="padding:12px;">{col}</th>'
        html += '</tr><tr>'
        for col in my_att.columns:
            val = row[col]
            html += f'<td style="padding:12px; text-align:center;">{style_attendance(str(val))}</td>'
        html += '</tr></table>'
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.info("No attendance data for you.")
    st.markdown('</div></div>', unsafe_allow_html=True)

def student_profile_settings():
    st.markdown("## Profile Settings")
    
    st.markdown('<div class="dash-card"><div class="dash-card-header">Update Profile Photo</div><div class="dash-card-body">', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose a profile photo", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        st.image(uploaded_file, width=150, caption="Preview")
        
        if st.button("Save Photo", use_container_width=True):
            b64_str = image_to_base64(uploaded_file)
            if b64_str:
                df_profiles = load_data("Student Profiles")
                if not df_profiles.empty:
                    df_profiles.columns = df_profiles.columns.astype(str).str.strip()
                    existing = df_profiles[df_profiles["Username"].astype(str).str.strip() == st.session_state.username.strip()]
                    if not existing.empty:
                        row_idx = existing.index[0] + 2
                        update_cell("Student Profiles", row_idx, 3, b64_str)
                    else:
                        write_data("Student Profiles", [
                            st.session_state.username,
                            st.session_state.student_name,
                            b64_str
                        ])
                    st.success("Profile photo updated! Refresh to see changes.")
                    st.rerun()
    
    st.markdown('</div></div>', unsafe_allow_html=True)

# ============================================================
# ADMIN DASHBOARD - HELPERS
# ============================================================
def get_available_terms():
    """Get unique terms from all financial and performance sheets."""
    terms = set()
    for sheet_name in ["Fee Payments", "Expenses", "Other Income", "Performance"]:
        df = load_data(sheet_name)
        if not df.empty and "Term" in df.columns:
            df.columns = df.columns.astype(str).str.strip()
            for t in df["Term"].dropna().unique():
                terms.add(str(t).strip())
    return sorted(list(terms), reverse=True)

def filter_by_term(df, term):
    """Filter dataframe by term if term column exists."""
    if df.empty or term == "All Time" or "Term" not in df.columns:
        return df
    df.columns = df.columns.astype(str).str.strip()
    return df[df["Term"].astype(str).str.strip() == term.strip()]

def safe_sum(df, column_name):
    """Safely sum a numeric column."""
    if df.empty or column_name not in df.columns:
        return 0.0
    return pd.to_numeric(df[column_name], errors='coerce').sum()

# ============================================================
# AUTO-GRADING SYSTEM
# ============================================================
def calculate_grade(mark):
    """Auto-calculate grade based on mark percentage."""
    if mark >= 75:
        return "A"
    elif mark >= 60:
        return "B"
    elif mark >= 50:
        return "C"
    elif mark >= 45:
        return "D"
    elif mark >= 40:
        return "E"
    else:
        return "F"

def grade_color(grade):
    """Return color for grade display."""
    colors = {
        "A": GREEN,
        "B": "#8BC34A",
        "C": "#FFC107",
        "D": "#FF9800",
        "E": "#FF5722",
        "F": RED,
    }
    return colors.get(grade, MAROON_TEXT)

# ============================================================
# ADMIN DASHBOARD - MAIN
# ============================================================
def admin_dashboard():
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0;">
            <img src="{SCHOOL_LOGO_URL}" style="width: 80px; border-radius: 8px; margin-bottom: 10px;">
            <h3 style="color: white; margin: 0;">{SCHOOL_NAME}</h3>
            <p style="color: #E0D5D8; margin: 5px 0;">Admin Portal</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        admin_pages = [
            "Overview",
            "Register Student",
            "Record Fee Payment",
            "Enter Performance",
            "Student Grades",
            "Mark Attendance",
            "Record Expense",
            "Record Other Income",
            "Salary Payments",
            "All Students",
        ]
        
        for page in admin_pages:
            if st.button(page, key=f"admin_{page}", use_container_width=True):
                st.session_state.admin_page = page
                st.rerun()
        
        st.markdown("---")
        if st.button("Logout", key="admin_logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    page = st.session_state.admin_page
    
    if page == "Overview":
        admin_overview()
    elif page == "Register Student":
        admin_register_student()
    elif page == "Record Fee Payment":
        admin_record_fee()
    elif page == "Enter Performance":
        admin_enter_performance()
    elif page == "Student Grades":
        admin_student_grades()
    elif page == "Mark Attendance":
        admin_mark_attendance()
    elif page == "Record Expense":
        admin_record_expense()
    elif page == "Record Other Income":
        admin_record_other_income()
    elif page == "Salary Payments":
        admin_salary_payments()
    elif page == "All Students":
        admin_all_students()

# ============================================================
# ADMIN OVERVIEW
# ============================================================
def admin_overview():
    st.markdown("## Admin Overview")
    
    available_terms = get_available_terms()
    term_options = ["All Time"] + available_terms
    
    col_filter, col_space = st.columns([1, 3])
    with col_filter:
        selected_term = st.selectbox(
            "Filter Financials by Term",
            term_options,
            key="overview_term_filter"
        )
    
    df_students = load_data("Students")
    df_payments_all = load_data("Fee Payments")
    df_expenses_all = load_data("Expenses")
    df_other_income_all = load_data("Other Income")
    
    total_students = len(df_students) if not df_students.empty else 0
    all_time_fees = safe_sum(df_payments_all, "Amount Paid")
    all_time_other = safe_sum(df_other_income_all, "Amount")
    all_time_expenses = safe_sum(df_expenses_all, "Amount")
    all_time_income = all_time_fees + all_time_other
    all_time_profit = all_time_income - all_time_expenses
    
    df_payments_term = filter_by_term(df_payments_all.copy(), selected_term)
    df_expenses_term = filter_by_term(df_expenses_all.copy(), selected_term)
    df_other_income_term = filter_by_term(df_other_income_all.copy(), selected_term)
    
    term_fees = safe_sum(df_payments_term, "Amount Paid")
    term_other = safe_sum(df_other_income_term, "Amount")
    term_expenses = safe_sum(df_expenses_term, "Amount")
    term_income = term_fees + term_other
    term_profit = term_income - term_expenses
    
    investments = term_profit * 0.10
    salaries_pool = term_profit * 0.20
    tithe = term_profit * 0.10
    alter = term_profit * 0.05
    operations = term_profit * 0.10
    net_profit = term_profit * 0.45
    per_person = salaries_pool / 4
    
    class_count = "N/A"
    if not df_students.empty:
        df_students.columns = df_students.columns.astype(str).str.strip()
        if "Class" in df_students.columns:
            class_count = str(df_students["Class"].nunique())
    
    # ============================================================
    # SECTION 1: ENROLLMENT (ALWAYS ALL-TIME)
    # ============================================================
    st.markdown('<div class="dash-card"><div class="dash-card-header">Enrollment<span class="lifetime-badge">ALL TIME</span></div><div class="dash-card-body">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_students}</div>
            <div class="metric-label">Total Students Enrolled</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{class_count}</div>
            <div class="metric-label">Classes</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${all_time_income:,.0f}</div>
            <div class="metric-label">Lifetime Income</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${all_time_expenses:,.0f}</div>
            <div class="metric-label">Lifetime Expenses</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # ============================================================
    # SECTION 2: FINANCIALS (TERM-FILTERED)
    # ============================================================
    badge_html = '<span class="term-badge">ALL TIME</span>' if selected_term == "All Time" else f'<span class="term-badge">{selected_term}</span>'
    st.markdown(f'<div class="dash-card"><div class="dash-card-header">Financials{badge_html}</div><div class="dash-card-body">', unsafe_allow_html=True)
    
    st.markdown("#### Income")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${term_fees:,.0f}</div>
            <div class="metric-label">Fees Income</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${term_other:,.0f}</div>
            <div class="metric-label">Other Income</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {MAROON};">${term_income:,.0f}</div>
            <div class="metric-label">Total Income</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("#### Expenses")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {RED};">${term_expenses:,.0f}</div>
            <div class="metric-label">Total Expenses</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("#### Profit")
    profit_color = GREEN if term_profit >= 0 else RED
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${term_income:,.0f}</div>
            <div class="metric-label">Total Income</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {RED};">${term_expenses:,.0f}</div>
            <div class="metric-label">Total Expenses</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {profit_color};">${term_profit:,.0f}</div>
            <div class="metric-label">Gross Profit</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # ============================================================
    # SECTION 3: PROFIT DISTRIBUTION (TERM-FILTERED)
    # ============================================================
    st.markdown(f'<div class="dash-card"><div class="dash-card-header">Profit Distribution{badge_html}</div><div class="dash-card-body">', unsafe_allow_html=True)
    
    st.markdown(f"**Gross Profit to Distribute:** ${term_profit:,.0f}")
    st.markdown("---")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${investments:,.0f}</div>
            <div class="metric-label">Investments</div>
            <div class="metric-label">10%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${salaries_pool:,.0f}</div>
            <div class="metric-label">Salaries</div>
            <div class="metric-label">20%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${tithe:,.0f}</div>
            <div class="metric-label">Tithe</div>
            <div class="metric-label">10%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${alter:,.0f}</div>
            <div class="metric-label">Alter</div>
            <div class="metric-label">5%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${operations:,.0f}</div>
            <div class="metric-label">Operations</div>
            <div class="metric-label">10%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown(f"""
        <div class="metric-card" style="border: 2px solid {GREEN};">
            <div class="metric-value" style="color: {GREEN};">${net_profit:,.0f}</div>
            <div class="metric-label">Retained Profit</div>
            <div class="metric-label">45%</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### Salary Split (20% divided equally among 4 people = 5% each)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${per_person:,.0f}</div>
            <div class="metric-label">Mr Kawonde</div>
            <div class="metric-label">5%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${per_person:,.0f}</div>
            <div class="metric-label">Mrs Kawonde</div>
            <div class="metric-label">5%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${per_person:,.0f}</div>
            <div class="metric-label">Nextvantage Analytics</div>
            <div class="metric-label">5%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${per_person:,.0f}</div>
            <div class="metric-label">Miss Mutasvu</div>
            <div class="metric-label">5%</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

# ============================================================
# STUDENT GRADES PAGE
# ============================================================
def admin_student_grades():
    st.markdown("## Student Grades")
    
    df_performance_all = load_data("Performance")
    
    available_terms = get_available_terms()
    term_options = ["All Time"] + available_terms
    
    col_filter, col_space = st.columns([1, 3])
    with col_filter:
        selected_term = st.selectbox(
            "Filter by Term",
            term_options,
            key="grades_term_filter"
        )
    
    df_perf = filter_by_term(df_performance_all.copy(), selected_term)
    
    badge_html = '<span class="term-badge">ALL TIME</span>' if selected_term == "All Time" else f'<span class="term-badge">{selected_term}</span>'
    st.markdown(f'<div class="dash-card"><div class="dash-card-header">Grade Records{badge_html}</div><div class="dash-card-body">', unsafe_allow_html=True)
    
    if not df_perf.empty:
        df_perf.columns = df_perf.columns.astype(str).str.strip()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            all_students = ["All"] + sorted(df_perf["Student Name"].dropna().unique().tolist()) if "Student Name" in df_perf.columns else ["All"]
            filter_student = st.selectbox("Student", all_students, key="grades_student")
        with col2:
            all_classes = ["All"] + sorted(df_perf["Class"].dropna().unique().tolist()) if "Class" in df_perf.columns else ["All"]
            filter_class = st.selectbox("Class", all_classes, key="grades_class")
        with col3:
            all_subjects = ["All"] + sorted(df_perf["Subject"].dropna().unique().tolist()) if "Subject" in df_perf.columns else ["All"]
            filter_subject = st.selectbox("Subject", all_subjects, key="grades_subject")
        with col4:
            all_grade_vals = ["All"] + sorted(df_perf["Grade"].dropna().unique().tolist()) if "Grade" in df_perf.columns else ["All"]
            filter_grade = st.selectbox("Grade", all_grade_vals, key="grades_grade")
        
        filtered = df_perf.copy()
        if filter_student != "All" and "Student Name" in filtered.columns:
            filtered = filtered[filtered["Student Name"].astype(str).str.strip() == filter_student.strip()]
        if filter_class != "All" and "Class" in filtered.columns:
            filtered = filtered[filtered["Class"].astype(str).str.strip() == filter_class.strip()]
        if filter_subject != "All" and "Subject" in filtered.columns:
            filtered = filtered[filtered["Subject"].astype(str).str.strip() == filter_subject.strip()]
        if filter_grade != "All" and "Grade" in filtered.columns:
            filtered = filtered[filtered["Grade"].astype(str).str.strip() == filter_grade.strip()]
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Records", len(filtered))
        with col2:
            avg_mark = filtered["Mark"].astype(float).mean() if "Mark" in filtered.columns and not filtered.empty else 0
            st.metric("Average Mark", f"{avg_mark:.1f}%")
        with col3:
            a_count = len(filtered[filtered["Grade"].astype(str).str.strip() == "A"]) if "Grade" in filtered.columns else 0
            st.metric("A Grades", a_count)
        with col4:
            pass_count = len(filtered[filtered["Grade"].astype(str).str.strip().isin(["A", "B", "C"])]) if "Grade" in filtered.columns else 0
            st.metric("Passes (A-C)", pass_count)
        with col5:
            fail_count = len(filtered[filtered["Grade"].astype(str).str.strip().isin(["E", "F"])]) if "Grade" in filtered.columns else 0
            st.metric("Fails (E-F)", fail_count)
        
        st.markdown("---")
        st.markdown(f"**Showing {len(filtered)} record(s)**")
        
        if not filtered.empty:
            html = '<table style="width:100%; border-collapse:collapse; font-size:14px;">'
            html += f'<tr style="background-color:{MAROON}; color:{WHITE};">'
            for col in filtered.columns:
                html += f'<th style="padding:10px 12px; text-align:left;">{col}</th>'
            html += '</tr>'
            
            for idx, row in filtered.iterrows():
                bg = CARD_ALT_ROW if idx % 2 == 0 else WHITE
                html += f'<tr style="background-color:{bg};">'
                for col in filtered.columns:
                    val = row[col]
                    if col == "Grade":
                        gc = grade_color(str(val).strip())
                        html += f'<td style="padding:10px 12px; font-weight:bold; color:{gc};">{val}</td>'
                    elif col == "Mark":
                        html += f'<td style="padding:10px 12px;">{val}%</td>'
                    else:
                        html += f'<td style="padding:10px 12px; color:{MAROON_TEXT};">{val}</td>'
                html += '</tr>'
            html += '</table>'
            st.markdown(html, unsafe_allow_html=True)
    else:
        st.info("No grade records found.")
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="dash-card"><div class="dash-card-header">Grading Scale</div><div class="dash-card-body">', unsafe_allow_html=True)
    
    scale_data = [
        ("A", "75% and above", GREEN, "Excellent"),
        ("B", "60% - 74%", "#8BC34A", "Good"),
        ("C", "50% - 59%", "#FFC107", "Satisfactory"),
        ("D", "45% - 49%", "#FF9800", "Needs Improvement"),
        ("E", "40% - 44%", "#FF5722", "At Risk"),
        ("F", "Below 40%", RED, "Fail"),
    ]
    
    html = '<table style="width:100%; border-collapse:collapse;">'
    html += f'<tr style="background-color:{MAROON}; color:{WHITE};"><th style="padding:10px;">Grade</th><th style="padding:10px;">Mark Range</th><th style="padding:10px;">Description</th></tr>'
    for grade, mark_range, color, desc in scale_data:
        html += f'<tr><td style="padding:10px; font-weight:bold; font-size:18px; color:{color};">{grade}</td><td style="padding:10px; color:{MAROON_TEXT};">{mark_range}</td><td style="padding:10px; color:{MAROON_TEXT};">{desc}</td></tr>'
    html += '</table>'
    st.markdown(html, unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

# ============================================================
# ADMIN DATA ENTRY PAGES
# ============================================================
def admin_register_student():
    st.markdown("## Register New Student")
    
    st.markdown('<div class="dash-card"><div class="dash-card-header">Student Information</div><div class="dash-card-body">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        student_name = st.text_input("Student Full Name*")
        dob = st.date_input("Date of Birth*", min_value=date(2000,1,1), max_value=date.today())
        gender = st.selectbox("Gender*", ["Male", "Female", "Other"])
        student_class = st.text_input("Class*", placeholder="e.g., Grade 1, Form 2")
    
    with col2:
        address = st.text_area("Address")
        guardian_name = st.text_input("Guardian Name*")
        guardian_phone = st.text_input("Guardian Phone*")
        enrollment_date = st.date_input("Enrollment Date*", value=date.today())
    
    st.markdown("---")
    st.markdown("### Login Credentials")
    username = st.text_input("Username*", placeholder="Auto-generated if left blank")
    password = st.text_input("Password*", type="password")
    
    if st.button("Register Student", use_container_width=True):
        if not student_name or not student_class or not guardian_name:
            st.error("Please fill in all required fields (*)")
        else:
            student_number = f"ZA-{datetime.now().year}-{random.randint(1000,9999)}"
            
            if not username:
                username = student_name.lower().replace(" ", ".") + str(random.randint(10,99))
            
            if not password:
                password = "student123"
            
            success1 = write_data("Students", [
                student_name, student_class, str(dob), gender,
                address, guardian_name, guardian_phone,
                student_number, str(enrollment_date)
            ])
            
            success2 = write_data("Student Logins", [
                student_name, username, password, student_class, "Active"
            ])
            
            if success1 and success2:
                st.success(f"Student registered successfully!\n\nUsername: {username}\nPassword: {password}\nStudent Number: {student_number}")
                st.balloons()
            else:
                st.error("There was an error saving to the database.")
    
    st.markdown('</div></div>', unsafe_allow_html=True)

def admin_record_fee():
    st.markdown("## Record Fee Payment")
    
    st.markdown('<div class="dash-card"><div class="dash-card-header">Payment Details</div><div class="dash-card-body">', unsafe_allow_html=True)
    
    df_students = load_data("Students")
    student_list = ["Select student..."]
    if not df_students.empty:
        df_students.columns = df_students.columns.astype(str).str.strip()
        student_list += df_students["Student Name"].tolist()
    
    col1, col2 = st.columns(2)
    
    with col1:
        student_name = st.selectbox("Student Name*", student_list)
        amount = st.number_input("Amount Paid*", min_value=0.0, step=10.0)
        payment_method = st.selectbox("Payment Method", ["Cash", "EFT", "Mobile Money", "Cheque", "Other"])
    
    with col2:
        payment_date = st.date_input("Payment Date", value=date.today())
        term = st.selectbox("Term", [
            "Term 1 2026", "Term 2 2026", "Term 3 2026",
            "Term 1 2027", "Term 2 2027", "Term 3 2027"
        ])
        term_month = st.text_input("Term Month", placeholder="e.g., Term 1 January 2026")
    
    student_class = ""
    if student_name != "Select student..." and not df_students.empty:
        match = df_students[df_students["Student Name"].astype(str).str.strip() == student_name.strip()]
        if not match.empty:
            student_class = str(match.iloc[0]["Class"])
    
    if st.button("Record Payment", use_container_width=True):
        if student_name == "Select student...":
            st.error("Please select a student.")
        elif amount <= 0:
            st.error("Please enter an amount.")
        else:
            success = write_data("Fee Payments", [
                str(payment_date), student_name, student_class,
                amount, payment_method, term, term_month
            ])
            if success:
                st.success(f"Payment of ${amount:,.2f} recorded for {student_name}!")
            else:
                st.error("Failed to record payment.")
    
    st.markdown('</div></div>', unsafe_allow_html=True)

def admin_enter_performance():
    st.markdown("## Enter Student Performance")
    
    st.markdown('<div class="dash-card"><div class="dash-card-header">Performance Entry</div><div class="dash-card-body">', unsafe_allow_html=True)
    
    df_students = load_data("Students")
    student_list = ["Select student..."]
    if not df_students.empty:
        df_students.columns = df_students.columns.astype(str).str.strip()
        student_list += df_students["Student Name"].tolist()
    
    col1, col2 = st.columns(2)
    
    with col1:
        student_name = st.selectbox("Student Name*", student_list)
        term = st.selectbox("Term*", [
            "Term 1 2026", "Term 2 2026", "Term 3 2026",
            "Term 1 2027", "Term 2 2027", "Term 3 2027"
        ])
        subject = st.text_input("Subject*", placeholder="e.g., Mathematics")
    
    with col2:
        mark = st.number_input("Mark (%)*", min_value=0, max_value=100, step=1)
        auto_grade = calculate_grade(mark)
        grade_color_display = grade_color(auto_grade)
        st.markdown(f"""
        <div style="margin-top: 10px; padding: 12px; background-color: {OFF_WHITE}; border-radius: 8px; border: 1px solid {CARD_BORDER};">
            <span style="color: {MAROON_TEXT}; font-size: 14px;">Auto-Calculated Grade: </span>
            <span style="color: {grade_color_display}; font-size: 24px; font-weight: bold;">{auto_grade}</span>
        </div>
        """, unsafe_allow_html=True)
        comment = st.text_area("Comment", placeholder="Teacher's comment...")
    
    student_class = ""
    if student_name != "Select student..." and not df_students.empty:
        match = df_students[df_students["Student Name"].astype(str).str.strip() == student_name.strip()]
        if not match.empty:
            student_class = str(match.iloc[0]["Class"])
    
    if st.button("Save Result", use_container_width=True):
        if student_name == "Select student...":
            st.error("Please select a student.")
        elif not subject:
            st.error("Please enter a subject.")
        else:
            success = write_data("Performance", [
                student_name, student_class, term, subject, mark, auto_grade, comment
            ])
            if success:
                st.success(f"Result saved for {student_name} - {subject}: {mark}% ({auto_grade})")
            else:
                st.error("Failed to save result.")
    
    st.markdown('</div></div>', unsafe_allow_html=True)

def admin_mark_attendance():
    st.markdown("## Mark Attendance")
    
    tab1, tab2 = st.tabs(["Attendance View (5-Day Grid)", "Record Absences"])
    
    with tab1:
        st.markdown('<div class="dash-card"><div class="dash-card-header">Update Attendance Grid</div><div class="dash-card-body">', unsafe_allow_html=True)
        
        df_students = load_data("Students")
        if not df_students.empty:
            df_students.columns = df_students.columns.astype(str).str.strip()
            
            df_att = load_data("Attendance View")
            
            st.markdown("**Select student and date to update:**")
            student_name = st.selectbox("Student", df_students["Student Name"].tolist(), key="att_student")
            
            date_cols = []
            if not df_att.empty:
                df_att.columns = df_att.columns.astype(str).str.strip()
                date_cols = [c for c in df_att.columns if c != "Student Name"]
            
            if date_cols:
                selected_date = st.selectbox("Date", date_cols, key="att_date")
                status = st.radio("Status", ["Present", "Absent"], horizontal=True)
                
                if st.button("Update Attendance"):
                    if not df_att.empty:
                        row_match = df_att[df_att["Student Name"].astype(str).str.strip() == student_name.strip()]
                        if not row_match.empty:
                            row_idx = row_match.index[0] + 2
                            col_idx = date_cols.index(selected_date) + 2
                            update_cell("Attendance View", row_idx, col_idx, status)
                            st.success(f"Updated {student_name} - {selected_date}: {status}")
                            st.rerun()
            else:
                st.info("No date columns found in Attendance View.")
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="dash-card"><div class="dash-card-header">Record Absent Students</div><div class="dash-card-body">', unsafe_allow_html=True)
        
        st.info("Use this to record which students were absent on a specific date (comma-separated).")
        
        absence_date = st.date_input("Date", value=date.today(), key="absence_date")
        
        if not df_students.empty:
            absent_students = st.multiselect("Absent Students", df_students["Student Name"].tolist())
            absent_str = ", ".join(absent_students)
            
            if st.button("Record Absences"):
                if absent_students:
                    write_data("Attendance", [
                        str(datetime.now()), str(absence_date), absent_str
                    ])
                    st.success(f"Recorded {len(absent_students)} absent student(s) on {absence_date}")
                else:
                    st.warning("No students selected.")
        
        st.markdown('</div></div>', unsafe_allow_html=True)

def admin_record_expense():
    st.markdown("## Record Expense")
    
    st.markdown('<div class="dash-card"><div class="dash-card-header">Expense Details</div><div class="dash-card-body">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        expense_date = st.date_input("Date", value=date.today(), key="exp_date")
        term = st.selectbox("Term", [
            "Term 1 2026", "Term 2 2026", "Term 3 2026",
            "Term 1 2027", "Term 2 2027", "Term 3 2027"
        ], key="exp_term")
        category = st.selectbox("Category", [
            "Utilities", "Supplies", "Maintenance", "Food", "Transport",
            "Printing", "Events", "Salaries", "Other"
        ])
    
    with col2:
        term_month = st.text_input("Term Month", placeholder="e.g., Term 1 January 2026", key="exp_month")
        description = st.text_area("Description")
        amount = st.number_input("Amount*", min_value=0.0, step=10.0, key="exp_amount")
    
    if st.button("Record Expense", use_container_width=True):
        if amount <= 0:
            st.error("Please enter an amount.")
        else:
            success = write_data("Expenses", [
                str(expense_date), term, term_month, category, description, amount
            ])
            if success:
                st.success(f"Expense of ${amount:,.2f} recorded!")
            else:
                st.error("Failed to record expense.")
    
    st.markdown('</div></div>', unsafe_allow_html=True)

def admin_record_other_income():
    st.markdown("## Record Other Income")
    
    st.markdown('<div class="dash-card"><div class="dash-card-header">Income Details</div><div class="dash-card-body">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        income_date = st.date_input("Date", value=date.today(), key="inc_date")
        term = st.selectbox("Term", [
            "Term 1 2026", "Term 2 2026", "Term 3 2026",
            "Term 1 2027", "Term 2 2027", "Term 3 2027"
        ], key="inc_term")
    
    with col2:
        term_month = st.text_input("Term Month", placeholder="e.g., Term 1 January 2026", key="inc_month")
        description = st.text_area("Description", key="inc_desc")
        amount = st.number_input("Amount*", min_value=0.0, step=10.0, key="inc_amount")
    
    if st.button("Record Income", use_container_width=True):
        if amount <= 0:
            st.error("Please enter an amount.")
        else:
            success = write_data("Other Income", [
                str(income_date), term, term_month, description, amount
            ])
            if success:
                st.success(f"Income of ${amount:,.2f} recorded!")
            else:
                st.error("Failed to record income.")
    
    st.markdown('</div></div>', unsafe_allow_html=True)

def admin_salary_payments():
    st.markdown("## Salary Payments")
    
    st.markdown('<div class="dash-card"><div class="dash-card-header">Record Salary Payout</div><div class="dash-card-body">', unsafe_allow_html=True)
    
    salary_recipients = [
        "Mr Kawonde",
        "Mrs Kawonde",
        "Nextvantage Analytics",
        "Miss Mutasvu"
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        salary_date = st.date_input("Date", value=date.today(), key="sal_date")
        term = st.selectbox("Term", [
            "Term 1 2026", "Term 2 2026", "Term 3 2026",
            "Term 1 2027", "Term 2 2027", "Term 3 2027"
        ], key="sal_term")
        term_month = st.text_input("Term Month", placeholder="e.g., Term 1 January 2026", key="sal_month")
    
    with col2:
        recipient = st.selectbox("Recipient", salary_recipients)
        amount = st.number_input("Amount ($)*", min_value=0.0, step=50.0, key="sal_amount")
        st.text_input("Percentage", value="5%", disabled=True, key="sal_pct")
    
    if st.button("Record Salary Payment", use_container_width=True):
        if amount <= 0:
            st.error("Please enter an amount.")
        else:
            success = write_data("Salaries", [
                str(salary_date), term, term_month, recipient, "5%", amount
            ])
            if success:
                st.success(f"Salary of ${amount:,.2f} paid to {recipient}!")
            else:
                st.error("Failed to record salary payment.")
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="dash-card"><div class="dash-card-header">Salary Summary</div><div class="dash-card-body">', unsafe_allow_html=True)
    df_salaries = load_data("Salaries")
    if not df_salaries.empty:
        df_salaries.columns = df_salaries.columns.astype(str).str.strip()
        st.dataframe(df_salaries, use_container_width=True, hide_index=True)
        
        st.markdown("#### Total per Recipient")
        for recipient in salary_recipients:
            rec_data = df_salaries[df_salaries["Recipient"].astype(str).str.strip() == recipient]
            total = safe_sum(rec_data, "Amount")
            st.markdown(f"**{recipient}:** ${total:,.2f}")
    else:
        st.info("No salary payments recorded.")
    st.markdown('</div></div>', unsafe_allow_html=True)

def admin_all_students():
    st.markdown("## All Students")
    
    df_students = load_data("Students")
    if not df_students.empty:
        df_students.columns = df_students.columns.astype(str).str.strip()
        
        search = st.text_input("Search by name...")
        if search:
            df_students = df_students[df_students["Student Name"].astype(str).str.contains(search, case=False)]
        
        st.dataframe(df_students, use_container_width=True, hide_index=True)
        st.markdown(f"**Total:** {len(df_students)} student(s)")
    else:
        st.info("No students registered yet.")

# ============================================================
# MAIN APP
# ============================================================
def main():
    inject_css()
    init_session()
    
    if not st.session_state.logged_in:
        login_page()
    elif st.session_state.user_type == "student":
        student_dashboard()
    elif st.session_state.user_type == "admin":
        admin_dashboard()

if __name__ == "__main__":
    main()
