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
st.set_page_config(page_title="AI Cover Letter Generator v1.1", layout="wide", page_icon="📝")

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
        
    st.divider()
    if st.button("🔄 Reset Session"):
        st.session_state.clear()
        st.rerun()

# --- Main Layout ---
st.title("AI 智能求职信生成器 v1.1")
tab_generator, tab_settings = st.tabs(["🚀 Generator", "⚙️ Settings"])

# ==========================
# TAB: SETTINGS
# ==========================
with tab_settings:
    st.header("⚙️ Configuration")
    
    col_set_1, col_set_2 = st.columns(2)
    
    # --- Section: API & Keys ---
    with col_set_1:
        st.subheader("1. AI Provider & Keys")
        
        # Provider
        provider = st.radio("Provider", ["OpenAI", "Google Gemini"], 
                          index=0 if st.session_state.provider == "OpenAI" else 1)
        st.session_state.provider = provider
        
        prov_key = "OpenAI" if provider == "OpenAI" else "Gemini"
        
        # Model (Cosmetic / passed to logic)
        MODEL_OPTIONS = {
            "OpenAI": {"gpt-4o": "GPT-4o (Best)", "gpt-3.5-turbo": "GPT-3.5 Turbo"},
            "Google Gemini": {
                "gemini-1.5-flash": "Gemini 1.5 Flash (Standard)", 
                "gemini-1.5-pro": "Gemini 1.5 Pro (High Reasoning)",
                "gemini-pro": "Gemini 1.0 Pro (Legacy/Stable)"
            }
        }
        
        model_map = MODEL_OPTIONS[provider]
        selected_display = st.selectbox("Model", list(model_map.values()))
        # Reverse map
        selected_model_name = [k for k, v in model_map.items() if v == selected_display][0]
        
        st.markdown("---")
        
        # Secrets Management
        secrets = get_secrets_status()
        
        if secrets["requires_unlock"]:
            st.info("Unlock vault in Sidebar to manage keys.")
        else:
            # Key Selection
            key_list = secrets.get("openai_keys" if provider == "OpenAI" else "gemini_keys", [])
            
            # Format for dropdown: "Name (Masked)" -> value is actual key
            # We need a map. 
            # key_list is mixed: strings (legacy) or dicts (new)
            
            key_options = {}
            for k_item in key_list:
                if isinstance(k_item, dict):
                    display = f"{k_item.get('name', 'Key')} (...{k_item.get('key', '')[-4:]})"
                    value = k_item.get('key')
                else:
                    display = f"Legacy (...{k_item[-4:] if len(k_item)>4 else ''})"
                    value = k_item
                key_options[display] = value
                
            NEW_OPTION = "➕ Add New Key"
            selection = st.selectbox("Select Key", [NEW_OPTION] + list(key_options.keys()))
            
            if selection == NEW_OPTION:
                new_key_val = st.text_input("Enter API Key", type="password")
                new_key_name = st.text_input("Key Name (e.g. Personal)", value="My Key")
                save_check = st.checkbox("Save to Vault")
                
                current_api_key = new_key_val
                if save_check and new_key_val:
                    if secrets["is_encrypted"]:
                        if st.button("💾 Save Encrypted"):
                            if secrets_utils.save_secret_encrypted(prov_key, new_key_name, new_key_val, st.session_state.master_password):
                                st.success("Saved!")
                                st.rerun()
                            else:
                                st.error("Failed to save.")
                    else:
                        if st.button("💾 Save Plaintext"):
                            secrets_utils.save_secret_plain(prov_key, new_key_val) 
                            st.success("Saved!")
                            st.rerun()
            else:
                current_api_key = key_options[selection]
                st.session_state.api_key = current_api_key
                st.info(f"Using: {selection}")
                
            # Encryption Setup
            if not secrets["is_encrypted"] and not secrets["requires_unlock"]:
                st.markdown("---")
                with st.expander("🔐 Security: Encrypt Vault"):
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
        st.subheader(f"2. Profile: {st.session_state.profile_name}")
        
        # Load active profile
        profile_data = profile_utils.load_profile(st.session_state.profile_name)
        
        with st.form("profile_form"):
            p_name = st.text_input("Full Name", value=profile_data.get("full_name", ""))
            p_email = st.text_input("Email", value=profile_data.get("email", ""))
            p_phone = st.text_input("Phone", value=profile_data.get("phone", ""))
            p_link = st.text_input("LinkedIn", value=profile_data.get("linkedin", ""))
            p_addr = st.text_input("Address", value=profile_data.get("address", ""))
            
            if st.form_submit_button("💾 Save Profile"):
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
                profile_utils.save_profile(new_prof_name, {}) # Create empty
                st.session_state.profile_name = new_prof_name
                st.rerun()

    # --- Section: Exports Preference ---
    st.markdown("---")
    st.subheader("3. Export Formats")
    ex_cols = st.columns(3)
    opts = ["Word", "PDF", "LaTeX"]
    selected_exports = []
    
    # Simple checkbox tracking
    if "export_formats" not in st.session_state: st.session_state.export_formats = opts
    
    for opt in opts:
        is_checked = opt in st.session_state.export_formats
        if st.checkbox(opt, value=is_checked, key=f"check_{opt}"):
            selected_exports.append(opt)
    
    st.session_state.export_formats = selected_exports
    
    # --- Danger Zone (Factory Reset) ---
    st.markdown("---")
    st.subheader("🚫 Danger Zone")
    st.warning("Erase all data? This will delete all Profiles and API Keys permanently (Factory Reset).")
    
    if st.button("🧨 Factory Reset (Clear All Data)", type="primary"):
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
    st.header("🚀 Create Cover Letter")
    
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
        st.subheader("Input")
        uploaded_file = st.file_uploader("1. Upload Resume (PDF)", type="pdf")
        job_description = st.text_area("2. Paste Job Description", height=300)
        
        today = datetime.date.today()
        letter_date = st.date_input("3. Date", value=today)
        date_str = letter_date.strftime("%B %d, %Y")
        
        generate_btn = st.button("✨ Generate", type="primary", use_container_width=True)

    with col_gen_2:
        st.subheader("Result")
        
        if generate_btn:
             if not st.session_state.api_key:
                 st.error("❌ Missing API Key in Settings.")
             elif not uploaded_file or not job_description:
                 st.error("❌ Missing Resume or JD.")
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
                             st.success("✅ Generated!")
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
                             st.error(f"Failed: {result['error']}")
                     else:
                         st.error("Failed to read PDF.")

        # Persistent View
        if st.session_state.cover_letter_content:
            # Editable Preview
            st.markdown("### Preview & Edit")
            st.text_area(
                "Edit your cover letter here to update downloads:",
                key="cover_letter_content",
                height=400,
                on_change=update_exports
            )
            
            # Copy Code (Optional)
            with st.expander("📋 View Raw Text (Copy)"):
                st.code(st.session_state.cover_letter_content, language="markdown")
                
            # Downloads
            dl_cols = st.columns(3)
            formats = st.session_state.export_formats
            
            if "Word" in formats and st.session_state.docx_data:
                dl_cols[0].download_button(
                    label="Download .docx",
                    data=st.session_state.docx_data,
                    file_name="cover_letter.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    icon="📄"
                )
            
            if "PDF" in formats and st.session_state.pdf_data:
                dl_cols[1].download_button(
                    label="Download .pdf",
                    data=st.session_state.pdf_data,
                    file_name="cover_letter.pdf",
                    mime="application/pdf",
                    icon="📑"
                )
                
            if "LaTeX" in formats and st.session_state.latex_data:
                dl_cols[2].download_button(
                    label="Download .tex",
                    data=st.session_state.latex_data,
                    file_name="cover_letter.tex",
                    mime="application/x-tex",
                    icon="📜"
                )
