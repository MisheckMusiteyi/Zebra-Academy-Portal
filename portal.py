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
import hashlib
import bcrypt

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Zebra Pace Academy Portal",
    page_icon="ZA",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# BRANDING
# ============================================================
SCHOOL_NAME = "Zebra Pace Academy"
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
FAINT_MAROON = "#F5F0F2"
HOVER_MAROON = "#EDE0E3"

# ============================================================
# CSS - ZEBRA ACADEMY MAROON THEME
# ============================================================
def inject_css():
    st.markdown(f"""
    <style>
        :root, [data-theme="light"], [data-theme="dark"] {{
            --background-color: {OFF_WHITE} !important;
            --secondary-background-color: {WHITE} !important;
            --text-color: {MAROON_TEXT} !important;
            --font: 'Georgia', 'Times New Roman', serif !important;
            --primary-color: {MAROON} !important;
            color-scheme: light !important;
        }}
        
        html {{
            color-scheme: light !important;
        }}
        
        html, body, [data-testid="stAppViewContainer"], .main, .block-container,
        [data-testid="stApp"], [data-testid="stHeader"], [data-testid="stToolbar"],
        [data-testid="stBottomBlockContainer"] {{
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
        
        section[data-testid="stSidebar"][aria-expanded="true"] {{
            background-color: {MAROON} !important;
            min-width: 300px !important;
            max-width: 300px !important;
            width: 300px !important;
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
        
        [data-testid*="ollapse" i] svg,
        [data-testid*="ollapse" i] span,
        [data-testid*="ollapse" i] p {{
            font-size: 0 !important;
            opacity: 0 !important;
            width: 0 !important;
            height: 0 !important;
        }}
        [data-testid*="ollapse" i] button {{
            background-color: {MAROON} !important;
            border: none !important;
            border-radius: 50% !important;
            width: 30px !important;
            height: 30px !important;
            min-width: 30px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 0 !important;
            color: transparent !important;
            line-height: 0 !important;
        }}
        [data-testid="collapsedControl"] button::after {{
            content: ">" !important;
            font-family: Arial, Helvetica, sans-serif !important;
            font-size: 16px !important;
            font-weight: bold !important;
            color: {WHITE} !important;
            line-height: 1 !important;
        }}
        [data-testid*="ollapse" i]:not([data-testid="collapsedControl"]) button::after {{
            content: "<" !important;
            font-family: Arial, Helvetica, sans-serif !important;
            font-size: 16px !important;
            font-weight: bold !important;
            color: {WHITE} !important;
            line-height: 1 !important;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            color: {MAROON} !important;
            font-family: 'Georgia', 'Times New Roman', serif !important;
        }}
        
        input, textarea, select {{
            color: {MAROON_TEXT} !important;
            background-color: {WHITE} !important;
            border: 1px solid {CARD_BORDER} !important;
        }}
        label, .stTextInput label, .stNumberInput label, .stSelectbox label, .stDateInput label {{
            color: {MAROON_TEXT} !important;
        }}
        
        [data-testid="stDataFrame"] table,
        .stDataFrame table,
        .dataframe table {{
            border-collapse: collapse !important;
            border: 1px solid {CARD_BORDER} !important;
        }}
        [data-testid="stDataFrame"] th,
        .stDataFrame th,
        .dataframe th {{
            background-color: {MAROON} !important;
            color: {WHITE} !important;
            padding: 12px 15px !important;
            font-weight: bold !important;
            border-bottom: 2px solid {MAROON_DARK} !important;
        }}
        [data-testid="stDataFrame"] td,
        .stDataFrame td,
        .dataframe td {{
            padding: 10px 15px !important;
            color: {MAROON_TEXT} !important;
            border-bottom: 1px solid {CARD_BORDER} !important;
        }}
        [data-testid="stDataFrame"] tr:nth-child(odd) td,
        .stDataFrame tr:nth-child(odd) td,
        .dataframe tr:nth-child(odd) td {{
            background-color: {WHITE} !important;
        }}
        [data-testid="stDataFrame"] tr:nth-child(even) td,
        .stDataFrame tr:nth-child(even) td,
        .dataframe tr:nth-child(even) td {{
            background-color: {FAINT_MAROON} !important;
        }}
        [data-testid="stDataFrame"] tr:hover td,
        .stDataFrame tr:hover td,
        .dataframe tr:hover td {{
            background-color: {HOVER_MAROON} !important;
        }}
        
        [data-testid="stTable"] table {{
            border-collapse: collapse !important;
            border: 1px solid {CARD_BORDER} !important;
        }}
        [data-testid="stTable"] th {{
            background-color: {MAROON} !important;
            color: {WHITE} !important;
            padding: 12px 15px !important;
            font-weight: bold !important;
        }}
        [data-testid="stTable"] td {{
            padding: 10px 15px !important;
            color: {MAROON_TEXT} !important;
            border-bottom: 1px solid {CARD_BORDER} !important;
        }}
        [data-testid="stTable"] tr:nth-child(odd) td {{
            background-color: {WHITE} !important;
        }}
        [data-testid="stTable"] tr:nth-child(even) td {{
            background-color: {FAINT_MAROON} !important;
        }}
        [data-testid="stTable"] tr:hover td {{
            background-color: {HOVER_MAROON} !important;
        }}
        
        [data-testid="stMetricValue"] {{
            color: {MAROON} !important;
        }}
        [data-testid="stMetricLabel"] {{
            color: {MAROON_TEXT} !important;
        }}
        
        .stAlert, [data-testid="stAlert"] {{
            color: {MAROON_TEXT} !important;
        }}
        .stAlert p, [data-testid="stAlert"] p {{
            color: {MAROON_TEXT} !important;
        }}
        
        .stSelectbox div[data-baseweb="select"] > div {{
            color: {MAROON_TEXT} !important;
            background-color: {WHITE} !important;
        }}
        
        .stRadio label, .stRadio p, .stRadio span {{
            color: {MAROON_TEXT} !important;
        }}
        
        .stCheckbox label, .stCheckbox p, .stCheckbox span {{
            color: {MAROON_TEXT} !important;
        }}
        
        .streamlit-expanderHeader {{
            color: {MAROON_TEXT} !important;
        }}
        
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
        
        .dash-card table {{
            width: 100%;
            border-collapse: collapse;
            border: 1px solid {CARD_BORDER};
        }}
        .dash-card th {{
            background-color: {MAROON} !important;
            color: {WHITE} !important;
            padding: 12px 15px;
            text-align: left;
            font-weight: bold;
            border-bottom: 2px solid {MAROON_DARK};
        }}
        .dash-card td {{
            padding: 10px 15px;
            border-bottom: 1px solid {CARD_BORDER};
            color: {MAROON_TEXT} !important;
        }}
        .dash-card tr:nth-child(odd) td {{
            background-color: {WHITE};
        }}
        .dash-card tr:nth-child(even) td {{
            background-color: {FAINT_MAROON};
        }}
        .dash-card tr:hover td {{
            background-color: {HOVER_MAROON} !important;
        }}
        
        .dash-card-body table {{
            width: 100%;
            border-collapse: collapse;
            border: 1px solid {CARD_BORDER};
        }}
        .dash-card-body table th {{
            background-color: {MAROON} !important;
            color: {WHITE} !important;
            padding: 12px 15px;
            text-align: left;
            font-weight: bold;
        }}
        .dash-card-body table td {{
            padding: 10px 15px;
            border-bottom: 1px solid {CARD_BORDER};
            color: {MAROON_TEXT} !important;
        }}
        .dash-card-body table tr:nth-child(odd) td {{
            background-color: {WHITE};
        }}
        .dash-card-body table tr:nth-child(even) td {{
            background-color: {FAINT_MAROON};
        }}
        .dash-card-body table tr:hover td {{
            background-color: {HOVER_MAROON} !important;
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
        
        .metric-grid {{
            display: grid;
            gap: 16px;
            margin-bottom: 16px;
        }}
        .metric-grid-2 {{ grid-template-columns: repeat(2, 1fr); }}
        .metric-grid-3 {{ grid-template-columns: repeat(3, 1fr); }}
        .metric-grid-4 {{ grid-template-columns: repeat(4, 1fr); }}
        .metric-grid-6 {{ grid-template-columns: repeat(6, 1fr); }}
        @media (max-width: 900px) {{
            .metric-grid-3, .metric-grid-4, .metric-grid-6 {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
        @media (max-width: 550px) {{
            .metric-grid-2, .metric-grid-3, .metric-grid-4, .metric-grid-6 {{
                grid-template-columns: 1fr;
            }}
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
        
        [data-testid="stFileUploadDropzone"] {{
            background-color: {WHITE} !important;
            border: 2px dashed {CARD_BORDER} !important;
            border-radius: 10px !important;
            padding: 20px !important;
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: wrap !important;
            align-items: center !important;
            justify-content: space-between !important;
            gap: 16px !important;
            min-height: 70px !important;
        }}
        [data-testid="stFileUploaderDropzoneInstructions"] {{
            display: flex !important;
            flex-direction: column !important;
            gap: 2px !important;
            flex: 1 1 auto !important;
            min-width: 180px !important;
        }}
        [data-testid="stFileUploaderDropzoneInstructions"] div,
        [data-testid="stFileUploaderDropzoneInstructions"] span,
        [data-testid="stFileUploaderDropzoneInstructions"] small {{
            color: {MAROON_TEXT} !important;
            font-family: 'Georgia', 'Times New Roman', serif !important;
            display: block !important;
            position: static !important;
        }}
        [data-testid="stFileUploadDropzone"] section {{
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            width: 100% !important;
            gap: 16px !important;
            position: static !important;
        }}
        [data-testid="stFileUploadDropzone"] button {{
            position: static !important;
            background-color: {MAROON} !important;
            color: {WHITE} !important;
            border: none !important;
            border-radius: 6px !important;
            flex: 0 0 auto !important;
            white-space: nowrap !important;
        }}
        [data-testid="stFileUploadDropzone"] button span,
        [data-testid="stFileUploadDropzone"] button p {{
            color: {WHITE} !important;
            position: static !important;
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
        
        .stMultiSelect label {{
            color: {MAROON_TEXT} !important;
        }}
        .stMultiSelect div[data-baseweb="select"] > div {{
            color: {MAROON_TEXT} !important;
        }}
        
        .stDateInput label {{
            color: {MAROON_TEXT} !important;
        }}
        .stDateInput input {{
            color: {MAROON_TEXT} !important;
        }}
        
        /* --- Widgets that pull from Streamlit's live theme color rather than
           plain CSS, and so can drift from the palette above on theme changes --- */
        
        a, a:visited {{
            color: {MAROON} !important;
        }}
        
        [data-baseweb="tooltip"], [data-baseweb="popover"] {{
            background-color: {WHITE} !important;
            color: {MAROON_TEXT} !important;
        }}
        
        /* Toggle switches */
        [data-baseweb="checkbox"] [aria-checked="true"] > div:first-child,
        [data-testid="stToggle"] [aria-checked="true"] {{
            background-color: {MAROON} !important;
            border-color: {MAROON} !important;
        }}
        
        /* Slider track/handle/labels */
        [data-testid="stSlider"] [role="slider"] {{
            background-color: {MAROON} !important;
            border-color: {MAROON} !important;
        }}
        [data-testid="stSlider"] div[data-baseweb="slider"] > div > div {{
            background-color: {MAROON} !important;
        }}
        [data-testid="stTickBarMin"], [data-testid="stTickBarMax"],
        [data-testid="stSliderThumbValue"] {{
            color: {MAROON_TEXT} !important;
        }}
        
        /* Progress bar */
        [data-testid="stProgress"] > div > div > div {{
            background-color: {MAROON} !important;
        }}
        
        /* Spinner */
        [data-testid="stSpinner"] svg circle {{
            stroke: {MAROON} !important;
        }}
        [data-testid="stSpinner"] p {{
            color: {MAROON_TEXT} !important;
        }}
        
        /* Toasts / notifications */
        [data-testid="stToast"] {{
            background-color: {WHITE} !important;
            color: {MAROON_TEXT} !important;
        }}
        
        /* Multiselect selected-item pills */
        [data-baseweb="tag"] {{
            background-color: {MAROON} !important;
            color: {WHITE} !important;
        }}
        [data-baseweb="tag"] span {{
            color: {WHITE} !important;
        }}
        
        /* --- Date input box + its calendar popover ---
           BaseWeb's Datepicker draws its own colors and ignores the page's
           color-scheme, so it needs to be targeted explicitly. */
        
        [data-testid="stDateInput"] [data-baseweb="base-input"],
        [data-testid="stDateInput"] [data-baseweb="input"] {{
            background-color: {WHITE} !important;
        }}
        [data-testid="stDateInput"] input {{
            background-color: {WHITE} !important;
            color: {MAROON_TEXT} !important;
        }}
        
        [data-baseweb="calendar"] {{
            background-color: {WHITE} !important;
        }}
        [data-baseweb="calendar"] * {{
            color: {MAROON_TEXT} !important;
        }}
        [data-baseweb="calendar"] div {{
            background-color: {WHITE} !important;
        }}
        [data-baseweb="calendar"] button {{
            background-color: {WHITE} !important;
            color: {MAROON_TEXT} !important;
        }}
        [data-baseweb="calendar"] button:hover {{
            background-color: {HOVER_MAROON} !important;
        }}
        [data-baseweb="calendar"] [aria-disabled="true"] {{
            color: {CARD_BORDER} !important;
        }}
        [data-baseweb="calendar"] [aria-selected="true"],
        [data-baseweb="calendar"] [aria-selected="true"]:hover {{
            background-color: {MAROON} !important;
            color: {WHITE} !important;
        }}
        [data-baseweb="calendar"] svg {{
            fill: {MAROON_TEXT} !important;
        }}
        
        /* Same dark-render issue can hit selectbox/multiselect dropdown menus */
        [data-baseweb="menu"], [data-baseweb="popover"] ul[role="listbox"] {{
            background-color: {WHITE} !important;
        }}
        [data-baseweb="menu"] li, [role="option"] {{
            background-color: {WHITE} !important;
            color: {MAROON_TEXT} !important;
        }}
        [role="option"]:hover, [role="option"][aria-selected="true"] {{
            background-color: {HOVER_MAROON} !important;
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
        'student_number': None,
        'username': None,
        'student_class': None,
        'current_page': "My Portal Dashboard",
        'admin_page': "Overview",
        'overview_month_filter': "All Time",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# ============================================================
# GOOGLE SHEETS CONNECTION
# ============================================================
@st.cache_resource
def connect_to_sheets():
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

def write_data(sheet_name, data_dict):
    """
    Write one row to a worksheet, keyed by COLUMN HEADER NAME rather than
    position. This makes writes immune to the sheet's columns being
    reordered, and means a typo in a header shows up as a blank cell
    instead of data silently landing under the wrong column.

    data_dict: {"Header Name": value, ...}
    Any header present in the sheet but missing from data_dict is written
    as an empty string. Keys in data_dict that don't match any header in
    the sheet are ignored (so double-check your header spelling matches
    exactly, including capitalization).
    """
    client = connect_to_sheets()
    for attempt in range(3):
        try:
            sheet = client.open(SHEET_NAME).worksheet(sheet_name)
            headers = [h.strip() for h in sheet.row_values(1)]
            if not headers:
                st.error(f"'{sheet_name}' has no header row — cannot map columns.")
                return False
            row = [data_dict.get(h, "") for h in headers]
            sheet.append_row(row, value_input_option="USER_ENTERED")
            time.sleep(0.7)  # let Sheets settle before any immediate re-read
            return True
        except Exception as e:
            if attempt < 2:
                connect_to_sheets.clear()
                client = connect_to_sheets()
                time.sleep(2)
            else:
                st.error(f"Failed to write to '{sheet_name}': {e}")
                return False

def update_cell(sheet_name, row, col, value):
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
    parts = name.strip().split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    elif len(parts) == 1:
        return parts[0][0].upper()
    return "ZA"

def normalize_name(name):
    return re.sub(r"\s+", " ", str(name).strip()).lower()

def generate_student_number(df_students):
    """
    Generates the next Student Number in the form R{YY}{NNN}, e.g.
    R26001, R26002... Sequence is scoped to the current year and derived
    from the highest existing number under that year's prefix already in
    the Students sheet — no separate counter to maintain, and it rolls
    over to R27001 etc. on its own next year.
    """
    year_prefix = f"R{datetime.now().strftime('%y')}"
    max_seq = 0
    if not df_students.empty and "Student Number" in df_students.columns:
        existing = df_students["Student Number"].astype(str).str.strip()
        for val in existing:
            if val.startswith(year_prefix) and val[len(year_prefix):].isdigit():
                max_seq = max(max_seq, int(val[len(year_prefix):]))
    return f"{year_prefix}{max_seq + 1:03d}"

def find_by_student_number(df, student_number, name_fallback=None, name_col="Student Name"):
    """
    Look up rows for one student using Student Number as the primary key.
    Falls back to a normalized-name match only if the sheet doesn't have
    a Student Number column yet, or the ID isn't found in it — keeps
    things working while you're still adding the header to older tabs,
    but Student Number is the real identifier going forward.
    """
    if df.empty:
        return df
    if "Student Number" in df.columns and student_number:
        match = df[df["Student Number"].astype(str).str.strip() == str(student_number).strip()]
        if not match.empty:
            return match
    if name_fallback and name_col in df.columns:
        return df[df[name_col].astype(str).apply(normalize_name) == normalize_name(name_fallback)]
    return df.iloc[0:0]

def build_student_dropdown(df_students):
    """
    Returns (display_labels, label_to_student_number) for an admin
    selectbox. Shows just the student's name normally; if two students
    share the exact same name, appends the Student Number in parentheses
    for just that pair so they stay distinguishable.
    """
    label_to_id = {}
    if df_students.empty or "Student Number" not in df_students.columns:
        return ["Select student..."], label_to_id

    df = df_students.copy()
    df.columns = df.columns.astype(str).str.strip()
    name_counts = df["Student Name"].astype(str).str.strip().value_counts()

    for _, row in df.iterrows():
        name = str(row.get("Student Name", "")).strip()
        sid = str(row.get("Student Number", "")).strip()
        if not name or not sid:
            continue
        label = f"{name} ({sid})" if name_counts.get(name, 0) > 1 else name
        label_to_id[label] = sid

    return ["Select student..."] + sorted(label_to_id.keys()), label_to_id

# ============================================================
# SUBJECTS, LEVELS & FEE STRUCTURE
# ============================================================
# Edit these lists to match your actual curriculum — they're just plain
# Python lists, no need to touch the Google Sheet to change them.
LEVELS = ["O Level", "A Level"]
LEARNING_MODES = ["One-on-One", "Group"]

O_LEVEL_SUBJECTS = [
    "Mathematics", "English Language", "Combined Science", "Biology",
    "Chemistry", "Physics", "Geography", "History", "Accounts",
    "Business Studies", "Shona", "Ndebele", "Computer Science",
    "Agriculture", "Religious Studies",
]

A_LEVEL_SUBJECTS = [
    "Mathematics", "Physics", "Chemistry", "Biology", "Geography",
    "History", "Accounting", "Business Studies", "Economics",
    "Computer Science", "English Literature", "Sociology", "Law",
]

SUBJECTS_BY_LEVEL = {"O Level": O_LEVEL_SUBJECTS, "A Level": A_LEVEL_SUBJECTS}

# USD per subject per month
SUBJECT_PRICING = {
    ("O Level", "One-on-One"): 15.0,
    ("O Level", "Group"): 10.0,
    ("A Level", "One-on-One"): 25.0,
    ("A Level", "Group"): 20.0,
}

def get_subject_price(level, mode):
    return SUBJECT_PRICING.get((level, mode), 0.0)

# ============================================================
# MONTH HANDLING (billing period — replaces "Term" everywhere)
# ============================================================
MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

def month_year_picker(label, key_prefix, default_date=None):
    """Two dropdowns (Month, Year) combined into a 'Month YYYY' string,
    e.g. 'June 2026'. Avoids maintaining a hardcoded, ever-growing list
    of every month/year combination."""
    default_date = default_date or date.today()
    years = list(range(date.today().year - 1, date.today().year + 3))
    col_a, col_b = st.columns(2)
    with col_a:
        month_name = st.selectbox(
            f"{label} Month", MONTH_NAMES,
            index=default_date.month - 1, key=f"{key_prefix}_month"
        )
    with col_b:
        year = st.selectbox(
            f"{label} Year", years,
            index=years.index(default_date.year) if default_date.year in years else 0,
            key=f"{key_prefix}_year"
        )
    return f"{month_name} {year}"

def month_sort_key(month_str):
    """('June 2026') -> (2026, 6), for chronological comparison/sorting."""
    try:
        name, year = str(month_str).strip().split()
        return (int(year), MONTH_NAMES.index(name) + 1)
    except (ValueError, IndexError):
        return (0, 0)

def get_available_months(sheet_names):
    months = set()
    for sheet_name in sheet_names:
        df = load_data(sheet_name)
        if not df.empty and "Month" in df.columns:
            df.columns = df.columns.astype(str).str.strip()
            for m in df["Month"].dropna().unique():
                if str(m).strip():
                    months.add(str(m).strip())
    return sorted(months, key=month_sort_key, reverse=True)

def filter_by_month(df, month):
    if df.empty or month == "All Time" or "Month" not in df.columns:
        return df
    df.columns = df.columns.astype(str).str.strip()
    return df[df["Month"].astype(str).str.strip() == month.strip()]

def compute_expected_monthly_fee(df_enrollments, student_number, month):
    """Sum of Monthly Fee for a student's enrollments that are billable
    in the given month: started on/before it, and either still Active
    or dropped in a later month than the one being checked."""
    if df_enrollments.empty or "Student Number" not in df_enrollments.columns:
        return 0.0
    month_key = month_sort_key(month)
    rows = df_enrollments[df_enrollments["Student Number"].astype(str).str.strip() == str(student_number).strip()]
    total = 0.0
    for _, row in rows.iterrows():
        start = month_sort_key(row.get("Start Month", ""))
        if start > month_key:
            continue
        status = str(row.get("Status", "Active")).strip()
        dropped_month = str(row.get("Exit Month", "")).strip()
        if status == "Dropped" and dropped_month:
            if month_key >= month_sort_key(dropped_month):
                continue
        total += pd.to_numeric(row.get("Monthly Fee", 0), errors="coerce") or 0.0
    return total

def hash_password(plain_password):
    """One-way hash for storage. There is no function to reverse this —
    verification only ever checks 'does this input match', it never
    recovers the original password."""
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password, stored_value):
    """Check a login attempt against a stored value.

    Supports two shapes of stored_value:
    - A bcrypt hash (starts with $2b$/$2a$/$2y$) -> proper hash check.
    - A legacy plaintext row from before this change -> direct string
      compare, so old rows in the sheet don't lock anyone out. Callers
      should re-hash and save the password after a successful legacy
      match, so rows get upgraded automatically the next time someone
      logs in with them.
    """
    stored_value = str(stored_value)
    if stored_value.startswith(("$2b$", "$2a$", "$2y$")):
        try:
            return bcrypt.checkpw(plain_password.encode(), stored_value.encode())
        except ValueError:
            return False
    return plain_password.strip() == stored_value.strip()

def is_hashed(stored_value):
    return str(stored_value).startswith(("$2b$", "$2a$", "$2y$"))

def render_kv_table(pairs):
    """Render a list of (label, value) pairs as a bordered table with
    alternating faint-maroon rows."""
    html = f'<table style="width:100%; border-collapse:collapse; border:1px solid {CARD_BORDER};">'
    for i, (label, value) in enumerate(pairs):
        bg = FAINT_MAROON if i % 2 == 0 else WHITE
        html += f'<tr style="background-color:{bg};">'
        html += f'<td style="padding:10px 12px; border:1px solid {CARD_BORDER}; color:{MAROON_TEXT}; width:45%;"><strong>{label}</strong></td>'
        html += f'<td style="padding:10px 12px; border:1px solid {CARD_BORDER}; color:{MAROON_TEXT};">{value}</td>'
        html += '</tr>'
    html += '</table>'
    st.markdown(html, unsafe_allow_html=True)

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
                    user_match = df_logins[
                        df_logins["Username"].astype(str).str.strip() == username.strip()
                    ]
                    if not user_match.empty and verify_password(password, user_match.iloc[0].get("Password", "")):
                        student = user_match.iloc[0]

                        # Legacy row still in plaintext -> upgrade it now that we
                        # have a confirmed-correct password to hash.
                        if not is_hashed(student.get("Password", "")):
                            row_idx = user_match.index[0] + 2
                            pw_col_idx = df_logins.columns.get_loc("Password") + 1
                            update_cell("Student Logins", row_idx, pw_col_idx, hash_password(password))

                        st.session_state.logged_in = True
                        st.session_state.user_type = "student"
                        st.session_state.username = username.strip()
                        st.session_state.student_name = str(student["Student Name"]).strip()
                        st.session_state.student_number = str(student.get("Student Number", "")).strip()
                        st.session_state.student_class = str(student["Class"]).strip()
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
                else:
                    st.error("Unable to load login data.")
        
        with tab2:
            st.markdown("### Admin Login")
            admin_username = st.text_input("Admin Username", key="admin_user", value="admin")
            admin_pass = st.text_input("Admin Password", type="password", key="admin_pass")
            
            if st.button("Login", key="admin_login_btn", use_container_width=True):
                df_admins = load_data("Admin Logins")
                
                if df_admins.empty:
                    # First-ever admin login: seed the sheet with a hashed
                    # account instead of leaving the password hardcoded in
                    # source. Uses the same bootstrap password as before,
                    # once, to avoid locking anyone out on rollout.
                    if admin_username.strip() == "admin" and admin_pass == "admin2026":
                        write_data("Admin Logins", {
                            "Username": "admin",
                            "Password": hash_password("admin2026"),
                        })
                        st.session_state.logged_in = True
                        st.session_state.user_type = "admin"
                        st.session_state.username = "admin"
                        st.session_state.student_name = "Administrator"
                        st.rerun()
                    else:
                        st.error("Invalid admin username or password.")
                else:
                    df_admins.columns = df_admins.columns.astype(str).str.strip()
                    admin_match = df_admins[df_admins["Username"].astype(str).str.strip() == admin_username.strip()]
                    if not admin_match.empty and verify_password(admin_pass, admin_match.iloc[0].get("Password", "")):
                        admin_row = admin_match.iloc[0]
                        
                        # Upgrade a legacy plaintext admin row the same way
                        # student rows get upgraded.
                        if not is_hashed(admin_row.get("Password", "")):
                            row_idx = admin_match.index[0] + 2
                            pw_col_idx = df_admins.columns.get_loc("Password") + 1
                            update_cell("Admin Logins", row_idx, pw_col_idx, hash_password(admin_pass))
                        
                        st.session_state.logged_in = True
                        st.session_state.user_type = "admin"
                        st.session_state.username = admin_username.strip()
                        st.session_state.student_name = "Administrator"
                        st.rerun()
                    else:
                        st.error("Invalid admin username or password.")
        
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
            profile = df_profiles[df_profiles["Username"].astype(str).str.strip().str.lower() == st.session_state.username.strip().lower()]
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
        
        pages = ["My Portal Dashboard", "My Performance", "My Fees", "My Attendance", "Profile Settings"]
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
    
    if page == "My Portal Dashboard":
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
    student_number = st.session_state.get("student_number", "")
    st.markdown(f"## Welcome, {student_name}!")
    st.markdown(f"**Class:** {student_class}")
    
    df_students = load_data("Students")
    student_info = pd.DataFrame()
    if not df_students.empty:
        df_students.columns = df_students.columns.astype(str).str.strip()
        student_info = find_by_student_number(df_students, student_number, name_fallback=student_name)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="dash-card"><div class="dash-card-header">Personal Details</div><div class="dash-card-body">', unsafe_allow_html=True)
        if not student_info.empty:
            s = student_info.iloc[0]
            details = [
                ("Date of Birth", s.get("Date of Birth", "N/A")),
                ("Gender", s.get("Gender", "N/A")),
                ("Guardian", s.get("Guardian Name", "N/A")),
                ("Guardian Phone", s.get("Guardian Phone", "N/A")),
                ("Address", s.get("Address", "N/A")),
                ("Enrollment Date", s.get("Enrollment Date", "N/A")),
            ]
            render_kv_table(details)
        else:
            st.info("No details found.")
        st.markdown('</div></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="dash-card"><div class="dash-card-header">Academic Details</div><div class="dash-card-body">', unsafe_allow_html=True)
        if not student_info.empty:
            s = student_info.iloc[0]
            
            display_student_number = s.get("Student Number", student_number) or "N/A"
            
            reg_status = "Active"
            df_logins = load_data("Student Logins")
            if not df_logins.empty:
                df_logins.columns = df_logins.columns.astype(str).str.strip()
                login_row = find_by_student_number(df_logins, student_number, name_fallback=student_name)
                if not login_row.empty:
                    reg_status = str(login_row.iloc[0].get("Status", "Active"))
            
            current_month = "N/A"
            df_perf = load_data("Performance")
            df_fees = load_data("Fee Payments")
            latest_months = []
            
            if not df_perf.empty:
                df_perf.columns = df_perf.columns.astype(str).str.strip()
                student_perf = find_by_student_number(df_perf, student_number, name_fallback=student_name)
                if not student_perf.empty and "Month" in student_perf.columns:
                    latest_months.extend(student_perf["Month"].dropna().tolist())
            
            if not df_fees.empty:
                df_fees.columns = df_fees.columns.astype(str).str.strip()
                name_col = "Name of Student" if "Name of Student" in df_fees.columns else "Student Name"
                student_payments = find_by_student_number(df_fees, student_number, name_fallback=student_name, name_col=name_col)
                if not student_payments.empty and "Month" in student_payments.columns:
                    latest_months.extend(student_payments["Month"].dropna().tolist())
            
            if latest_months:
                current_month = sorted(latest_months, key=month_sort_key, reverse=True)[0]
            
            academic_details = [
                ("Student Number", display_student_number),
                ("Class", student_class),
                ("Registration Status", f'<span style="color:{GREEN}; font-weight:bold;">{reg_status}</span>'),
                ("Current Month", current_month),
            ]
            render_kv_table(academic_details)
        else:
            st.info("No academic details found.")
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="dash-card"><div class="dash-card-header">Financial Details</div><div class="dash-card-body">', unsafe_allow_html=True)
        df_fee_status = load_data("Fee Status")
        if not df_fee_status.empty:
            df_fee_status.columns = df_fee_status.columns.astype(str).str.strip()
            # Fee Status isn't written by this app (looks maintained
            # separately/via formulas), so it still keys off name only
            # until that sheet is confirmed to carry Student Number too.
            fee_row = df_fee_status[df_fee_status["Student Name"].astype(str).apply(normalize_name) == normalize_name(student_name)]
            if not fee_row.empty:
                financial_details = [(col, fee_row.iloc[0][col]) for col in fee_row.columns if col != "Student Name"]
                render_kv_table(financial_details)
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
    my_perf = find_by_student_number(df_perf, st.session_state.get("student_number", ""), name_fallback=student_name)
    
    if my_perf.empty:
        st.info("No results found for you yet.")
        return
    
    months = my_perf["Month"].unique()
    for month in sorted(months, key=month_sort_key, reverse=True):
        month_data = my_perf[my_perf["Month"] == month]
        st.markdown(f"### {month}")
        
        display_cols = ["Subject", "Mark", "Grade", "Comment"]
        display_data = month_data[[c for c in display_cols if c in month_data.columns]]
        
        st.markdown('<div class="dash-card"><div class="dash-card-body">', unsafe_allow_html=True)
        st.dataframe(display_data, use_container_width=True, hide_index=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

def student_fees(student_name, student_class):
    st.markdown("## My Fees")
    
    student_number = st.session_state.get("student_number", "")
    
    df_enroll = load_data("Subject Enrollments")
    current_month_str = f"{MONTH_NAMES[date.today().month - 1]} {date.today().year}"
    
    st.markdown('<div class="dash-card"><div class="dash-card-header">My Subjects</div><div class="dash-card-body">', unsafe_allow_html=True)
    if not df_enroll.empty and "Student Number" in df_enroll.columns:
        df_enroll.columns = df_enroll.columns.astype(str).str.strip()
        my_enrollments = find_by_student_number(df_enroll, student_number, name_fallback=student_name)
        active_enrollments = my_enrollments[my_enrollments["Status"].astype(str).str.strip() == "Active"] if "Status" in my_enrollments.columns else my_enrollments.iloc[0:0]
        
        if not active_enrollments.empty:
            display_cols = [c for c in ["Level", "Subject", "Mode", "Monthly Fee"] if c in active_enrollments.columns]
            st.dataframe(active_enrollments[display_cols], use_container_width=True, hide_index=True)
            
            expected_this_month = compute_expected_monthly_fee(df_enroll, student_number, current_month_str)
            
            df_payments_for_owing = load_data("Fee Payments")
            paid_this_month = 0.0
            if not df_payments_for_owing.empty:
                df_payments_for_owing.columns = df_payments_for_owing.columns.astype(str).str.strip()
                df_this_month = filter_by_month(df_payments_for_owing, current_month_str)
                my_payments_this_month = find_by_student_number(df_this_month, student_number, name_fallback=student_name, name_col="Name of Student" if "Name of Student" in df_this_month.columns else "Student Name")
                paid_this_month = safe_sum(my_payments_this_month, "Amount Paid")
            
            owing_this_month = max(expected_this_month - paid_this_month, 0.0)
            owing_color = GREEN if owing_this_month <= 0 else RED
            
            st.markdown(f"""
            <div class="metric-grid metric-grid-3" style="margin-top:12px;">
                <div class="metric-card"><div class="metric-value">${expected_this_month:,.0f}</div><div class="metric-label">{current_month_str} — Expected</div></div>
                <div class="metric-card"><div class="metric-value" style="color:{GREEN};">${paid_this_month:,.0f}</div><div class="metric-label">Paid</div></div>
                <div class="metric-card" style="border:2px solid {owing_color};"><div class="metric-value" style="color:{owing_color};">${owing_this_month:,.0f}</div><div class="metric-label">Owing</div></div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No active subject enrollments.")
    else:
        st.info("No subject enrollments recorded yet.")
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    df_payments = load_data("Fee Payments")
    df_fee_status = load_data("Fee Status")
    
    if not df_fee_status.empty:
        df_fee_status.columns = df_fee_status.columns.astype(str).str.strip()
        fee_row = df_fee_status[df_fee_status["Student Name"].astype(str).apply(normalize_name) == normalize_name(student_name)]
        
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
        name_col = "Name of Student" if "Name of Student" in df_payments.columns else "Student Name"
        my_payments = find_by_student_number(df_payments, student_number, name_fallback=student_name, name_col=name_col)
        
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
    my_att = find_by_student_number(df_att, st.session_state.get("student_number", ""), name_fallback=student_name)
    
    st.markdown('<div class="dash-card"><div class="dash-card-header">Last 5 Working Days</div><div class="dash-card-body">', unsafe_allow_html=True)
    if not my_att.empty:
        row = my_att.iloc[0]
        date_cols = [c for c in my_att.columns if c not in ("Student Name", "Student Number")]
        
        html = '<table style="width:100%; border-collapse:collapse;">'
        html += f'<tr style="background-color:{MAROON}; color:{WHITE};">'
        html += '<th style="padding:12px; text-align:left;">Day</th>'
        html += '<th style="padding:12px; text-align:left;">Status</th>'
        html += '</tr>'
        for i, col in enumerate(date_cols):
            val = str(row[col]).strip()
            status_class = "positive" if val == "Present" else ("negative" if val == "Absent" else "")
            bg = FAINT_MAROON if i % 2 == 0 else WHITE
            html += f'<tr style="background-color:{bg};">'
            html += f'<td style="padding:12px;">{col}</td>'
            html += f'<td style="padding:12px;"><span class="{status_class}">{val}</span></td>'
            html += '</tr>'
        html += '</table>'
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
                    existing = df_profiles[df_profiles["Username"].astype(str).str.strip().str.lower() == st.session_state.username.strip().lower()]
                    if not existing.empty:
                        row_idx = existing.index[0] + 2
                        photo_col_idx = df_profiles.columns.get_loc("Profile Photo") + 1
                        update_cell("Student Profiles", row_idx, photo_col_idx, b64_str)
                    else:
                        write_data("Student Profiles", {
                            "Username": st.session_state.username,
                            "Display Name": st.session_state.student_name,
                            "Profile Photo": b64_str,
                        })
                    st.success("Profile photo updated! Refresh to see changes.")
                    st.rerun()
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="dash-card"><div class="dash-card-header">Change Username</div><div class="dash-card-body">', unsafe_allow_html=True)
    
    st.markdown(f"**Current Username:** {st.session_state.username}")
    new_username = st.text_input("New Username", placeholder="Enter a new username", key="new_username_input")
    
    if st.button("Update Username", use_container_width=True):
        new_username_clean = new_username.strip()
        if not new_username_clean:
            st.error("Please enter a new username.")
        elif new_username_clean == st.session_state.username:
            st.warning("That's already your current username.")
        else:
            df_logins = load_data("Student Logins")
            if df_logins.empty:
                st.error("Unable to load login data.")
            else:
                df_logins.columns = df_logins.columns.astype(str).str.strip()
                taken = df_logins[df_logins["Username"].astype(str).str.strip().str.lower() == new_username_clean.lower()]
                if not taken.empty:
                    st.error("That username is already taken. Please choose another.")
                else:
                    my_row = df_logins[df_logins["Username"].astype(str).str.strip() == st.session_state.username.strip()]
                    if my_row.empty:
                        st.error("Could not find your login record.")
                    else:
                        row_idx = my_row.index[0] + 2
                        username_col_idx = df_logins.columns.get_loc("Username") + 1
                        success = update_cell("Student Logins", row_idx, username_col_idx, new_username_clean)
                        
                        if success:
                            df_profiles = load_data("Student Profiles")
                            if not df_profiles.empty:
                                df_profiles.columns = df_profiles.columns.astype(str).str.strip()
                                profile_row = df_profiles[df_profiles["Username"].astype(str).str.strip() == st.session_state.username.strip()]
                                if not profile_row.empty:
                                    p_row_idx = profile_row.index[0] + 2
                                    p_username_col_idx = df_profiles.columns.get_loc("Username") + 1
                                    update_cell("Student Profiles", p_row_idx, p_username_col_idx, new_username_clean)
                            
                            st.session_state.username = new_username_clean
                            st.success(f"Username updated to '{new_username_clean}'. Use this to log in next time.")
                            st.rerun()
                        else:
                            st.error("Failed to update username.")
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="dash-card"><div class="dash-card-header">Change Password</div><div class="dash-card-body">', unsafe_allow_html=True)
    
    current_password = st.text_input("Current Password", type="password", key="current_pw_input")
    new_password = st.text_input("New Password", type="password", key="new_pw_input")
    confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_pw_input")
    
    if st.button("Update Password", use_container_width=True):
        if not current_password or not new_password or not confirm_password:
            st.error("Please fill in all three fields.")
        elif new_password != confirm_password:
            st.error("New password and confirmation don't match.")
        elif len(new_password) < 6:
            st.error("New password should be at least 6 characters.")
        else:
            df_logins = load_data("Student Logins")
            if df_logins.empty:
                st.error("Unable to load login data.")
            else:
                df_logins.columns = df_logins.columns.astype(str).str.strip()
                my_row = df_logins[df_logins["Username"].astype(str).str.strip() == st.session_state.username.strip()]
                if my_row.empty:
                    st.error("Could not find your login record.")
                elif not verify_password(current_password, my_row.iloc[0].get("Password", "")):
                    st.error("Current password is incorrect.")
                else:
                    row_idx = my_row.index[0] + 2
                    pw_col_idx = df_logins.columns.get_loc("Password") + 1
                    success = update_cell("Student Logins", row_idx, pw_col_idx, hash_password(new_password))
                    if success:
                        st.success("Password updated. Use your new password next time you log in.")
                    else:
                        st.error("Failed to update password.")
    
    st.markdown('</div></div>', unsafe_allow_html=True)

# ============================================================
# ADMIN DASHBOARD - HELPERS
# ============================================================
def safe_sum(df, column_name):
    if df.empty or column_name not in df.columns:
        return 0.0
    return pd.to_numeric(
        df[column_name].astype(str).str.replace(r'[$,]', '', regex=True),
        errors='coerce'
    ).sum()

# ============================================================
# AUTO-GRADING SYSTEM
# ============================================================
def calculate_grade(mark):
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
            "Subject Enrollments",
            "Fees Owing",
            "Record Fee Payment",
            "Enter Performance",
            "Student Grades",
            "Mark Attendance",
            "Record Expense",
            "Record Other Income",
            "Salary Payments",
            "All Students",
            "Account Settings",
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
    elif page == "Subject Enrollments":
        admin_subject_enrollments()
    elif page == "Fees Owing":
        admin_fees_owing()
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
    elif page == "Account Settings":
        admin_account_settings()

# ============================================================
# ADMIN OVERVIEW
# ============================================================
def admin_overview():
    st.markdown("## Admin Overview")
    
    available_months = get_available_months(["Fee Payments", "Expenses", "Other Income", "Performance", "Salaries", "Subject Enrollments"])
    month_options = ["All Time"] + available_months
    
    col_filter, col_space = st.columns([1, 3])
    with col_filter:
        selected_month = st.selectbox(
            "Filter Financials by Month",
            month_options,
            key="overview_month_filter"
        )
    
    df_students = load_data("Students")
    df_payments_all = load_data("Fee Payments")
    df_expenses_all = load_data("Expenses")
    df_other_income_all = load_data("Other Income")
    df_enrollments_all = load_data("Subject Enrollments")
    
    total_students = len(df_students) if not df_students.empty else 0
    all_time_fees = safe_sum(df_payments_all, "Amount Paid")
    all_time_other = safe_sum(df_other_income_all, "Amount")
    all_time_expenses = safe_sum(df_expenses_all, "Amount")
    all_time_income = all_time_fees + all_time_other
    
    df_payments_month = filter_by_month(df_payments_all.copy(), selected_month)
    df_expenses_month = filter_by_month(df_expenses_all.copy(), selected_month)
    df_other_income_month = filter_by_month(df_other_income_all.copy(), selected_month)
    
    month_fees = safe_sum(df_payments_month, "Amount Paid")
    month_other = safe_sum(df_other_income_month, "Amount")
    month_expenses = safe_sum(df_expenses_month, "Amount")
    month_income = month_fees + month_other
    month_profit = month_income - month_expenses
    
    investments = month_profit * 0.10
    salaries_pool = month_profit * 0.20
    tithe = month_profit * 0.10
    alter = month_profit * 0.05
    operations = month_profit * 0.10
    net_profit = month_profit * 0.45
    per_person = salaries_pool / 4
    
    class_count = "N/A"
    if not df_students.empty:
        df_students.columns = df_students.columns.astype(str).str.strip()
        if "Class" in df_students.columns:
            class_count = str(df_students["Class"].nunique())
    
    badge_html = '<span class="term-badge">ALL TIME</span>' if selected_month == "All Time" else f'<span class="term-badge">{selected_month}</span>'
    profit_color = GREEN if month_profit >= 0 else RED
    
    st.markdown(f"""
    <div class="dash-card">
        <div class="dash-card-header">Enrollment<span class="lifetime-badge">ALL TIME</span></div>
        <div class="dash-card-body">
            <div class="metric-grid metric-grid-4">
                <div class="metric-card"><div class="metric-value">{total_students}</div><div class="metric-label">Total Students</div></div>
                <div class="metric-card"><div class="metric-value">{class_count}</div><div class="metric-label">Classes</div></div>
                <div class="metric-card"><div class="metric-value">${all_time_income:,.0f}</div><div class="metric-label">Lifetime Income</div></div>
                <div class="metric-card"><div class="metric-value">${all_time_expenses:,.0f}</div><div class="metric-label">Lifetime Expenses</div></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="dash-card">
        <div class="dash-card-header">Financials{badge_html}</div>
        <div class="dash-card-body">
            <h4>Income</h4>
            <div class="metric-grid metric-grid-3">
                <div class="metric-card"><div class="metric-value">${month_fees:,.0f}</div><div class="metric-label">Fees Income</div></div>
                <div class="metric-card"><div class="metric-value">${month_other:,.0f}</div><div class="metric-label">Other Income</div></div>
                <div class="metric-card"><div class="metric-value" style="color:{MAROON};">${month_income:,.0f}</div><div class="metric-label">Total Income</div></div>
            </div>
            <h4>Expenses</h4>
            <div class="metric-grid metric-grid-2">
                <div class="metric-card"><div class="metric-value" style="color:{RED};">${month_expenses:,.0f}</div><div class="metric-label">Total Expenses</div></div>
            </div>
            <h4>Profit</h4>
            <div class="metric-grid metric-grid-3">
                <div class="metric-card"><div class="metric-value">${month_income:,.0f}</div><div class="metric-label">Total Income</div></div>
                <div class="metric-card"><div class="metric-value" style="color:{RED};">${month_expenses:,.0f}</div><div class="metric-label">Total Expenses</div></div>
                <div class="metric-card"><div class="metric-value" style="color:{profit_color};">${month_profit:,.0f}</div><div class="metric-label">Gross Profit</div></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="dash-card">
        <div class="dash-card-header">Profit Distribution{badge_html}</div>
        <div class="dash-card-body">
            <p><strong>Gross Profit:</strong> ${month_profit:,.0f}</p>
            <hr class="section-divider">
            <div class="metric-grid metric-grid-6">
                <div class="metric-card"><div class="metric-value">${investments:,.0f}</div><div class="metric-label">Investments</div><div class="metric-label">10%</div></div>
                <div class="metric-card"><div class="metric-value">${salaries_pool:,.0f}</div><div class="metric-label">Salaries</div><div class="metric-label">20%</div></div>
                <div class="metric-card"><div class="metric-value">${tithe:,.0f}</div><div class="metric-label">Tithe</div><div class="metric-label">10%</div></div>
                <div class="metric-card"><div class="metric-value">${alter:,.0f}</div><div class="metric-label">Alter</div><div class="metric-label">5%</div></div>
                <div class="metric-card"><div class="metric-value">${operations:,.0f}</div><div class="metric-label">Operations</div><div class="metric-label">10%</div></div>
                <div class="metric-card" style="border:2px solid {GREEN};"><div class="metric-value" style="color:{GREEN};">${net_profit:,.0f}</div><div class="metric-label">Retained Profit</div><div class="metric-label">45%</div></div>
            </div>
            <hr class="section-divider">
            <h4>Salaries</h4>
            <div class="metric-grid metric-grid-4">
                <div class="metric-card"><div class="metric-value">${per_person:,.0f}</div><div class="metric-label">Mr Kawonde</div><div class="metric-label">5%</div></div>
                <div class="metric-card"><div class="metric-value">${per_person:,.0f}</div><div class="metric-label">Mrs Kawonde</div><div class="metric-label">5%</div></div>
                <div class="metric-card"><div class="metric-value">${per_person:,.0f}</div><div class="metric-label">Nextvantage Analytics</div><div class="metric-label">5%</div></div>
                <div class="metric-card"><div class="metric-value">${per_person:,.0f}</div><div class="metric-label">Miss Mutasvu</div><div class="metric-label">5%</div></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # --- Subject fees: expected vs. collected vs. owing, for the selected month ---
    if selected_month != "All Time" and not df_enrollments_all.empty and "Student Number" in df_enrollments_all.columns:
        df_enrollments_all.columns = df_enrollments_all.columns.astype(str).str.strip()
        active_student_numbers = df_enrollments_all["Student Number"].astype(str).str.strip().unique()
        
        expected_total = 0.0
        for sid in active_student_numbers:
            expected_total += compute_expected_monthly_fee(df_enrollments_all, sid, selected_month)
        
        collected_total = month_fees  # Fee Payments total for the selected month
        owing_total = max(expected_total - collected_total, 0.0)
        owing_color = GREEN if owing_total <= 0 else RED
        
        st.markdown(f"""
        <div class="dash-card">
            <div class="dash-card-header">Subject Fees — Expected vs Collected<span class="term-badge">{selected_month}</span></div>
            <div class="dash-card-body">
                <div class="metric-grid metric-grid-3">
                    <div class="metric-card"><div class="metric-value">${expected_total:,.0f}</div><div class="metric-label">Expected (Enrolled Subjects)</div></div>
                    <div class="metric-card"><div class="metric-value" style="color:{GREEN};">${collected_total:,.0f}</div><div class="metric-label">Collected</div></div>
                    <div class="metric-card" style="border:2px solid {owing_color};"><div class="metric-value" style="color:{owing_color};">${owing_total:,.0f}</div><div class="metric-label">Owing</div></div>
                </div>
                <p style="font-size:13px; color:{SKY_BLUE}; margin-top:8px;">See the "Fees Owing" page for a per-student breakdown.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif selected_month == "All Time":
        st.info("Select a specific month above to see expected vs. collected subject fees for that month.")


# ============================================================
# STUDENT GRADES PAGE
# ============================================================
def admin_student_grades():
    st.markdown("## Student Grades")
    
    df_performance_all = load_data("Performance")
    
    available_months = get_available_months(["Performance"])
    month_options = ["All Time"] + available_months
    
    col_filter, col_space = st.columns([1, 3])
    with col_filter:
        selected_month = st.selectbox("Filter by Month", month_options, key="grades_month_filter")
    
    df_perf = filter_by_month(df_performance_all.copy(), selected_month)
    
    badge_html = '<span class="term-badge">ALL TIME</span>' if selected_month == "All Time" else f'<span class="term-badge">{selected_month}</span>'
    st.markdown(f'<div class="dash-card"><div class="dash-card-header">Grade Records{badge_html}</div><div class="dash-card-body">', unsafe_allow_html=True)
    
    if not df_perf.empty:
        df_perf.columns = df_perf.columns.astype(str).str.strip()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            all_students = ["All"] + sorted(df_perf["Student Name"].dropna().unique().tolist()) if "Student Name" in df_perf.columns else ["All"]
            filter_student = st.selectbox("Student", all_students, key="grades_student")
        with col2:
            all_subjects = ["All"] + sorted(df_perf["Subject"].dropna().unique().tolist()) if "Subject" in df_perf.columns else ["All"]
            filter_subject = st.selectbox("Subject", all_subjects, key="grades_subject")
        with col3:
            all_grade_vals = ["All"] + sorted(df_perf["Grade"].dropna().unique().tolist()) if "Grade" in df_perf.columns else ["All"]
            filter_grade = st.selectbox("Grade", all_grade_vals, key="grades_grade")
        with col4:
            st.write("")
        
        filtered = df_perf.copy()
        if filter_student != "All" and "Student Name" in filtered.columns:
            filtered = filtered[filtered["Student Name"].astype(str).str.strip() == filter_student.strip()]
        if filter_subject != "All" and "Subject" in filtered.columns:
            filtered = filtered[filtered["Subject"].astype(str).str.strip() == filter_subject.strip()]
        if filter_grade != "All" and "Grade" in filtered.columns:
            filtered = filtered[filtered["Grade"].astype(str).str.strip() == filter_grade.strip()]
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Records", len(filtered))
        with col2:
            marks_numeric = pd.to_numeric(filtered["Mark"], errors="coerce") if "Mark" in filtered.columns else pd.Series(dtype=float)
            avg_mark = marks_numeric.mean() if not filtered.empty and not marks_numeric.empty else 0
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
        if "Mark" in filtered.columns and not filtered.empty:
            invalid_mark_count = marks_numeric.isna().sum()
            if invalid_mark_count > 0:
                st.warning(f"{invalid_mark_count} record(s) have a non-numeric Mark and were excluded from the average above.")
        st.markdown(f"**Showing {len(filtered)} record(s)**")
        
        if not filtered.empty:
            html = '<table style="width:100%; border-collapse:collapse; font-size:14px;">'
            html += f'<tr style="background-color:{MAROON}; color:{WHITE};">'
            for col in filtered.columns:
                html += f'<th style="padding:10px 12px; text-align:left;">{col}</th>'
            html += '</tr>'
            
            for idx, row in filtered.iterrows():
                bg = FAINT_MAROON if idx % 2 == 0 else WHITE
                html += f'<tr>'
                for col in filtered.columns:
                    val = row[col]
                    if col == "Grade":
                        gc = grade_color(str(val).strip())
                        html += f'<td style="padding:10px 12px; font-weight:bold; color:{gc}; background-color:{bg};">{val}</td>'
                    elif col == "Mark":
                        html += f'<td style="padding:10px 12px; background-color:{bg};">{val}%</td>'
                    else:
                        html += f'<td style="padding:10px 12px; color:{MAROON_TEXT}; background-color:{bg};">{val}</td>'
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
    for idx, (grade, mark_range, color, desc) in enumerate(scale_data):
        bg = FAINT_MAROON if idx % 2 == 0 else WHITE
        html += f'<tr><td style="padding:10px; font-weight:bold; font-size:18px; color:{color}; background-color:{bg};">{grade}</td><td style="padding:10px; color:{MAROON_TEXT}; background-color:{bg};">{mark_range}</td><td style="padding:10px; color:{MAROON_TEXT}; background-color:{bg};">{desc}</td></tr>'
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
        guardian_name = st.text_input("Guardian Name*")
    
    with col2:
        student_class = st.text_input("Class*", placeholder="e.g., Grade 1, Form 2")
        guardian_phone = st.text_input("Guardian Phone*")
        address = st.text_area("Address")
        enrollment_date = st.date_input("Enrollment Date*", value=date.today())
    
    st.markdown("---")
    st.markdown("### Login Credentials")
    username = st.text_input("Username*", placeholder="Auto-generated if left blank")
    password = st.text_input("Password*", type="password")
    
    if st.button("Register Student", use_container_width=True):
        if not student_name or not student_class or not guardian_name:
            st.error("Please fill in all required fields (*)")
        else:
            df_logins = load_data("Student Logins")
            existing_usernames = set()
            if not df_logins.empty and "Username" in df_logins.columns:
                existing_usernames = set(df_logins["Username"].astype(str).str.strip().str.lower())

            username_clean = username.strip()
            username_taken = bool(username_clean) and username_clean.lower() in existing_usernames

            if username_taken:
                st.error(f"Username '{username_clean}' is already taken. Please choose a different one.")
            else:
                if username_clean:
                    final_username = username_clean
                else:
                    base = student_name.lower().replace(" ", ".")
                    final_username = base + str(random.randint(10, 99))
                    attempts = 0
                    while final_username.lower() in existing_usernames and attempts < 20:
                        final_username = base + str(random.randint(10, 99))
                        attempts += 1

                final_password = password if password else "student123"

                df_students_existing = load_data("Students")
                new_student_number = generate_student_number(df_students_existing)

                success1 = write_data("Students", {
                    "Student Number": new_student_number,
                    "Timestamp": str(datetime.now()),
                    "Student Name": student_name,
                    "Class": student_class,
                    "Date of Birth": str(dob),
                    "Gender": gender,
                    "Guardian Name": guardian_name,
                    "Guardian Phone": guardian_phone,
                    "Address": address,
                    "Enrollment Date": str(enrollment_date),
                })

                success2 = write_data("Student Logins", {
                    "Student Number": new_student_number,
                    "Student Name": student_name,
                    "Username": final_username,
                    "Password": hash_password(final_password),
                    "Class": student_class,
                    "Status": "Active",
                })

                if success1 and success2:
                    st.success(f"Student registered successfully!\n\nStudent Number: {new_student_number}\nUsername: {final_username}\nPassword: {final_password}")
                    st.balloons()
                else:
                    st.error("There was an error saving to the database.")
    
    st.markdown('</div></div>', unsafe_allow_html=True)

def admin_subject_enrollments():
    st.markdown("## Subject Enrollments")
    
    df_students = load_data("Students")
    if not df_students.empty:
        df_students.columns = df_students.columns.astype(str).str.strip()
    student_display_list, student_label_to_id = build_student_dropdown(df_students)
    
    tab1, tab2, tab3 = st.tabs(["Enroll in a Subject", "Manage / Drop Enrollments", "Fees Structure"])
    
    with tab1:
        st.markdown('<div class="dash-card"><div class="dash-card-header">New Enrollment</div><div class="dash-card-body">', unsafe_allow_html=True)
        
        selected_label = st.selectbox("Student*", student_display_list, key="enroll_student")
        col1, col2 = st.columns(2)
        with col1:
            level = st.selectbox("Level*", LEVELS, key="enroll_level")
            subject = st.selectbox("Subject*", SUBJECTS_BY_LEVEL[level], key="enroll_subject")
        with col2:
            mode = st.selectbox("Learning Mode*", LEARNING_MODES, key="enroll_mode")
            start_month = month_year_picker("Start", "enroll_start")
        
        monthly_fee = get_subject_price(level, mode)
        st.markdown(f"""
        <div style="margin-top: 4px; padding: 12px; background-color: {OFF_WHITE}; border-radius: 8px; border: 1px solid {CARD_BORDER};">
            <span style="color: {MAROON_TEXT}; font-size: 14px;">Monthly Fee for this subject: </span>
            <span style="color: {MAROON}; font-size: 22px; font-weight: bold;">${monthly_fee:,.2f}</span>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Enroll Student", use_container_width=True):
            if selected_label == "Select student...":
                st.error("Please select a student.")
            else:
                student_number = student_label_to_id.get(selected_label, "")
                student_name = selected_label.split(" (")[0]
                
                df_enroll = load_data("Subject Enrollments")
                already_active = False
                if not df_enroll.empty:
                    df_enroll.columns = df_enroll.columns.astype(str).str.strip()
                    required = {"Student Number", "Subject", "Level", "Status"}
                    if required.issubset(df_enroll.columns):
                        existing = df_enroll[
                            (df_enroll["Student Number"].astype(str).str.strip() == student_number) &
                            (df_enroll["Subject"].astype(str).str.strip().str.lower() == subject.strip().lower()) &
                            (df_enroll["Level"].astype(str).str.strip() == level) &
                            (df_enroll["Status"].astype(str).str.strip() == "Active")
                        ]
                        already_active = not existing.empty
                
                if already_active:
                    st.error(f"{student_name} already has an active enrollment in {subject} ({level}). Use 'Manage / Drop Enrollments' to change it.")
                else:
                    success = write_data("Subject Enrollments", {
                        "Timestamp": str(datetime.now()),
                        "Student Number": student_number,
                        "Student Name": student_name,
                        "Level": level,
                        "Subject": subject,
                        "Mode": mode,
                        "Monthly Fee": monthly_fee,
                        "Start Month": start_month,
                        "Status": "Active",
                        "Exit Month": "",
                    })
                    if success:
                        st.success(f"{student_name} enrolled in {subject} ({level}, {mode}) at ${monthly_fee:,.2f}/month, starting {start_month}.")
                    else:
                        st.error("Failed to save enrollment.")
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="dash-card"><div class="dash-card-header">Current Enrollments</div><div class="dash-card-body">', unsafe_allow_html=True)
        
        manage_label = st.selectbox("Student", student_display_list, key="manage_enroll_student")
        
        if manage_label != "Select student...":
            manage_student_number = student_label_to_id.get(manage_label, "")
            df_enroll = load_data("Subject Enrollments")
            
            if not df_enroll.empty:
                df_enroll.columns = df_enroll.columns.astype(str).str.strip()
                student_enrollments = find_by_student_number(df_enroll, manage_student_number)
                
                if not student_enrollments.empty:
                    display_cols = [c for c in ["Level", "Subject", "Mode", "Monthly Fee", "Start Month", "Status", "Exit Month"] if c in student_enrollments.columns]
                    st.dataframe(student_enrollments[display_cols], use_container_width=True, hide_index=True)
                    
                    active_rows = student_enrollments[student_enrollments["Status"].astype(str).str.strip() == "Active"] if "Status" in student_enrollments.columns else student_enrollments.iloc[0:0]
                    
                    if not active_rows.empty:
                        st.markdown("---")
                        st.markdown("**Drop a subject:**")
                        subject_options = [f"{r['Subject']} ({r['Level']}, {r['Mode']})" for _, r in active_rows.iterrows()]
                        subject_to_row_idx = {opt: idx for opt, idx in zip(subject_options, active_rows.index)}
                        
                        drop_choice = st.selectbox("Subject to drop", subject_options, key="drop_choice")
                        drop_month = month_year_picker("Effective", "drop_month")
                        
                        if st.button("Drop Subject", use_container_width=True):
                            row_idx = subject_to_row_idx[drop_choice] + 2
                            ok = True
                            ok &= update_cell("Subject Enrollments", row_idx, df_enroll.columns.get_loc("Status") + 1, "Dropped")
                            ok &= update_cell("Subject Enrollments", row_idx, df_enroll.columns.get_loc("Exit Month") + 1, drop_month)
                            if ok:
                                st.success(f"Dropped {drop_choice} effective {drop_month}.")
                                st.rerun()
                            else:
                                st.error("Failed to update the enrollment.")
                    else:
                        st.info("No active enrollments to drop.")
                else:
                    st.info("This student has no subject enrollments yet.")
            else:
                st.info("No enrollments recorded yet.")
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="dash-card"><div class="dash-card-header">Monthly Fee per Subject (USD)</div><div class="dash-card-body">', unsafe_allow_html=True)
        
        html = '<table style="width:100%; border-collapse:collapse;">'
        html += f'<tr style="background-color:{MAROON}; color:{WHITE};">'
        html += '<th style="padding:12px;">Level</th><th style="padding:12px;">Learning Mode</th><th style="padding:12px;">Fee per Subject / Month</th></tr>'
        row_num = 0
        for level in LEVELS:
            for mode in LEARNING_MODES:
                price = get_subject_price(level, mode)
                bg = FAINT_MAROON if row_num % 2 == 0 else WHITE
                html += f'<tr>'
                html += f'<td style="padding:12px; font-weight:bold; color:{MAROON_TEXT}; background-color:{bg};">{level}</td>'
                html += f'<td style="padding:12px; color:{MAROON_TEXT}; background-color:{bg};">{mode}</td>'
                html += f'<td style="padding:12px; color:{MAROON}; font-weight:bold; font-size:16px; background-color:{bg};">${price:,.2f}</td>'
                html += '</tr>'
                row_num += 1
        html += '</table>'
        st.markdown(html, unsafe_allow_html=True)
        
        st.markdown(f"""
        <p style="font-size:13px; color:{SKY_BLUE}; margin-top:12px;">
        A student's total monthly fee is the sum of the per-subject fee across every subject they're actively enrolled in — e.g. two O Level subjects on One-on-One is ${get_subject_price("O Level", "One-on-One") * 2:,.2f}/month.
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown('</div></div>', unsafe_allow_html=True)

def admin_fees_owing():
    st.markdown("## Fees Owing")
    
    df_enroll = load_data("Subject Enrollments")
    if df_enroll.empty or "Student Number" not in df_enroll.columns:
        st.info("No subject enrollments recorded yet — nothing to calculate.")
        return
    df_enroll.columns = df_enroll.columns.astype(str).str.strip()
    
    available_months = get_available_months(["Subject Enrollments", "Fee Payments"])
    current_month_str = f"{MONTH_NAMES[date.today().month - 1]} {date.today().year}"
    if current_month_str not in available_months:
        available_months = [current_month_str] + available_months
    
    selected_month = st.selectbox("Month", sorted(available_months, key=month_sort_key, reverse=True), key="owing_month")
    
    df_payments = load_data("Fee Payments")
    if not df_payments.empty:
        df_payments.columns = df_payments.columns.astype(str).str.strip()
    df_payments_month = filter_by_month(df_payments, selected_month) if not df_payments.empty else pd.DataFrame()
    
    student_numbers = df_enroll["Student Number"].astype(str).str.strip().unique()
    rows = []
    for sid in student_numbers:
        expected = compute_expected_monthly_fee(df_enroll, sid, selected_month)
        if expected <= 0:
            continue  # not enrolled in anything billable this month
        
        student_rows = df_enroll[df_enroll["Student Number"].astype(str).str.strip() == sid]
        student_name = str(student_rows.iloc[0].get("Student Name", "")).strip()
        
        paid = 0.0
        if not df_payments_month.empty and "Student Number" in df_payments_month.columns:
            paid = safe_sum(df_payments_month[df_payments_month["Student Number"].astype(str).str.strip() == sid], "Amount Paid")
        
        owing = round(expected - paid, 2)
        rows.append({
            "Student Number": sid,
            "Student Name": student_name,
            "Expected": expected,
            "Paid": paid,
            "Owing": owing,
        })
    
    if not rows:
        st.info(f"No billable enrollments found for {selected_month}.")
        return
    
    df_report = pd.DataFrame(rows).sort_values("Owing", ascending=False)
    
    total_expected = df_report["Expected"].sum()
    total_paid = df_report["Paid"].sum()
    total_owing = df_report["Owing"].clip(lower=0).sum()
    
    st.markdown(f"""
    <div class="dash-card">
        <div class="dash-card-header">Summary<span class="term-badge">{selected_month}</span></div>
        <div class="dash-card-body">
            <div class="metric-grid metric-grid-3">
                <div class="metric-card"><div class="metric-value">${total_expected:,.0f}</div><div class="metric-label">Expected</div></div>
                <div class="metric-card"><div class="metric-value" style="color:{GREEN};">${total_paid:,.0f}</div><div class="metric-label">Paid</div></div>
                <div class="metric-card" style="border:2px solid {RED if total_owing > 0 else GREEN};"><div class="metric-value" style="color:{RED if total_owing > 0 else GREEN};">${total_owing:,.0f}</div><div class="metric-label">Total Owing</div></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="dash-card"><div class="dash-card-header">Per-Student Breakdown</div><div class="dash-card-body">', unsafe_allow_html=True)
    
    html = '<table style="width:100%; border-collapse:collapse; font-size:14px;">'
    html += f'<tr style="background-color:{MAROON}; color:{WHITE};">'
    for col in ["Student Number", "Student Name", "Expected", "Paid", "Owing"]:
        html += f'<th style="padding:10px 12px; text-align:left;">{col}</th>'
    html += '</tr>'
    for i, (_, row) in enumerate(df_report.iterrows()):
        bg = FAINT_MAROON if i % 2 == 0 else WHITE
        owing_color = RED if row["Owing"] > 0 else GREEN
        html += f'<tr>'
        html += f'<td style="padding:10px 12px; background-color:{bg}; color:{MAROON_TEXT};">{row["Student Number"]}</td>'
        html += f'<td style="padding:10px 12px; background-color:{bg}; color:{MAROON_TEXT};">{row["Student Name"]}</td>'
        html += f'<td style="padding:10px 12px; background-color:{bg}; color:{MAROON_TEXT};">${row["Expected"]:,.2f}</td>'
        html += f'<td style="padding:10px 12px; background-color:{bg}; color:{MAROON_TEXT};">${row["Paid"]:,.2f}</td>'
        html += f'<td style="padding:10px 12px; background-color:{bg}; color:{owing_color}; font-weight:bold;">${row["Owing"]:,.2f}</td>'
        html += '</tr>'
    html += '</table>'
    st.markdown(html, unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

def admin_record_fee():
    st.markdown("## Record Fee Payment")
    
    st.markdown('<div class="dash-card"><div class="dash-card-header">Payment Details</div><div class="dash-card-body">', unsafe_allow_html=True)
    
    df_students = load_data("Students")
    if not df_students.empty:
        df_students.columns = df_students.columns.astype(str).str.strip()
    student_display_list, student_label_to_id = build_student_dropdown(df_students)
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_label = st.selectbox("Student Name*", student_display_list)
        payment_date = st.date_input("Payment Date", value=date.today())
        month = month_year_picker("Billing", "fee_payment")
    
    with col2:
        amount = st.number_input("Amount Paid*", min_value=0.0, step=10.0, format="%.2f")
        payment_method = st.selectbox("Payment Method", ["Cash", "EFT", "Mobile Money", "Cheque", "Other"])
    
    if st.button("Record Payment", use_container_width=True):
        if selected_label == "Select student...":
            st.error("Please select a student.")
        elif amount <= 0:
            st.error("Please enter an amount.")
        else:
            student_number = student_label_to_id.get(selected_label, "")
            student_name = selected_label.split(" (")[0]
            # Headers expected in the "Fee Payments" tab:
            # Timestamp | Student Number | Name of Student | Date | Month | Amount Paid | Payment Method
            success = write_data("Fee Payments", {
                "Timestamp": str(datetime.now()),
                "Student Number": student_number,
                "Name of Student": student_name,
                "Date": str(payment_date),
                "Month": month,
                "Amount Paid": float(amount),
                "Payment Method": payment_method,
            })
            if success:
                st.success(f"Payment of ${amount:,.2f} recorded for {student_name}!")
            else:
                st.error("Failed to record payment.")
    
    st.markdown('</div></div>', unsafe_allow_html=True)

def admin_enter_performance():
    st.markdown("## Enter Student Performance")
    
    st.markdown('<div class="dash-card"><div class="dash-card-header">Performance Entry</div><div class="dash-card-body">', unsafe_allow_html=True)
    
    df_students = load_data("Students")
    if not df_students.empty:
        df_students.columns = df_students.columns.astype(str).str.strip()
    student_display_list, student_label_to_id = build_student_dropdown(df_students)
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_label = st.selectbox("Student Name*", student_display_list)
        month = month_year_picker("Result", "perf_entry")
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
    
    student_number = student_label_to_id.get(selected_label, "")
    student_name = selected_label.split(" (")[0] if selected_label != "Select student..." else ""
    student_dob = ""
    if student_number and not df_students.empty:
        match = find_by_student_number(df_students, student_number, name_fallback=student_name)
        if not match.empty:
            student_dob = str(match.iloc[0].get("Date of Birth", ""))
    
    if st.button("Save Result", use_container_width=True):
        if selected_label == "Select student...":
            st.error("Please select a student.")
        elif not subject:
            st.error("Please enter a subject.")
        else:
            # One mark per student/month/subject: check for an existing row
            # before writing, so re-saving a corrected mark updates it in
            # place instead of appending a duplicate. Matched by Student
            # Number now — exact, no risk of same-name collisions.
            df_perf = load_data("Performance")
            existing_row_idx = None
            if not df_perf.empty:
                df_perf.columns = df_perf.columns.astype(str).str.strip()
                if "Student Number" in df_perf.columns and {"Month", "Subject"}.issubset(df_perf.columns):
                    match = df_perf[
                        (df_perf["Student Number"].astype(str).str.strip() == student_number) &
                        (df_perf["Month"].astype(str).str.strip() == month.strip()) &
                        (df_perf["Subject"].astype(str).str.strip().str.lower() == subject.strip().lower())
                    ]
                    if not match.empty:
                        existing_row_idx = match.index[0] + 2  # header row + 0-index offset

            if existing_row_idx is not None:
                ok = True
                ok &= update_cell("Performance", existing_row_idx, df_perf.columns.get_loc("Mark") + 1, mark)
                ok &= update_cell("Performance", existing_row_idx, df_perf.columns.get_loc("Grade") + 1, auto_grade)
                if "Comment" in df_perf.columns:
                    ok &= update_cell("Performance", existing_row_idx, df_perf.columns.get_loc("Comment") + 1, comment)
                if "Date of Birth" in df_perf.columns:
                    ok &= update_cell("Performance", existing_row_idx, df_perf.columns.get_loc("Date of Birth") + 1, student_dob)
                if ok:
                    st.success(f"Existing result updated for {student_name} - {subject} ({month}): {mark}% ({auto_grade})")
                else:
                    st.error("Failed to update the existing result.")
            else:
                success = write_data("Performance", {
                    "Student Number": student_number,
                    "Student Name": student_name,
                    "Date of Birth": student_dob,
                    "Month": month,
                    "Subject": subject,
                    "Mark": mark,
                    "Grade": auto_grade,
                    "Comment": comment,
                })
                if success:
                    st.success(f"Result saved for {student_name} - {subject}: {mark}% ({auto_grade})")
                else:
                    st.error("Failed to save result.")
    
    st.markdown('</div></div>', unsafe_allow_html=True)

def admin_mark_attendance():
    st.markdown("## Mark Attendance")
    
    tab1, tab2 = st.tabs(["Attendance View (5-Day Grid)", "Record Absences"])
    
    df_students = load_data("Students")
    if not df_students.empty:
        df_students.columns = df_students.columns.astype(str).str.strip()
    student_display_list, student_label_to_id = build_student_dropdown(df_students)
    
    with tab1:
        st.markdown('<div class="dash-card"><div class="dash-card-header">Update Attendance Grid</div><div class="dash-card-body">', unsafe_allow_html=True)
        
        if not df_students.empty:
            df_att = load_data("Attendance View")
            
            st.markdown("**Select student and date to update:**")
            selected_label = st.selectbox("Student", student_display_list, key="att_student")
            student_number = student_label_to_id.get(selected_label, "")
            student_name = selected_label.split(" (")[0] if selected_label != "Select student..." else ""
            
            date_cols = []
            if not df_att.empty:
                df_att.columns = df_att.columns.astype(str).str.strip()
                date_cols = [c for c in df_att.columns if c not in ("Student Name", "Student Number")]
            
            if date_cols:
                selected_date = st.selectbox("Date", date_cols, key="att_date")
                status = st.radio("Status", ["Present", "Absent"], horizontal=True)
                
                if st.button("Update Attendance"):
                    if selected_label == "Select student...":
                        st.warning("Please select a student.")
                    elif not df_att.empty:
                        row_match = find_by_student_number(df_att, student_number, name_fallback=student_name)
                        if not row_match.empty:
                            row_idx = row_match.index[0] + 2
                            col_idx = list(df_att.columns).index(selected_date) + 1
                            update_cell("Attendance View", row_idx, col_idx, status)
                            st.success(f"Updated {student_name} - {selected_date}: {status}")
                            st.rerun()
                        else:
                            st.error(f"No Attendance View row found for {student_name}.")
            else:
                st.info("No date columns found in Attendance View.")
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="dash-card"><div class="dash-card-header">Record Absent Students</div><div class="dash-card-body">', unsafe_allow_html=True)
        
        st.info("Use this to record which students were absent on a specific date.")
        
        absence_date = st.date_input("Date", value=date.today(), key="absence_date")
        
        if not df_students.empty:
            absent_labels = st.multiselect("Absent Students", [l for l in student_display_list if l != "Select student..."])
            absent_names = [l.split(" (")[0] for l in absent_labels]
            absent_numbers = [student_label_to_id.get(l, "") for l in absent_labels]
            
            if st.button("Record Absences"):
                if absent_labels:
                    write_data("Attendance", {
                        "Timestamp": str(datetime.now()),
                        "Date": str(absence_date),
                        "Absent Students": ", ".join(absent_names),
                        "Absent Student Numbers": ", ".join(absent_numbers),
                    })
                    st.success(f"Recorded {len(absent_labels)} absent student(s) on {absence_date}")
                else:
                    st.warning("No students selected.")
        
        st.markdown('</div></div>', unsafe_allow_html=True)

def admin_record_expense():
    st.markdown("## Record Expense")
    
    st.markdown('<div class="dash-card"><div class="dash-card-header">Expense Details</div><div class="dash-card-body">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        expense_date = st.date_input("Date", value=date.today(), key="exp_date")
        month = month_year_picker("Expense", "expense")
        category = st.selectbox("Category", [
            "Utilities", "Supplies", "Maintenance", "Food", "Transport",
            "Printing", "Events", "Salaries", "Other"
        ])
    
    with col2:
        description = st.text_area("Expense Description")
        amount = st.number_input("Amount*", min_value=0.0, step=10.0, key="exp_amount")
    
    if st.button("Record Expense", use_container_width=True):
        if amount <= 0:
            st.error("Please enter an amount.")
        else:
            # Headers expected in the "Expenses" tab:
            # Timestamp | Date | Description | Amount | Month | Category
            success = write_data("Expenses", {
                "Timestamp": str(datetime.now()),
                "Date": str(expense_date),
                "Description": description,
                "Amount": amount,
                "Month": month,
                "Category": category,
            })
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
    
    with col2:
        description = st.text_area("Income Description", key="inc_desc")
        amount = st.number_input("Amount*", min_value=0.0, step=10.0, key="inc_amount")
    
    if st.button("Record Income", use_container_width=True):
        if amount <= 0:
            st.error("Please enter an amount.")
        else:
            success = write_data("Other Income", {
                "Timestamp": str(datetime.now()),
                "Date": str(income_date),
                "Income Description": description,
                "Amount": amount,
            })
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
        month = month_year_picker("Salary", "salary")
    
    with col2:
        recipient = st.selectbox("Recipient", salary_recipients)
        amount = st.number_input("Amount ($)*", min_value=0.0, step=50.0, key="sal_amount")
        st.text_input("Percentage", value="5%", disabled=True, key="sal_pct")
    
    if st.button("Record Salary Payment", use_container_width=True):
        if amount <= 0:
            st.error("Please enter an amount.")
        else:
            success = write_data("Salaries", {
                "Date": str(salary_date),
                "Month": month,
                "Recipient": recipient,
                "Percentage": "5%",
                "Amount": amount,
            })
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

def admin_account_settings():
    st.markdown("## Account Settings")
    
    st.markdown('<div class="dash-card"><div class="dash-card-header">Change Your Password</div><div class="dash-card-body">', unsafe_allow_html=True)
    st.markdown(f"**Logged in as:** {st.session_state.username}")
    
    current_password = st.text_input("Current Password", type="password", key="admin_current_pw")
    new_password = st.text_input("New Password", type="password", key="admin_new_pw")
    confirm_password = st.text_input("Confirm New Password", type="password", key="admin_confirm_pw")
    
    if st.button("Update Password", use_container_width=True, key="admin_update_pw_btn"):
        if not current_password or not new_password or not confirm_password:
            st.error("Please fill in all three fields.")
        elif new_password != confirm_password:
            st.error("New password and confirmation don't match.")
        elif len(new_password) < 6:
            st.error("New password should be at least 6 characters.")
        else:
            df_admins = load_data("Admin Logins")
            if df_admins.empty:
                st.error("Unable to load admin login data.")
            else:
                df_admins.columns = df_admins.columns.astype(str).str.strip()
                my_row = df_admins[df_admins["Username"].astype(str).str.strip() == st.session_state.username.strip()]
                if my_row.empty:
                    st.error("Could not find your admin login record.")
                elif not verify_password(current_password, my_row.iloc[0].get("Password", "")):
                    st.error("Current password is incorrect.")
                else:
                    row_idx = my_row.index[0] + 2
                    pw_col_idx = df_admins.columns.get_loc("Password") + 1
                    success = update_cell("Admin Logins", row_idx, pw_col_idx, hash_password(new_password))
                    if success:
                        st.success("Password updated. Use your new password next time you log in.")
                    else:
                        st.error("Failed to update password.")
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="dash-card"><div class="dash-card-header">Add Another Admin Account</div><div class="dash-card-body">', unsafe_allow_html=True)
    
    new_admin_username = st.text_input("New Admin Username", key="new_admin_user")
    new_admin_password = st.text_input("New Admin Password", type="password", key="new_admin_pw")
    
    if st.button("Create Admin Account", use_container_width=True, key="create_admin_btn"):
        if not new_admin_username.strip() or not new_admin_password:
            st.error("Please fill in both fields.")
        elif len(new_admin_password) < 6:
            st.error("Password should be at least 6 characters.")
        else:
            df_admins = load_data("Admin Logins")
            taken = False
            if not df_admins.empty and "Username" in df_admins.columns:
                df_admins.columns = df_admins.columns.astype(str).str.strip()
                taken = not df_admins[df_admins["Username"].astype(str).str.strip().str.lower() == new_admin_username.strip().lower()].empty
            
            if taken:
                st.error(f"Username '{new_admin_username.strip()}' is already taken.")
            else:
                success = write_data("Admin Logins", {
                    "Username": new_admin_username.strip(),
                    "Password": hash_password(new_admin_password),
                })
                if success:
                    st.success(f"Admin account '{new_admin_username.strip()}' created.")
                else:
                    st.error("Failed to create admin account.")
    
    st.markdown('</div></div>', unsafe_allow_html=True)

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
