# AI Cover Letter Generator v1.1

A local-first, privacy-focused tool to generate tailored cover letters using OpenAI (GPT-4o) or Google Gemini.

## ✅ Published (Live Demo)

Live URL: https://ai-cover-letter-generator.azurewebsites.net

## Features (v1.1)

- **AI-Powered Generation**: Uses OpenAI or Google Gemini.
- **Privacy First**: API keys stored locally (encrypted option available). Resume/JD data is sent *only* to the AI provider.
- **Multi-Profile**: Switch between different personas (e.g., Engineering vs. Management).
- **Professional Exports**: Word (.docx), PDF (.pdf), and LaTeX (.tex).
- **Secure Vault**: Optional master-password encryption for your API keys.

## Quick Start (macOS)

1.  **Clone & CD**
    ```bash
    git clone https://github.com/HansonHe-UW/ai-cover-letter-generator.git
    cd ai-cover-letter-generator
    ```

2.  **Setup**
    Run the setup script to create the virtual environment and install dependencies.
    ```bash
    ./setup.sh
    ```

3.  **Run**
    Launch the app:
    ```bash
    ./start_app.command
    ```
    Or manually:
    ```bash
    source venv/bin/activate
    streamlit run app.py
    ```

    > **Tip (Permission Denied?)**: If macOS blocks the app ("unidentified developer"), simply **Right-Click** `start_app.command` -> **Open**. This bypasses the security check permanently for this file.

## 🔑 Getting Your API Key

This app needs an AI model to work. You can get one easily:

### 1. Google Gemini (Free Tier Available)
*   **Cost**: Historically Free (for personal use via Google AI Studio).
*   **Get Key**: Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
*   **Model**: Supports `gemini-1.5-flash` (fast) and `gemini-1.5-pro`.

### 2. OpenAI (GPT-4o)
*   **Cost**: Paid (Pay-as-you-go).
*   **Get Key**: Go to [OpenAI Platform](https://platform.openai.com/api-keys).
*   **Model**: Supports `gpt-4o`, `gpt-4-turbo`, etc.

## Usage

1.  **Settings**:
    *   Enter your OpenAI or Gemini API Key.
    *   (Optional) Enable Encryption to lock your keys with a password.
    *   Create a Profile with your name and contact info.
2.  **Generator**:
    *   Upload your Resume (PDF).
    *   Paste the Job Description.
    *   Click "Generate".
3.  **Output**:
    *   Preview and Edit the letter directly in the app.
    *   Download in your preferred format (Word, PDF, LaTeX).

## 🔒 Privacy & Security

*   **Local Storage**: Your API keys and profiles are stored in `secrets_store.json` and `profiles/` on your machine.
*   **Encrypted Vault**: v1.1 introduces AES encryption for your keys if you set a master password.
*   **AI Data**: Your Resume text and the Job Description are sent to the selected AI Provider (OpenAI or Google) for processing. They are NOT stored on any third-party server by this app.
*   **Safety**: Prompt injection defenses are enabled to prevent malicious hidden instructions in JDs.

## Requirements

*   Python 3.8+
*   See `requirements.txt` for dependencies.

## Manual QA / Self-Check

To verify the installation:
1.  Run the included tests: `python3 -m unittest tests/test_basics.py`
2.  Launch app, confirm you can create a profile.
3.  Try "Enable Encryption" in Settings.
