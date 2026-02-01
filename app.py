import streamlit as st
import utils
import export_utils
import secrets_utils
import profile_utils
import json
import os
import datetime
from io import BytesIO

# --- Page Config ---
st.set_page_config(page_title="AI Cover Letter Generator v1.1", layout="wide", page_icon="CL")

# --- Custom CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* Global font */
html, body, [class*="css"] {
    font-family: 'Inter', 'system-ui', -apple-system, 'Segoe UI', sans-serif;
}

/* Monospace sub-labels for developer-grade feel */
.mono-label {
    font-family: 'JetBrains Mono', 'SF Mono', 'Fira Code', 'Consolas', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    color: #64748B;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 0.35rem;
}

/* Main background */
.stApp, [data-testid="stAppViewContainer"] {
    background-color: #F4F7FA;
}

/* Remove heavy shadows, micro-round all containers */
div[data-testid="stVerticalBlock"] > div,
div[data-testid="stHorizontalBlock"] > div,
.stForm, .stExpander {
    border-radius: 6px !important;
}

/* Buttons: flat with border, no gradient */
.stButton > button {
    border: 1px solid #D1D9E6 !important;
    border-radius: 4px !important;
    background: #FFFFFF !important;
    color: #1E293B !important;
    font-weight: 500 !important;
    box-shadow: none !important;
    transition: background 0.15s, border-color 0.15s;
}
.stButton > button:hover {
    background: #EAEFF5 !important;
    border-color: #4A6FA5 !important;
}

/* Primary buttons */
.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"] {
    background: #4A6FA5 !important;
    color: #FFFFFF !important;
    border: 1px solid #4A6FA5 !important;
}
.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="stBaseButton-primary"]:hover {
    background: #3D5F8F !important;
    border-color: #3D5F8F !important;
}

/* Download buttons: outlined/secondary */
.stDownloadButton > button {
    border: 1px solid #D1D9E6 !important;
    border-radius: 4px !important;
    background: #FFFFFF !important;
    color: #4A6FA5 !important;
    font-weight: 500 !important;
    box-shadow: none !important;
}
.stDownloadButton > button:hover {
    background: #EAEFF5 !important;
    border-color: #4A6FA5 !important;
}

/* Input fields: transparent bg, bottom-border style */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stDateInput > div > div > input {
    background: transparent !important;
    border: none !important;
    border-bottom: 1.5px solid #C8D1DC !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    padding-left: 2px !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stDateInput > div > div > input:focus {
    border-bottom: 1.5px solid #4A6FA5 !important;
    box-shadow: 0 2px 8px rgba(74, 111, 165, 0.15) !important;
    outline: none !important;
}
.stTextInput > div > div > input:hover,
.stTextArea > div > div > textarea:hover,
.stDateInput > div > div > input:hover {
    border-bottom-color: #94A3B8 !important;
}
/* Selectbox keeps light stroke */
.stSelectbox > div > div {
    border: 1px solid #D1D9E6 !important;
    border-radius: 4px !important;
    box-shadow: none !important;
    background: transparent !important;
}
.stSelectbox > div > div:focus-within {
    border-color: #4A6FA5 !important;
    box-shadow: 0 0 0 2px rgba(74, 111, 165, 0.12) !important;
}

/* --- Secure Well (API Key area) --- */
.secure-well {
    background: #E4EAF1;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 1rem 1.1rem;
    margin-top: 0.5rem;
    margin-bottom: 0.75rem;
    position: relative;
}
.secure-well::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    border-radius: 6px;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.04);
    pointer-events: none;
}
.secure-well-label {
    font-family: 'JetBrains Mono', 'SF Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    color: #64748B;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.secure-well-label .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #4A6FA5;
    display: inline-block;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #EAEFF5 !important;
    border-right: 1px solid #D1D9E6 !important;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    padding-top: 0.5rem;
}

/* Tabs: clean underline style */
.stTabs [data-baseweb="tab-list"] {
    gap: 0px;
    border-bottom: 1px solid #D1D9E6;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 0px !important;
    background: transparent !important;
    border-bottom: 2px solid transparent;
    padding: 0.5rem 1.25rem;
    font-weight: 500;
    color: #64748B;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    border-bottom: 2px solid #4A6FA5;
    color: #1E293B;
    font-weight: 600;
}
.stTabs [data-baseweb="tab-highlight"] {
    display: none;
}
.stTabs [data-baseweb="tab-border"] {
    display: none;
}

/* Expanders: clean bordered */
.streamlit-expanderHeader {
    border: 1px solid #D1D9E6 !important;
    border-radius: 4px !important;
    background: #FFFFFF !important;
    box-shadow: none !important;
    font-weight: 500;
}
details[data-testid="stExpander"] {
    border: 1px solid #D1D9E6 !important;
    border-radius: 6px !important;
    box-shadow: none !important;
}

/* Typography */
h1 { font-weight: 700 !important; color: #1E293B !important; }
h2 { font-weight: 700 !important; color: #1E293B !important; }
h3 { font-weight: 600 !important; color: #1E293B !important; }
label { font-weight: 400 !important; }

/* Section divider style */
hr {
    border: none !important;
    border-top: 1px solid #D1D9E6 !important;
    margin: 1rem 0 !important;
}

/* Form borders */
[data-testid="stForm"] {
    border: 1px solid #D1D9E6 !important;
    border-radius: 6px !important;
    padding: 1rem !important;
    box-shadow: none !important;
    background: #FFFFFF;
}

/* Style the Streamlit radio as a segmented control */
div[data-testid="stRadio"] > div[role="radiogroup"] {
    display: inline-flex !important;
    flex-direction: row !important;
    gap: 0 !important;
    background: #E2E8F0;
    border-radius: 6px;
    padding: 3px;
}
div[data-testid="stRadio"] > div[role="radiogroup"] > label {
    padding: 6px 18px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: #64748B !important;
    cursor: pointer;
    border-radius: 4px;
    transition: all 0.2s ease;
    margin: 0 !important;
    white-space: nowrap;
    background: transparent !important;
}
div[data-testid="stRadio"] > div[role="radiogroup"] > label[data-checked="true"],
div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
    background: #FFFFFF !important;
    color: #1E293B !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
div[data-testid="stRadio"] > div[role="radiogroup"] > label:not(:has(input:checked)):hover {
    color: #475569 !important;
    background: rgba(255,255,255,0.4) !important;
}
/* Hide the actual radio circle */
div[data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child {
    display: none !important;
}

/* Remove default container shadows */
div[data-testid="stVerticalBlockBorderWrapper"] {
    box-shadow: none !important;
}

/* Section container helper */
.section-box {
    border: 1px solid #D1D9E6;
    border-radius: 6px;
    padding: 1.25rem;
    background: #FFFFFF;
    margin-bottom: 1rem;
}
.section-box h4 {
    margin-top: 0;
    font-weight: 600;
    color: #1E293B;
    font-size: 1rem;
    margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #D1D9E6;
}

/* Danger zone: subtle red border */
.danger-zone {
    border: 1px solid #E2A0A0;
    border-radius: 6px;
    padding: 1.25rem;
    background: #FFF8F8;
    margin-top: 0.5rem;
}
.danger-zone h4 {
    margin-top: 0;
    font-weight: 600;
    color: #9B1C1C;
    font-size: 1rem;
    margin-bottom: 0.75rem;
}

/* Alert boxes: softer */
.stAlert > div {
    border-radius: 4px !important;
    box-shadow: none !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    border-radius: 6px !important;
}
[data-testid="stFileUploader"] > div {
    border-radius: 6px !important;
}

/* ========================================
   Gemini Branding — Accent: #4285F4
   ======================================== */

/* --- Pulse Dot (Live indicator) --- */
@keyframes gemini-pulse {
    0%   { box-shadow: 0 0 0 0 rgba(66, 133, 244, 0.45); }
    70%  { box-shadow: 0 0 0 6px rgba(66, 133, 244, 0); }
    100% { box-shadow: 0 0 0 0 rgba(66, 133, 244, 0); }
}
.live-indicator {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    margin-top: 0.35rem;
    margin-bottom: 0.25rem;
}
.live-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #4285F4;
    display: inline-block;
    animation: gemini-pulse 2s ease-in-out infinite;
}
.live-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    color: #4285F4;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* --- Generate Button: Deep blue + shimmer --- */
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position: 200% center; }
}
.generate-btn-wrap .stButton > button,
.generate-btn-wrap .stButton > button[kind="primary"],
.generate-btn-wrap .stButton > button[data-testid="stBaseButton-primary"] {
    background: #1A3F7A !important;
    color: #FFFFFF !important;
    border: 1px solid #163870 !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.02em;
    padding: 0.6rem 1.5rem !important;
    position: relative;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(26, 63, 122, 0.18) !important;
    transition: box-shadow 0.25s ease;
}
.generate-btn-wrap .stButton > button:hover,
.generate-btn-wrap .stButton > button[kind="primary"]:hover,
.generate-btn-wrap .stButton > button[data-testid="stBaseButton-primary"]:hover {
    background: linear-gradient(
        110deg,
        #1A3F7A 0%,
        #1A3F7A 35%,
        #2A5FAA 45%,
        #4285F4 50%,
        #2A5FAA 55%,
        #1A3F7A 65%,
        #1A3F7A 100%
    ) !important;
    background-size: 200% 100% !important;
    animation: shimmer 1.8s ease-in-out infinite !important;
    border-color: #1A3F7A !important;
    box-shadow: 0 2px 10px rgba(66, 133, 244, 0.25) !important;
    color: #FFFFFF !important;
}

/* Gemini Blue for active states */
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    border-bottom-color: #4285F4 !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stDateInput > div > div > input:focus {
    border-bottom-color: #4285F4 !important;
    box-shadow: 0 2px 8px rgba(66, 133, 244, 0.13) !important;
}
.stSelectbox > div > div:focus-within {
    border-color: #4285F4 !important;
    box-shadow: 0 0 0 2px rgba(66, 133, 244, 0.10) !important;
}
.secure-well-label .dot {
    background: #4285F4 !important;
}
</style>
""", unsafe_allow_html=True)

# --- Session State Init ---
DEFAULTS = {
    "api_key": "",
    "provider": "OpenAI",
    "cover_letter_content": None,
    "docx_data": None,
    "pdf_data": None,
    "latex_data": None,
    "latex_code": None,
    "session_usage": {"tokens": 0, "cost_est": 0.0, "chars": 0},
    "master_password": None,
    "profile_name": "Default",
    "export_formats": ["Word", "PDF", "LaTeX"],
    "gen_metadata": {}
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- Helper: Secrets Loading ---
def get_secrets_status():
    """Loads secrets considering lock state."""
    pwd = st.session_state.master_password
    return secrets_utils.load_secrets(pwd)

def update_exports():
    """Regenerates export files when text is edited."""
    if not st.session_state.gen_metadata:
        return

    meta = st.session_state.gen_metadata
    full_data = {
        "body": st.session_state.cover_letter_content,
        "user_info": meta.get("user_info", {}),
        "date_str": meta.get("date_str", ""),
        "hr_info": meta.get("hr_info", {})
    }

    formats = st.session_state.export_formats
    if "Word" in formats:
        st.session_state.docx_data = export_utils.create_docx(full_data)
    if "PDF" in formats:
        st.session_state.pdf_data = export_utils.create_pdf(full_data)
    if "LaTeX" in formats:
        data, code = export_utils.create_latex(full_data)
        st.session_state.latex_data = data
        st.session_state.latex_code = code

# --- Sidebar ---
with st.sidebar:
    st.title("Status")

    # Profile Selector
    profile_list = profile_utils.list_profiles()
    selected_idx = 0
    if st.session_state.profile_name in profile_list:
        selected_idx = profile_list.index(st.session_state.profile_name)

    new_profile_selection = st.selectbox("Active Profile", profile_list, index=selected_idx)
    if new_profile_selection != st.session_state.profile_name:
        st.session_state.profile_name = new_profile_selection
        st.rerun()

    # Secrets Status
    secrets_status = get_secrets_status()
    if secrets_status["requires_unlock"]:
        st.error("Secrets Locked")
        pwd_input = st.text_input("Unlock Password", type="password", key="sidebar_pwd")
        if st.button("Unlock"):
            st.session_state.master_password = pwd_input
            st.rerun()
    else:
        if st.session_state.api_key:
            st.success("API Key: Active")
        else:
            st.warning("API Key: Missing")

    st.divider()

    # Usage Stats
    st.subheader("Session Usage")
    u = st.session_state.session_usage
    if u['tokens'] > 0:
        st.write(f"**Tokens**: ~{u['tokens']}")
    if u['chars'] > 0:
        st.write(f"**Chars**: ~{u['chars']}")

    st.divider()
    if st.button("Reset Session", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- Main Layout ---
st.title("AI Cover Letter Generator")
tab_generator, tab_settings = st.tabs(["Generator", "Settings"])

# ==========================
# TAB: SETTINGS
# ==========================
with tab_settings:
    st.header("Configuration")

    col_set_1, col_set_2 = st.columns(2)

    # --- Section: API & Keys ---
    with col_set_1:
        st.markdown('<div class="section-box"><h4>AI Provider & Keys</h4></div>', unsafe_allow_html=True)

        # Provider — Segmented Control
        st.markdown('<p class="mono-label">provider</p>', unsafe_allow_html=True)

        providers_list = ["OpenAI", "Google Gemini"]
        current_prov_idx = 0 if st.session_state.provider == "OpenAI" else 1

        # Radio styled as segmented control via CSS
        provider = st.radio("Provider", providers_list,
                          index=current_prov_idx,
                          horizontal=True, label_visibility="collapsed")
        st.session_state.provider = provider

        prov_key = "OpenAI" if provider == "OpenAI" else "Gemini"

        # Model
        st.markdown('<p class="mono-label">model</p>', unsafe_allow_html=True)
        MODEL_OPTIONS = {
            "OpenAI": {"gpt-4o": "GPT-4o (Best)", "gpt-3.5-turbo": "GPT-3.5 Turbo"},
            "Google Gemini": {
                "gemini-1.5-flash": "Gemini 1.5 Flash (Standard)",
                "gemini-1.5-pro": "Gemini 1.5 Pro (High Reasoning)",
                "gemini-pro": "Gemini 1.0 Pro (Legacy/Stable)"
            }
        }

        model_map = MODEL_OPTIONS[provider]
        selected_display = st.selectbox("Model", list(model_map.values()), label_visibility="collapsed")
        # Reverse map
        selected_model_name = [k for k, v in model_map.items() if v == selected_display][0]

        st.divider()

        # Secrets Management — inside secure well
        secrets = get_secrets_status()

        st.markdown("""
        <div class="secure-well">
            <div class="secure-well-label"><span class="dot"></span>api credentials</div>
        </div>
        """, unsafe_allow_html=True)

        if secrets["requires_unlock"]:
            st.info("Unlock vault in Sidebar to manage keys.")
        else:
            # Key Selection
            st.markdown('<p class="mono-label">active key</p>', unsafe_allow_html=True)
            key_list = secrets.get("openai_keys" if provider == "OpenAI" else "gemini_keys", [])

            key_options = {}
            for k_item in key_list:
                if isinstance(k_item, dict):
                    display = f"{k_item.get('name', 'Key')} (...{k_item.get('key', '')[-4:]})"
                    value = k_item.get('key')
                else:
                    display = f"Legacy (...{k_item[-4:] if len(k_item)>4 else ''})"
                    value = k_item
                key_options[display] = value

            NEW_OPTION = "+ Add New Key"
            selection = st.selectbox("Select Key", [NEW_OPTION] + list(key_options.keys()), label_visibility="collapsed")

            if selection == NEW_OPTION:
                new_key_val = st.text_input("Enter API Key", type="password")
                new_key_name = st.text_input("Key Name (e.g. Personal)", value="My Key")
                save_check = st.checkbox("Save to Vault")

                current_api_key = new_key_val
                if save_check and new_key_val:
                    if secrets["is_encrypted"]:
                        if st.button("Save Encrypted"):
                            if secrets_utils.save_secret_encrypted(prov_key, new_key_name, new_key_val, st.session_state.master_password):
                                st.success("Saved!")
                                st.rerun()
                            else:
                                st.error("Failed to save.")
                    else:
                        if st.button("Save Plaintext"):
                            secrets_utils.save_secret_plain(prov_key, new_key_val)
                            st.success("Saved!")
                            st.rerun()
            else:
                current_api_key = key_options[selection]
                st.session_state.api_key = current_api_key
                st.info(f"Using: {selection}")

            # Encryption Setup
            if not secrets["is_encrypted"] and not secrets["requires_unlock"]:
                st.divider()
                with st.expander("Security: Encrypt Vault"):
                    st.warning("Set a master password. All keys will be encrypted.")
                    pass1 = st.text_input("Master Password", type="password")
                    pass2 = st.text_input("Confirm Password", type="password")
                    if st.button("Enable Encryption"):
                        if pass1 and pass1 == pass2:
                            secrets_utils.init_encryption(pass1)
                            st.session_state.master_password = pass1
                            st.success("Vault Encrypted!")
                            st.rerun()
                        else:
                            st.error("Passwords do not match.")

    # --- Section: Profile ---
    with col_set_2:
        st.markdown(f'<div class="section-box"><h4>Profile: {st.session_state.profile_name}</h4></div>', unsafe_allow_html=True)

        st.markdown('<p class="mono-label">user details</p>', unsafe_allow_html=True)
        # Load active profile
        profile_data = profile_utils.load_profile(st.session_state.profile_name)

        with st.form("profile_form"):
            p_name = st.text_input("Full Name", value=profile_data.get("full_name", ""))
            p_email = st.text_input("Email", value=profile_data.get("email", ""))
            p_phone = st.text_input("Phone", value=profile_data.get("phone", ""))
            p_link = st.text_input("LinkedIn", value=profile_data.get("linkedin", ""))
            p_addr = st.text_input("Address", value=profile_data.get("address", ""))

            if st.form_submit_button("Save Profile"):
                new_data = {
                    "full_name": p_name, "email": p_email, "phone": p_phone,
                    "linkedin": p_link, "address": p_addr
                }
                profile_utils.save_profile(st.session_state.profile_name, new_data)
                st.success("Saved!")

        st.markdown("#### Create New Profile")
        new_prof_name = st.text_input("New Profile Name")
        if st.button("Create Profile"):
            if new_prof_name:
                profile_utils.save_profile(new_prof_name, {})
                st.session_state.profile_name = new_prof_name
                st.rerun()

    # --- Section: Exports Preference ---
    st.divider()
    st.markdown('<p class="mono-label">export formats</p>', unsafe_allow_html=True)
    ex_cols = st.columns(3)
    opts = ["Word", "PDF", "LaTeX"]
    selected_exports = []

    if "export_formats" not in st.session_state: st.session_state.export_formats = opts

    for opt in opts:
        is_checked = opt in st.session_state.export_formats
        if st.checkbox(opt, value=is_checked, key=f"check_{opt}"):
            selected_exports.append(opt)

    st.session_state.export_formats = selected_exports

    # --- Danger Zone ---
    st.divider()
    st.markdown("""
    <div class="danger-zone">
        <h4>Danger Zone</h4>
        <p style="color: #64748B; font-size: 0.9rem; margin-bottom: 0;">
            Erase all data including profiles and API keys permanently.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Factory Reset", type="secondary"):
        # 1. Delete Secrets
        if os.path.exists(secrets_utils.SECRETS_FILE):
             try: os.remove(secrets_utils.SECRETS_FILE)
             except: pass

        # 2. Delete Profiles
        import shutil
        if os.path.exists(profile_utils.PROFILES_DIR):
            try: shutil.rmtree(profile_utils.PROFILES_DIR)
            except: pass

        # 3. Clear Session
        st.session_state.clear()
        st.rerun()


# ==========================
# TAB: GENERATOR
# ==========================
with tab_generator:
    st.header("Create Cover Letter")

    # Reload profile just in case
    live_profile = profile_utils.load_profile(st.session_state.profile_name)
    user_info = {
        "name": live_profile.get("full_name", ""),
        "email": live_profile.get("email", ""),
        "phone": live_profile.get("phone", ""),
        "linkedin": live_profile.get("linkedin", ""),
        "address": live_profile.get("address", "")
    }

    col_gen_1, col_gen_2 = st.columns([1, 1])

    with col_gen_1:
        st.markdown('<div class="section-box"><h4>Input</h4></div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
        job_description = st.text_area("Paste Job Description", height=300)

        today = datetime.date.today()
        letter_date = st.date_input("Date", value=today)
        date_str = letter_date.strftime("%B %d, %Y")

        generate_btn = st.button("Generate", type="primary", use_container_width=True)

    with col_gen_2:
        st.markdown('<div class="section-box"><h4>Result</h4></div>', unsafe_allow_html=True)

        if generate_btn:
             if not st.session_state.api_key:
                 st.error("Missing API Key. Configure it in Settings.")
             elif not uploaded_file or not job_description:
                 st.error("Please provide both a resume and job description.")
             else:
                 with st.spinner("Analyzing & Writing..."):
                     # Extract Text
                     cv_text = utils.extract_text_from_pdf(uploaded_file)

                     if cv_text:
                         prov_key_norm = "Gemini" if provider == "Google Gemini" else "OpenAI"

                         result = utils.generate_cover_letter(
                             cv_text, job_description, st.session_state.api_key,
                             prov_key_norm, user_info, selected_model_name, date_str
                         )

                         if result["ok"]:
                             st.success("Generated successfully.")
                             st.session_state.cover_letter_content = result["text"]

                             # Update Usage
                             u_clean = st.session_state.session_usage
                             new_u = result.get("usage", {})
                             u_clean['tokens'] += new_u.get("total_tokens", 0)
                             u_clean['chars'] += new_u.get("input_chars", 0) + new_u.get("output_chars", 0)

                             # Generate Exports
                             full_data = {
                                 "body": result["text"],
                                 "user_info": live_profile,
                                 "date_str": date_str,
                                 "hr_info": result.get("hr_info_debug", {})
                             }

                             # Save Metadata for editing
                             st.session_state.gen_metadata = {
                                 "user_info": live_profile,
                                 "date_str": date_str,
                                 "hr_info": result.get("hr_info_debug", {})
                             }

                             # Only generate selected
                             formats = st.session_state.export_formats
                             if "Word" in formats:
                                 st.session_state.docx_data = export_utils.create_docx(full_data)
                             if "PDF" in formats:
                                 st.session_state.pdf_data = export_utils.create_pdf(full_data)
                             if "LaTeX" in formats:
                                 data, code = export_utils.create_latex(full_data)
                                 st.session_state.latex_data = data
                                 st.session_state.latex_code = code

                         else:
                             st.error(f"Generation failed: {result['error']}")
                     else:
                         st.error("Failed to read PDF content.")

        # Persistent View
        if st.session_state.cover_letter_content:
            # Editable Preview
            st.markdown("#### Preview & Edit")
            st.text_area(
                "Edit your cover letter here to update downloads:",
                key="cover_letter_content",
                height=400,
                on_change=update_exports
            )

            # Copy Code
            with st.expander("View Raw Text"):
                st.code(st.session_state.cover_letter_content, language="markdown")

            # Downloads
            dl_cols = st.columns(3)
            formats = st.session_state.export_formats

            if "Word" in formats and st.session_state.docx_data:
                dl_cols[0].download_button(
                    label="Download .docx",
                    data=st.session_state.docx_data,
                    file_name="cover_letter.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

            if "PDF" in formats and st.session_state.pdf_data:
                dl_cols[1].download_button(
                    label="Download .pdf",
                    data=st.session_state.pdf_data,
                    file_name="cover_letter.pdf",
                    mime="application/pdf"
                )

            if "LaTeX" in formats and st.session_state.latex_data:
                dl_cols[2].download_button(
                    label="Download .tex",
                    data=st.session_state.latex_data,
                    file_name="cover_letter.tex",
                    mime="application/x-tex"
                )
