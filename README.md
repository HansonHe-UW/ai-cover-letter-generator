# AI Cover Letter Generator v1.2

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Release](https://img.shields.io/github/v/release/HansonHe-UW/ai-cover-letter-generator.svg)](https://github.com/HansonHe-UW/ai-cover-letter-generator/releases)

A local-first, privacy-focused tool to generate tailored cover letters using OpenAI (GPT-4o) or Google Gemini.

## Features (v1.2)

- **AI-Powered Generation**: Uses OpenAI or Google Gemini.
- **Privacy First**: API keys stored locally (encrypted option available). Resume/JD data is sent *only* to the AI provider.
- **Multi-Profile**: Switch between different personas (e.g., Engineering vs. Management).
- **Professional Exports**: Word (.docx), PDF (.pdf), and LaTeX (.tex).
- **Secure Vault**: Optional master-password encryption for your API keys.
- **Comprehensive Error Handling**: Robust error handling for all API calls (v1.2 NEW)
- **Input Validation**: All user inputs validated before processing (v1.2 NEW)
- **User-Friendly Errors**: Clear error messages instead of crashes (v1.2 NEW)

## Quick Start (macOS)

### 1. Clone & CD

```bash
git clone https://github.com/HansonHe-UW/ai-cover-letter-generator.git
cd ai-cover-letter-generator
```

### 2. Setup

Run the setup script to create the virtual environment and install dependencies:

```bash
./setup.sh
```

### 3. Configure API Keys

Copy the example env file and add your API keys:

```bash
cp .env.example .env
# Edit .env with your OpenAI or Google Gemini API key
```

### 4. Run the App

Launch the app:

```bash
./start_app.command
```

Or manually:

```bash
source venv/bin/activate
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Usage

1.  **Settings Tab**:
    *   Enter your OpenAI or Google Gemini API Key.
    *   (Optional) Enable Encryption to lock your keys with a password.
    *   Create or select a Profile with your name and contact info.
2.  **Generator Tab**:
    *   Upload your Resume (PDF).
    *   Paste the Job Description.
    *   Click "Generate".
3.  **Output Tab**:
    *   Preview and edit the letter directly in the app.
    *   Download in your preferred format (Word, PDF, LaTeX).

## 🔒 Privacy & Security

*   **Local Storage**: Your API keys and profiles are stored in `secrets_store.json` and `profiles/` on your machine.
*   **Encrypted Vault**: v1.2 includes AES encryption for your keys if you set a master password.
*   **AI Data**: Your Resume text and the Job Description are sent to the selected AI Provider (OpenAI or Google Gemini) for processing. They are NOT stored on any third-party server by this app.
*   **Safety**: Prompt injection defenses are enabled to prevent malicious hidden instructions in JDs.

## Requirements

*   Python 3.8 or higher
*   See `requirements.txt` for all dependencies.

## Testing

To verify the installation:

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

Alternatively, you can manually verify:
1.  Launch app and confirm you can create a profile.
2.  Try "Enable Encryption" in Settings.

## Troubleshooting

**Q: "Module not found" errors?**  
A: Run `./setup.sh` again, then activate the virtual environment: `source venv/bin/activate`

**Q: API key not working?**  
A: Verify your key is correct in Settings. For OpenAI, check https://platform.openai.com/account/api-keys. For Google, check https://console.cloud.google.com

**Q: PDF upload fails?**  
A: Ensure the PDF contains extractable text (not scanned images).

**Q: "PDF file too large"?**  
A: Max file size is 10MB. Compress your PDF or use a shorter resume.

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### What you can do:
✅ Use commercially  
✅ Modify the code  
✅ Distribute it  
✅ Use privately  

### What you must do:
✅ Include the original license and copyright notice

[Learn more about MIT License](https://opensource.org/licenses/MIT)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📚 Documentation

- [CHANGELOG.md](CHANGELOG.md) - Version history and changes
- [v1.2_RELEASE_NOTES.md](v1.2_RELEASE_NOTES.md) - v1.2.0 release guide
- [IMPROVEMENTS.md](IMPROVEMENTS.md) - Future roadmap

---

Made with ❤️ by [Hanson He](https://github.com/HansonHe-UW)

**Questions?** Open an [issue](https://github.com/HansonHe-UW/ai-cover-letter-generator/issues) or check the [discussions](https://github.com/HansonHe-UW/ai-cover-letter-generator/discussions)
