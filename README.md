# AI Cover Letter Generator v1.1

A local-first, privacy-focused tool to generate tailored cover letters using OpenAI (GPT-4o) or Google Gemini.

## Features (v1.1)

- **AI-Powered Generation**: Uses OpenAI or Google Gemini.
- **Privacy First**: API keys stored locally (encrypted option available). Resume/JD data is sent *only* to the AI provider.
- **Multi-Profile**: Switch between different personas (e.g., Engineering vs. Management).
- **Professional Exports**: Word (.docx), PDF (.pdf), and LaTeX (.tex).
- **Secure Vault**: Optional master-password encryption for your API keys.

## Quick Start (macOS)

1.  **Clone & CD**
    ```bash
    git clone https://github.com/your-username/ai-cover-letter-generator.git
    cd ai-cover-letter-generator
    ```

<<<<<<< HEAD
### 1. Clone the Repository
```bash
git clone https://github.com/HansonHe-UW/ai-cover-letter-generator.git
cd ai-cover-letter-generator
```
=======
2.  **Setup**
    Run the setup script to create the virtual environment and install dependencies.
    ```bash
    ./setup.sh
    ```
>>>>>>> 9204232 (Release v1.1: Added encryption, editable results, and improved exports)

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

<<<<<<< HEAD
---
Made with ❤️ by [Hanson He]
=======
## Manual QA / Self-Check

To verify the installation:
1.  Run the included tests: `python3 -m unittest tests/test_basics.py`
2.  Launch app, confirm you can create a profile.
3.  Try "Enable Encryption" in Settings.
>>>>>>> 9204232 (Release v1.1: Added encryption, editable results, and improved exports)
