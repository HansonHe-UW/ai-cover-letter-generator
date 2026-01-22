# AI Cover Letter Generator 🚀

[![Made with Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?style=flat&logo=openai&logoColor=white)](https://openai.com/)
[![Gemini](https://img.shields.io/badge/Google-Gemini--1.5-8E75B2?style=flat&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)

A professional, privacy-focused AI tool that crafts tailored cover letters from your Resume (PDF) and a Job Description. Built for macOS users who want a clean, production-ready workflow.

## ✨ Features

-   **Multi-Model Intelligence**: Choose between **OpenAI (GPT-4o)** for maximum quality or **Google Gemini (1.5 Pro/Flash)** for speed and longer context.
-   **Granular Control**: Toggle between "Budget Mode" (Flash/Turbo) and "Quality Mode" (GPT-4o/Pro) on the fly.
-   **Smart Profile Management**: Your personal details (Name, Email, Links) are persisted locally but **never hardcoded** in the source.
-   **Secure API Key Vault**: Keys are stored locally in a git-ignored file. You only need to enter them once.
-   **Parallel Export**: Instantly generate downloads in **Word (.docx)**, **PDF (.pdf)**, and **LaTeX (.tex)** formats.
-   **Privacy First**: All sensitive data (`my_profile.json`, `secrets_store.json`) is strictly excluded from version control.

## 🚀 Installation & Setup (macOS)

### 1. Clone the Repository
```bash
git clone https://github.com/HansonHe-UW/ai-cover-letter-generator.git
cd ai-cover-letter-generator
```

### 2. Auto-Setup
Run the included setup script. This will check for Homebrew, Python 3, create a virtual environment, and install dependencies.
```bash
./setup.sh
```

### 3. Launch the App
Use the one-click launcher to start the server and open your browser automatically.
```bash
./start_app.command
```
*(Or manually run: `./run.sh`)*

## ⚙️ Configuration

### User Profile
Go to the **"⚙️ Settings"** tab in the app to set up your profile.
-   Name, Email, Phone, LinkedIn, Address.
-   This data is saved to `my_profile.json` locally.

### API Keys
Enter your OpenAI or Google Gemini API keys in the **Settings** tab.
-   You can save them for future sessions.
-   They are stored securely in `secrets_store.json`.

## 🛡️ Privacy & Security
This project is configured to **ignore** sensitive files. Ensure you have the `.gitignore` file present which blocks:
-   `secrets_store.json`
-   `my_profile.json`
-   `.env`

## 📦 Tech Stack
-   **Frontend**: Streamlit
-   **AI Core**: OpenAI API, Google Generative AI SDK
-   **PDF Processing**: PyPDF2
-   **Document Gen**: python-docx, FPDF2

---
Made with ❤️ by [Hanson He]
