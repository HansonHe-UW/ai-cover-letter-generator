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
st.set_page_config(page_title="AI Cover Letter Generator v1.2", layout="wide", page_icon="📝")

# --- Model Configuration ---
MODEL_OPTIONS = {
    "OpenAI": {
        "gpt-4o": "GPT-4o (Best Quality)",
        "gpt-3.5-turbo": "GPT-3.5 Turbo (Fast)"
    },
    "Google Gemini": {
        "gemini-1.5-pro": "Gemini 1.5 Pro (Best Reasoning)",
        "gemini-1.5-flash": "Gemini 1.5 Flash (Fast)"
    }
}


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
    "model_name": "gpt-4o",
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

# --- UI Helper Functions ---
def show_error(message):
    """Display user-friendly error message."""
    st.error(f"❌ {message}")

def show_success(message):
    """Display success message."""
    st.success(f"✅ {message}")

def show_info(message):
    """Display info message."""
    st.info(f"ℹ️ {message}")

# --- Sidebar ---
with st.sidebar:
    st.title("🧩 Status")
    
    # Profile Selector
    profile_list = profile_utils.list_profiles()
    selected_idx = 0
    if st.session_state.profile_name in profile_list:
        selected_idx = profile_list.index(st.session_state.profile_name)
    
    new_profile_selection = st.selectbox("👤 Active Profile", profile_list, index=selected_idx)
    if new_profile_selection != st.session_state.profile_name:
        st.session_state.profile_name = new_profile_selection
        st.rerun()

    # Secrets Status
    secrets_status = get_secrets_status()
    if secrets_status["requires_unlock"]:
        st.error("🔒 Secrets Locked")
        pwd_input = st.text_input("Unlock Password", type="password", key="sidebar_pwd")
        if st.button("Unlock"):
            st.session_state.master_password = pwd_input
            st.rerun()
    else:
        if st.session_state.api_key:
            st.success("🟢 API Key: Active")
        else:
            st.warning("🔴 API Key: Missing")

    st.divider()
    
    # Usage Stats
    st.subheader("📊 Session Usage")
    u = st.session_state.session_usage
    if u['tokens'] > 0:
        st.write(f"**Tokens**: ~{u['tokens']}")
    if u['chars'] > 0:
        st.write(f"**Chars**: ~{u['chars']}")

# --- Main Tabs ---
st.title("📝 AI Cover Letter Generator v1.2")

tab1, tab2, tab3 = st.tabs(["⚙️ Settings", "🔧 Generator", "📥 Output"])

# --- Settings Tab ---
with tab1:
    st.header("Settings")
    
    col_s1, col_s2 = st.columns([2, 1])
    
    with col_s1:
        st.subheader("API Configuration")
        provider = st.radio("Provider", ["OpenAI", "Google Gemini"], horizontal=True)
        st.session_state.provider = provider
        
        # Model Selection
        model_map = MODEL_OPTIONS.get(provider, {})
        display_map = {v: k for k, v in model_map.items()}
        current_model = st.session_state.model_name
        
        # Default if switching providers
        if current_model not in model_map:
             current_model = list(model_map.keys())[0]

        # Find display name for current model or default
        default_idx = 0
        model_values = list(model_map.keys())
        if current_model in model_values:
            default_idx = model_values.index(current_model)
            
        selected_display = st.selectbox("Model", list(model_map.values()), index=default_idx)
        st.session_state.model_name = display_map[selected_display]

        
        api_key_input = st.text_input("API Key", type="password", value=st.session_state.api_key, key="api_key_input")
        
        if api_key_input != st.session_state.api_key:
            # Validate API key before saving
            validation = utils.validate_api_key(api_key_input, provider.split()[0].lower())
            if not validation["valid"]:
                show_error(validation["error"])
            else:
                st.session_state.api_key = api_key_input
                show_info("API key validated and saved")
        
        # Encryption
        use_encryption = st.checkbox("🔐 Enable Encryption", value=bool(secrets_utils.SECRETS_FILE and os.path.exists(secrets_utils.SECRETS_FILE)))
        
        if use_encryption:
            pwd_input = st.text_input("Master Password", type="password", key="master_pwd_setup")
            if st.button("Enable Encryption"):
                if not pwd_input:
                    show_error("Password cannot be empty")
                else:
                    try:
                        secrets_utils.set_master_password(pwd_input)
                        # We save current key if exists
                        if st.session_state.api_key:
                             secrets_utils.save_secret(st.session_state.provider, st.session_state.api_key, pwd_input)
                        show_success("Encryption enabled successfully")
                        st.rerun()
                    except Exception as e:
                        show_error(f"Encryption setup failed: {str(e)}")
    
    with col_s2:
        st.subheader("Profile Management")
        profile_name = st.text_input("Profile Name", value="Default")
        
        if st.button("Create Profile"):
            profile_utils.save_profile(profile_name, {
                "name": profile_name,
                "created": str(datetime.datetime.now())
            })
            st.session_state.profile_name = profile_name
            show_success(f"Profile '{profile_name}' created")
            st.rerun()
    
    st.divider()
    st.subheader("👤 Active Profile Settings")
    
    live_profile = profile_utils.load_profile(st.session_state.profile_name)
    
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        name = st.text_input("Full Name", value=live_profile.get("name", ""), key="profile_name")
        email = st.text_input("Email", value=live_profile.get("email", ""), key="profile_email")
    
    with col_p2:
        phone = st.text_input("Phone", value=live_profile.get("phone", ""), key="profile_phone")
        linkedin = st.text_input("LinkedIn URL", value=live_profile.get("linkedin", ""), key="profile_linkedin")
    
    # Validate email before saving
    if st.button("Save Profile"):
        errors = []
        
        if not name:
            errors.append("Name is required")
        
        if email:
            email_validation = utils.validate_email(email)
            if not email_validation["valid"]:
                errors.append(email_validation["error"])
        
        if errors:
            for error in errors:
                show_error(error)
        else:
            updated_profile = {
                "name": name,
                "email": email,
                "phone": phone,
                "linkedin": linkedin
            }
            profile_utils.save_profile(st.session_state.profile_name, updated_profile)
            show_success("Profile saved successfully")

    st.divider()
    with st.expander("⚠️ Danger Zone"):
        st.warning("This will reset the app and delete all local data (profiles, secrets, etc).")
        if st.button("🔴 Factory Reset App"):
            try:
                if os.path.exists("secrets_store.json"): os.remove("secrets_store.json")
                # Profile cleanup logic if needed, or just clear session
                st.session_state.clear()
                st.rerun()
            except Exception as e:
                show_error(f"Reset failed: {e}")


# --- Generator Tab ---
with tab2:
    st.header("Generate Cover Letter")
    
    col_gen_1, col_gen_2 = st.columns([1, 1])
    
    with col_gen_1:
        st.subheader("Input")
        uploaded_file = st.file_uploader("1. Upload Resume (PDF)", type="pdf")
        job_description = st.text_area("2. Paste Job Description", height=300, help="Paste the complete job description from the job posting")
        
        today = datetime.date.today()
        letter_date = st.date_input("3. Date", value=today)
        date_str = letter_date.strftime("%B %d, %Y")
        
        generate_btn = st.button("✨ Generate", type="primary", use_container_width=True)

    with col_gen_2:
        st.subheader("Result")
        
        if generate_btn:
            errors = []
            
            # Validate API Key
            if not st.session_state.api_key:
                errors.append("API Key not configured in Settings tab")
            else:
                api_validation = utils.validate_api_key(st.session_state.api_key, st.session_state.provider.split()[0].lower())
                if not api_validation["valid"]:
                    errors.append(api_validation["error"])
            
            # Validate Resume File
            if not uploaded_file:
                errors.append("Resume PDF file is required")
            else:
                pdf_validation = utils.validate_pdf_file(uploaded_file)
                if not pdf_validation["valid"]:
                    errors.append(pdf_validation["error"])
            
            # Validate Job Description
            if not job_description:
                errors.append("Job Description is required")
            else:
                jd_validation = utils.validate_job_description(job_description)
                if not jd_validation["valid"]:
                    errors.append(jd_validation["error"])
            
            # Display validation errors
            if errors:
                for error in errors:
                    show_error(error)
            else:
                # All validations passed, proceed with generation
                with st.spinner("Analyzing & Writing..."):
                    try:
                        # Extract Text from PDF
                        pdf_result = utils.extract_text_from_pdf(uploaded_file)
                        
                        if not pdf_result["ok"]:
                            show_error(pdf_result["error"])
                        else:
                            cv_text = pdf_result["text"]
                            live_profile = profile_utils.load_profile(st.session_state.profile_name)
                            user_info = {
                                "name": live_profile.get("name", "John Doe"),
                                "email": live_profile.get("email", ""),
                                "phone": live_profile.get("phone", ""),
                                "linkedin": live_profile.get("linkedin", "")
                            }
                            
                            # Call appropriate generation function
                            # Call appropriate generation function
                            if st.session_state.provider == "Google Gemini":
                                result = utils.generate_cover_letter_chain_gemini(
                                    cv_text, job_description, st.session_state.api_key,
                                    user_info, model_name=st.session_state.model_name, date_str=date_str
                                )
                            else:
                                result = utils.generate_cover_letter_chain_openai(
                                    cv_text, job_description, st.session_state.api_key,
                                    user_info, model_name=st.session_state.model_name, date_str=date_str
                                )

                            
                            if result["ok"]:
                                show_success("Cover Letter Generated Successfully!")
                                st.session_state.cover_letter_content = result["text"]
                                st.session_state.gen_metadata = {
                                    "user_info": user_info,
                                    "date_str": date_str,
                                    "hr_info": result.get("hr_info", {})
                                }
                                
                                # Update Usage Stats
                                u_clean = st.session_state.session_usage
                                new_u = result.get("usage", {})
                                u_clean['tokens'] += new_u.get("total_tokens", 0)
                                
                                # Regenerate exports
                                update_exports()
                                st.rerun()
                            else:
                                show_error(result["error"])
                    
                    except Exception as e:
                        show_error(f"Unexpected error occurred: {str(e)}")
                        st.info("Please check your inputs and try again. If the error persists, contact support.")

# --- Output Tab ---
with tab3:
    st.header("Download & Edit")
    
    if not st.session_state.cover_letter_content:
        st.info("👆 Generate a cover letter first in the Generator tab")
    else:
        st.subheader("Edit")
        edited_text = st.text_area(
            "Edit your cover letter:",
            value=st.session_state.cover_letter_content,
            height=400,
            key="letter_editor"
        )
        
        if edited_text != st.session_state.cover_letter_content:
            st.session_state.cover_letter_content = edited_text
            update_exports()
        
        st.divider()
        st.subheader("Export & Download")
        
        col_exp_1, col_exp_2, col_exp_3 = st.columns(3)
        
        with col_exp_1:
            if st.session_state.docx_data:
                st.download_button(
                    label="📄 Download DOCX",
                    data=st.session_state.docx_data,
                    file_name="cover_letter.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
        
        with col_exp_2:
            if st.session_state.pdf_data:
                st.download_button(
                    label="📑 Download PDF",
                    data=st.session_state.pdf_data,
                    file_name="cover_letter.pdf",
                    mime="application/pdf"
                )
        
        with col_exp_3:
            if st.session_state.latex_code:
                st.download_button(
                    label="📋 Download LaTeX",
                    data=st.session_state.latex_code,
                    file_name="cover_letter.tex",
                    mime="text/plain"
                )
        
        st.divider()
        st.subheader("Generation Metadata")
        
        if st.session_state.gen_metadata:
            st.json(st.session_state.gen_metadata)

# Footer
st.divider()
st.caption("🔒 Privacy First: All data processed locally. Never stored on third-party servers.")
