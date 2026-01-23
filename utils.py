import os
import PyPDF2
from openai import OpenAI
import google.generativeai as genai

def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from an uploaded PDF file.
    
    Args:
        uploaded_file: The uploaded PDF file object from Streamlit.
        
    Returns:
        str: The extracted text, or None if an error occurs.
    """
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def generate_cover_letter_chain_openai(cv_text, job_description, api_key, user_info, model_name="gpt-4o", date_str="[Date]"):
    """
    Generates a cover letter using OpenAI (specific model).
    """
    client = OpenAI(api_key=api_key)
    
    # Step 1: Extract Skills + HR Info
    try:
        response_step1 = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are an expert recruiter. Extract the following from the Job Description:\n1. Top technical and soft skills (comma-separated).\n2. Company Name.\n3. Hiring Manager Name (use 'Hiring Manager' if not found).\n4. Company Address (use 'Headquarters' if not found).\n\nReturn as JSON: {\"skills\": \"...\", \"company\": \"...\", \"manager\": \"...\", \"address\": \"...\"}"},
                {"role": "user", "content": f"Job Description:\n{job_description}"}
            ]
        )
        step1_text = response_step1.choices[0].message.content
        # Simple cleaning if it returns markdown json
        step1_text = step1_text.replace("```json", "").replace("```", "")
        import json
        data = json.loads(step1_text)
        skills_from_jd = data.get("skills", "")
        hr_info = {
            "company": data.get("company", "Company"),
            "manager": data.get("manager", "Hiring Manager"),
            "address": data.get("address", "Headquarters")
        }
    except Exception as e:
        return f"Error in Step 1 (Extraction): {e}"

    # Step 2: Match CV experiences to Skills
    try:
        response_step2 = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a career coach. Identify the candidate's experiences from their CV that best match the provided list of required skills. Highlight specific achievements."},
                {"role": "user", "content": f"Skills Required: {skills_from_jd}\n\nCandidate CV:\n{cv_text}"}
            ]
        )
        matched_experiences = response_step2.choices[0].message.content
    except Exception as e:
        return f"Error in Step 2 (Experience Matching): {e}"

    # Step 3: Draft the letter
    try:
        prompt_content = f"""
        You are a professional copywriter. Write a compelling, tailored cover letter.
        
        STRICT FORMATTING RULES:
        The output must start with this EXACT header block:
        
        {user_info['name']}
        {user_info['address']} | {user_info['email']} | {user_info['phone']}
        {user_info['linkedin']}
        
        {date_str}
        
        {hr_info['manager']}
        {hr_info['company']}
        {hr_info['address']}
        
        Dear {hr_info['manager']},
        
        [Rest of the letter based on matched experiences and job description]
        """
        
        response_step3 = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": prompt_content},
                {"role": "user", "content": f"Matched Experiences:\n{matched_experiences}\n\nJob Description:\n{job_description}"}
            ]
        )
        cover_letter = response_step3.choices[0].message.content
        return cover_letter
    except Exception as e:
        return f"Error in Step 3 (Drafting): {e}"

def generate_cover_letter_chain_gemini(cv_text, job_description, api_key, user_info, model_name="gemini-1.5-flash", date_str="[Date]"):
    """
    Generates a cover letter using Google Gemini (specific model).
    """
    try:
        genai.configure(api_key=api_key)
        
        # If user selected a specific model, try to use it directly first
        final_model_name = model_name
        try:
            genai.GenerativeModel(final_model_name)
        except:
             # Fallback logic if the specific model fails (e.g. typos or deprecation)
            candidates = [
                'gemini-2.0-flash', 
                'gemini-flash-latest', 
                'gemini-2.0-flash-lite',
                'gemini-1.5-flash',
                'gemini-pro'
            ]
            for cand in candidates:
                 try:
                    genai.GenerativeModel(cand)
                    final_model_name = cand
                    break
                 except:
                    continue
        
        model = genai.GenerativeModel(final_model_name)
        
        # Step 1: Extract Skills + HR Info
        prompt_1 = f"""
        You are an expert recruiter. Extract the following from the Job Description:
        1. Top technical and soft skills (comma-separated).
        2. Company Name.
        3. Hiring Manager Name (use 'Hiring Manager' if not found).
        4. Company Address (use 'Headquarters' if not found).

        Return strictly as JSON: {{\"skills\": \"...\", \"company\": \"...\", \"manager\": \"...\", \"address\": \"...\"}}
        
        Job Description:
        {job_description}
        """
        response_1 = model.generate_content(prompt_1)
        step1_text = response_1.text.replace("```json", "").replace("```", "")
        import json
        data = json.loads(step1_text)
        skills_from_jd = data.get("skills", "")
        hr_info = {
            "company": data.get("company", "Company"),
            "manager": data.get("manager", "Hiring Manager"),
            "address": data.get("address", "Headquarters")
        }

        # Step 2: Match CV
        prompt_2 = f"""
        You are a career coach. Identify the candidate's experiences from their CV that best match the provided list of required skills. Highlight specific achievements.
        
        Skills Required: {skills_from_jd}
        
        Candidate CV:
        {cv_text}
        """
        response_2 = model.generate_content(prompt_2)
        matched_experiences = response_2.text

        # Step 3: Draft Letter
        prompt_3 = f"""
        You are a professional copywriter. Write a compelling, tailored cover letter.
        
        STRICT FORMATTING RULES:
        The output must start with this EXACT header block:
        
        {user_info['name']}
        {user_info['address']} | {user_info['email']} | {user_info['phone']}
        {user_info['linkedin']}
        
        {date_str}
        
        {hr_info['manager']}
        {hr_info['company']}
        {hr_info['address']}
        
        Dear {hr_info['manager']},
        
        [Rest of the letter using matched experiences and job description]
        
        Matched Experiences:
        {matched_experiences}
        
        Job Description:
        {job_description}
        """
        response_3 = model.generate_content(prompt_3)
        return response_3.text
        
    except Exception as e:
        # Improved Error Message
        error_msg = f"Error with Gemini ({final_model_name} used): {e}\n"
        try:
            available_models = [m.name for m in genai.list_models()]
            error_msg += f"\nAvailable models: {available_models}"
        except:
             error_msg += "\nCould not list available models."
        return error_msg

def generate_cover_letter(cv_text, job_description, api_key, provider, user_info, model_name=None, date_str="[Date]"):
    """
    Wrapper to route request to the correct provider.
    """
    if provider == "OpenAI":
        return generate_cover_letter_chain_openai(cv_text, job_description, api_key, user_info, model_name, date_str)
    elif provider == "Gemini":
        return generate_cover_letter_chain_gemini(cv_text, job_description, api_key, user_info, model_name, date_str)
    else:
        return "Error: Invalid Provider Selected"
