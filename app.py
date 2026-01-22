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
st.set_page_config(page_title="AI 智能求职信生成器", layout="wide")

# --- Initialize Session State ---
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'provider' not in st.session_state:
    st.session_state.provider = "OpenAI"

# --- Model Configuration ---
MODEL_OPTIONS = {
    "OpenAI": {
        "gpt-4o": "GPT-4o (Best Quality - Paid)",
        "gpt-3.5-turbo": "GPT-3.5 Turbo (Fast & Cheap)"
    },
    "Google Gemini": {
        "gemini-2.0-flash": "Gemini 2.0 Flash (New - Fast)",
        "gemini-1.5-flash": "Gemini 1.5 Flash (Standard)",
        "gemini-1.5-pro": "Gemini 1.5 Pro (High Reasoning)"
    }
}

# --- Sidebar (Status & Reset) ---
with st.sidebar:
    st.title("🧩 Status")
    
    # Check Profile
    profile = profile_utils.load_profile()
    if profile.get("full_name"):
        st.success(f"👤 Profile: {profile.get('full_name')}")
    else:
        st.warning("👤 Profile: Empty")
        
    # Check API Key
    if st.session_state.api_key:
        st.success("🟢 API Key: Set")
    else:
        st.error("🔴 API Key: Missing")
        
    st.divider()
    
    # Reset Button
    if st.button("🔄 Reset App State"):
        st.session_state.clear()
        st.rerun()

# --- Initialize Session State for Content ---
if 'cover_letter_content' not in st.session_state:
    st.session_state.cover_letter_content = None
if 'docx_data' not in st.session_state:
    st.session_state.docx_data = None
if 'pdf_data' not in st.session_state:
    st.session_state.pdf_data = None
if 'latex_data' not in st.session_state:
    st.session_state.latex_data = None
if 'latex_code' not in st.session_state:
    st.session_state.latex_code = None


# --- Main Layout ---
st.title("AI 智能求职信生成器")

tab_generator, tab_settings = st.tabs(["🚀 Generator", "⚙️ Settings"])

# ==========================
# TAB: SETTINGS
# ==========================
with tab_settings:
    st.header("⚙️ Configuration")
    
    col_set_1, col_set_2 = st.columns(2)
    
    # --- Section 1: API & Model ---
    with col_set_1:
        st.subheader("1. AI Provider & Model")
        
        # Provider Selection
        provider_options = list(MODEL_OPTIONS.keys())
        provider = st.radio("AGI Provider", provider_options, index=0 if st.session_state.provider == "OpenAI" else 1)
        st.session_state.provider = provider
        
        # Model Selection
        model_map = MODEL_OPTIONS[provider]
        display_model_map = {v: k for k, v in model_map.items()}
        selected_display_name = st.selectbox("Model Version", list(model_map.values()))
        selected_model_name = display_model_map[selected_display_name]
        
        # API Key Management
        st.markdown("---")
        st.markdown("**API Key Management**")
        
        secrets = secrets_utils.load_secrets()
        if provider == "OpenAI":
            saved_keys = secrets.get("openai_keys", [])
        else:
            saved_keys = secrets.get("gemini_keys", [])
            
        NEW_KEY_OPTION = "➕ Enter New Key"
        options = [NEW_KEY_OPTION] + [secrets_utils.mask_key(k) for k in saved_keys]
        key_map = {secrets_utils.mask_key(k): k for k in saved_keys}
        
        selected_option = st.selectbox(f"Select saved {provider} Key", options)
        
        if selected_option == NEW_KEY_OPTION:
            api_input = st.text_input(f"Enter {provider} API Key", type="password")
            save_key_check = st.checkbox(f"Save this {provider} key safely")
            current_api_key = api_input
            should_save = save_key_check
        else:
            current_api_key = key_map[selected_option]
            should_save = False
            st.info(f"Using saved key: {selected_option}")
        
        # Update session state with the valid key immediately for the sidebar status
        if current_api_key:
            st.session_state.api_key = current_api_key

    # --- Section 2: User Profile ---
    with col_set_2:
        st.subheader("2. User Profile")
        with st.form("profile_form"):
            user_name = st.text_input("姓名 (Name)", value=profile.get("full_name", ""), placeholder="e.g. John Doe")
            user_email = st.text_input("邮箱 (Email)", value=profile.get("email", ""), placeholder="e.g. john.doe@example.com")
            user_phone = st.text_input("电话 (Phone)", value=profile.get("phone", ""), placeholder="e.g. +1 555-010-9999")
            user_linkedin = st.text_input("LinkedIn", value=profile.get("linkedin", ""), placeholder="e.g. linkedin.com/in/johndoe")
            user_address = st.text_input("地址 (Address)", value=profile.get("address", ""), placeholder="e.g. Toronto, ON")
            
            submitted = st.form_submit_button("💾 Save Profile")
            if submitted:
                new_profile = {
                    "full_name": user_name,
                    "email": user_email,
                    "phone": user_phone,
                    "linkedin": user_linkedin,
                    "address": user_address
                }
                if profile_utils.save_profile(new_profile):
                    st.success("Profile saved successfully!")
                    st.rerun() # Rerun to update sidebar status

    # --- Section 3: Factory Reset ---
    st.markdown("---")
    with st.expander("⚠️ Danger Zone"):
        st.warning("This will delete all saved API keys and your profile data. This action cannot be undone.")
        if st.button("🗑️ Reset App & Delete All Data", type="primary", use_container_width=True):
            # Delete files
            try:
                if os.path.exists("secrets_store.json"):
                    os.remove("secrets_store.json")
                if os.path.exists("my_profile.json"):
                    os.remove("my_profile.json")
                # Optional: clear output output dir if we had one, but we use in-memory mostly
            except Exception as e:
                st.error(f"Error deleting files: {e}")
            
            # Clear State
            st.session_state.clear()
            st.toast("App reset successfully!", icon="🧹")
            st.rerun()

# ==========================
# TAB: GENERATOR
# ==========================
with tab_generator:
    st.header("🚀 Create Cover Letter")
    
    # Prepare User Info from live profile
    # Reload to ensure fresh data if just saved
    live_profile = profile_utils.load_profile()
    user_info = {
        "name": live_profile.get("full_name", ""),
        "email": live_profile.get("email", ""),
        "phone": live_profile.get("phone", ""),
        "linkedin": live_profile.get("linkedin", ""),
        "address": live_profile.get("address", "")
    }
    
    col_gen_1, col_gen_2 = st.columns([1, 1])
    
    with col_gen_1:
        st.subheader("Input")
        uploaded_file = st.file_uploader("1. Upload Resume (PDF)", type="pdf")
        job_description = st.text_area("2. Paste Job Description (JD)", height=300)
        
        # Date Selection
        today = datetime.date.today()
        letter_date = st.date_input("3. Date on Letter", value=today)
        date_str = letter_date.strftime("%B %d, %Y") # e.g. January 21, 2026
        
        generate_btn = st.button("✨ Generate Cover Letter", type="primary", use_container_width=True)

    with col_gen_2:
        st.subheader("Output")
        
        # Generation Logic
        if generate_btn:
            if not current_api_key:
                st.error(f"❌ Missing API Key. Please go to 'Settings' tab to configure {provider}.")
            elif not uploaded_file:
                st.error("❌ Please upload your Resume PDF.")
            elif not job_description:
                st.error("❌ Please enter the Job Description.")
            else:
                # Save key if requested (Just-in-time saving)
                if should_save and current_api_key:
                    secrets_utils.save_secret(provider, current_api_key)
                    st.toast(f"API Key saved to {provider} history!", icon="💾")
                
                with st.spinner(f"AI ({selected_model_name}) is analyzing & writing..."):
                    # Extract text
                    cv_text = utils.extract_text_from_pdf(uploaded_file)
                    
                    if cv_text:
                        # Map "Google Gemini" to "Gemini" for the backend utility
                        backend_provider = "Gemini" if provider == "Google Gemini" else "OpenAI"

                        # Generate
                        cover_letter = utils.generate_cover_letter(
                            cv_text, job_description, current_api_key, backend_provider, user_info, selected_model_name, date_str
                        )
                        
                        if cover_letter and not cover_letter.startswith("Error"):
                            # STORE SUCCESS IN SESSION STATE
                            st.session_state.cover_letter_content = cover_letter
                            
                            # Prepare Data for Export
                            full_data = {
                                "body": cover_letter,
                                "user_info": live_profile,
                                "date_str": date_str,
                                "hr_info": {} 
                            }
                            
                            # Generate Files and Store in Session State
                            st.session_state.docx_data = export_utils.create_docx(full_data)
                            st.session_state.pdf_data = export_utils.create_pdf(full_data)
                            st.session_state.latex_data, st.session_state.latex_code = export_utils.create_latex(full_data)
                            
                            st.success("✅ Success! Content Saved.")
                            
                        else:
                            st.error(f"Generation Failed: {cover_letter}")
                    else:
                        st.error("Could not extract text from PDF.")

        # Display Logic (Persistent)
        if st.session_state.cover_letter_content:
            st.success("✅ Generated Successfully")
            st.markdown("### Preview")
            st.text_area("Finalized Text", value=st.session_state.cover_letter_content, height=400)
            
            # Download Buttons (Using Session State Data)
            col_dl_1, col_dl_2, col_dl_3 = st.columns(3)
            with col_dl_1:
                st.download_button(
                    "📄 Word (.docx)", 
                    st.session_state.docx_data, 
                    "cover_letter.docx", 
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            with col_dl_2:
                st.download_button(
                    "📑 PDF (.pdf)", 
                    st.session_state.pdf_data, 
                    "cover_letter.pdf", 
                    "application/pdf"
                )
            with col_dl_3:
                st.download_button(
                    "📜 LaTeX (.tex)", 
                    st.session_state.latex_data, 
                    "cover_letter.tex", 
                    "application/x-tex"
                )
                
            # Source View
            if st.session_state.latex_code:
                with st.expander("🔍 View LaTeX Source Code"):
                    st.code(st.session_state.latex_code, language='tex')
