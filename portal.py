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
    initial_sidebar_state="collapsed"
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
# CSS - ZEBRA ACADEMY MAROON THEME
# ============================================================
def inject_css():
    st.markdown(f"""
    <style>
        /* Force Light Theme */
        @media (prefers-color-scheme: dark) {{
            :root {{
                --background-color: {OFF_WHITE};
                --text-color: {MAROON_TEXT};
            }}
        }}
        
        /* Global Font */
        * {{
            font-family: 'Georgia', 'Times New Roman', serif !important;
        }}
        
        /* Material Icons Fix */
        [style*="Material Symbols"] {{
            font-family: 'Material Symbols Rounded', 'Material Symbols Outlined',
                         'Material Symbols Sharp', sans-serif !important;
        }}
        
        /* Button Text Fix */
        .stButton > button p, .stButton > button span, .stButton > button div {{
            color: {WHITE} !important;
        }}
        
        /* Tab Text Fix */
        .stTabs [aria-selected="true"] p, .stTabs [aria-selected="true"] span {{
            color: {WHITE} !important;
        }}
        
        /* Main Container */
        [data-testid="stAppViewContainer"] {{
            background-color: {OFF_WHITE};
        }}
        
        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {MAROON};
            min-width: 300px !important;
            max-width: 300px !important;
        }}
        [data-testid="stSidebar"] * {{
            color: {WHITE} !important;
        }}
        [data-testid="stSidebar"] button {{
            background-color: {SKY_BLUE} !important;
            border: none !important;
            border-radius: 6px !important;
            color: {WHITE} !important;
        }}
        [data-testid="stSidebar"] button:hover {{
            background-color: {MAROON_DARK} !important;
        }}
        /* Hide sidebar collapse */
        [data-testid="collapsedControl"] {{
            display: none;
        }}
        
        /* Top Banner */
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
            color: {WHITE};
            margin: 0;
            font-size: 28px;
        }}
        
        /* Login Container */
        .login-container {{
            max-width: 450px;
            margin: 0 auto;
            background: {WHITE};
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            border: 1px solid {CARD_BORDER};
        }}
        
        /* Bottom Footer */
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
        
        /* Dashboard Cards */
        .dash-card {{
            background: {WHITE};
            border-radius: 10px;
            border: 1px solid {CARD_BORDER};
            margin-bottom: 20px;
            overflow: hidden;
        }}
        .dash-card-header {{
            background-color: {MAROON};
            color: {WHITE};
            padding: 14px 20px;
            font-size: 16px;
            font-weight: bold;
        }}
        .dash-card-body {{
            padding: 20px;
        }}
        
        /* Metric Cards */
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
        
        /* Tables */
        .dash-card table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .dash-card th {{
            background-color: {MAROON};
            color: {WHITE};
            padding: 10px 15px;
            text-align: left;
        }}
        .dash-card td {{
            padding: 10px 15px;
            border-bottom: 1px solid {CARD_BORDER};
        }}
        .dash-card tr:nth-child(even) {{
            background-color: {CARD_ALT_ROW};
        }}
        
        /* Positive/Negative */
        .positive {{
            color: {GREEN};
            font-weight: bold;
        }}
        .negative {{
            color: {RED};
            font-weight: bold;
        }}
        
        /* Profile Avatar */
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
        
        /* Hide Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        /* File upload fix */
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
        # Try Streamlit Cloud secrets first
        creds_dict = dict(st.secrets["connections"]["gsheet"])
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            creds_dict,
            scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        )
    except Exception:
        # Fallback to local credentials.json for development
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
        
        # --- Student Login ---
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
        
        # --- Admin Login ---
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
    
    # Bottom footer
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
        
        # Profile photo or initials
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
        
        # Navigation
        pages = ["My Dashboard", "My Performance", "My Fees", "My Attendance", "Profile Settings"]
        for page in pages:
            if st.button(page, key=f"nav_{page}", use_container_width=True):
                st.session_state.current_page = page
                st.rerun()
        
        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.rerun()
    
    # Main content
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
    
    # Load student details
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
    
    # Group by Term
    terms = my_perf["Term"].unique()
    for term in sorted(terms, reverse=True):
        term_data = my_perf[my_perf["Term"] == term]
        st.markdown(f"### {term}")
        
        # Build display table
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
# ADMIN DASHBOARD
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
            "Mark Attendance",
            "Record Expense",
            "Record Other Income",
            "Salary Payments",
            "All Students",
            "Financial Summary",
        ]
        
        for page in admin_pages:
            if st.button(page, key=f"admin_{page}", use_container_width=True):
                st.session_state.admin_page = page
                st.rerun()
        
        st.markdown("---")
        if st.button("Logout", key="admin_logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.rerun()
    
    # Route to correct page
    page = st.session_state.admin_page
    if page == "Overview":
        admin_overview()
    elif page == "Register Student":
        admin_register_student()
    elif page == "Record Fee Payment":
        admin_record_fee()
    elif page == "Enter Performance":
        admin_enter_performance()
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
    elif page == "Financial Summary":
        admin_financial_summary()

def admin_overview():
    st.markdown("## Admin Overview")
    
    df_students = load_data("Students")
    df_payments = load_data("Fee Payments")
    df_expenses = load_data("Expenses")
    df_other_income = load_data("Other Income")
    
    total_students = len(df_students) if not df_students.empty else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_students}</div>
            <div class="metric-label">Total Students</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_fees = 0
        if not df_payments.empty:
            df_payments.columns = df_payments.columns.astype(str).str.strip()
            total_fees = df_payments["Amount Paid"].astype(float).sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${total_fees:,.0f}</div>
            <div class="metric-label">Fees Collected</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_exp = 0
        if not df_expenses.empty:
            df_expenses.columns = df_expenses.columns.astype(str).str.strip()
            total_exp = df_expenses["Amount"].astype(float).sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${total_exp:,.0f}</div>
            <div class="metric-label">Total Expenses</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        other_inc = 0
        if not df_other_income.empty:
            df_other_income.columns = df_other_income.columns.astype(str).str.strip()
            other_inc = df_other_income["Amount"].astype(float).sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${other_inc:,.0f}</div>
            <div class="metric-label">Other Income</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Net position
    net = total_fees + other_inc - total_exp
    color = GREEN if net >= 0 else RED
    st.markdown(f"""
    <div class="metric-card" style="max-width: 300px; margin: 20px auto;">
        <div class="metric-value" style="color: {color};">${net:,.0f}</div>
        <div class="metric-label">Net Position</div>
    </div>
    """, unsafe_allow_html=True)

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
        mark = st.number_input("Mark*", min_value=0, max_value=100, step=1)
        grade = st.selectbox("Grade", ["A+", "A", "B", "C", "D", "E", "F"])
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
                student_name, student_class, term, subject, mark, grade, comment
            ])
            if success:
                st.success(f"Result saved for {student_name} - {subject}!")
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
    
    # Show salary summary
    st.markdown('<div class="dash-card"><div class="dash-card-header">Salary Summary</div><div class="dash-card-body">', unsafe_allow_html=True)
    df_salaries = load_data("Salaries")
    if not df_salaries.empty:
        df_salaries.columns = df_salaries.columns.astype(str).str.strip()
        st.dataframe(df_salaries, use_container_width=True, hide_index=True)
        
        st.markdown("#### Total per Recipient")
        for recipient in salary_recipients:
            rec_data = df_salaries[df_salaries["Recipient"].astype(str).str.strip() == recipient]
            total = rec_data["Amount"].astype(float).sum() if not rec_data.empty else 0
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

def admin_financial_summary():
    st.markdown("## Financial Summary")
    
    st.markdown("### Profit Distribution")
    st.markdown("*Based on total income (Fees + Other Income) minus total expenses*")
    
    df_payments = load_data("Fee Payments")
    df_other_income = load_data("Other Income")
    df_expenses = load_data("Expenses")
    
    total_fees = 0
    total_other = 0
    total_expenses = 0
    
    if not df_payments.empty:
        df_payments.columns = df_payments.columns.astype(str).str.strip()
        total_fees = df_payments["Amount Paid"].astype(float).sum()
    
    if not df_other_income.empty:
        df_other_income.columns = df_other_income.columns.astype(str).str.strip()
        total_other = df_other_income["Amount"].astype(float).sum()
    
    if not df_expenses.empty:
        df_expenses.columns = df_expenses.columns.astype(str).str.strip()
        total_expenses = df_expenses["Amount"].astype(float).sum()
    
    total_income = total_fees + total_other
    gross_profit = total_income - total_expenses
    
    investments = gross_profit * 0.10
    salaries = gross_profit * 0.20
    tithe = gross_profit * 0.10
    alter = gross_profit * 0.05
    operations = gross_profit * 0.10
    net_profit = gross_profit * 0.45
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${total_income:,.0f}</div>
            <div class="metric-label">Total Income</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${total_expenses:,.0f}</div>
            <div class="metric-label">Total Expenses</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        color = GREEN if gross_profit >= 0 else RED
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {color};">${gross_profit:,.0f}</div>
            <div class="metric-label">Gross Profit</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Distribution Breakdown")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${investments:,.0f}</div>
            <div class="metric-label">Investments (10%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${salaries:,.0f}</div>
            <div class="metric-label">Salaries (20%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${tithe:,.0f}</div>
            <div class="metric-label">Tithe (10%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${alter:,.0f}</div>
            <div class="metric-label">Alter (5%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${operations:,.0f}</div>
            <div class="metric-label">Operations (10%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {GREEN};">${net_profit:,.0f}</div>
            <div class="metric-label">Net Profit (45%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Salary split
    st.markdown("---")
    st.markdown("### Salary Split (20% / 4 = 5% each)")
    
    per_person = salaries / 4
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${per_person:,.0f}</div>
            <div class="metric-label">Mr Kawonde (5%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${per_person:,.0f}</div>
            <div class="metric-label">Mrs Kawonde (5%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${per_person:,.0f}</div>
            <div class="metric-label">Nextvantage Analytics (5%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${per_person:,.0f}</div>
            <div class="metric-label">Miss Mutasvu (5%)</div>
        </div>
        """, unsafe_allow_html=True)

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
