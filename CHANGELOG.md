# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2026-01-23

### 🎯 New Features
- **Input Validation**: Added comprehensive validation for all user inputs
  - PDF file validation (size limit: 10MB, format check)
  - Job description validation (length check, empty check)
  - API key format validation for OpenAI and Google
  - Email validation for user profiles
- **Enhanced Error Handling**: All API calls now have proper exception handling
  - OpenAI calls with configurable timeout (60s default)
  - Google Gemini calls completely protected with try-catch
  - Specific error messages for common issues (invalid key, rate limits, timeouts)
  - Network retry logic with exponential backoff
- **Improved User Experience**
  - User-friendly error messages instead of cryptic crashes
  - Step-by-step validation feedback
  - Better error recovery guidance

### 🔧 Technical Improvements
- **API Layer Hardening**
  - Added timeout configuration to OpenAI client
  - Wrapped unprotected Gemini API calls (3 calls now protected)
  - Implemented exponential backoff retry mechanism
  - Replaced bare `except:` clauses with specific exception types

- **Input Validation System**
  - `validate_pdf_file()`: File size, format, and readability checks
  - `validate_job_description()`: Length and content checks
  - `validate_api_key()`: Format validation for multiple providers
  - `validate_email()`: RFC-compliant email format validation

- **PDF Processing**
  - Added file size pre-check before processing
  - Better error handling for corrupted PDFs
  - Empty PDF detection
  - Scanned image PDF detection

### 🐛 Bug Fixes
- Fixed unhandled exceptions in Gemini generation (lines 234, 259, 288 in utils.py)
- Fixed bare except clauses in cleanup code (app.py lines 269, 275)
- Fixed missing error messages when PDF extraction fails
- Fixed missing error messages when job description validation fails

### 📚 Documentation
- Updated README.md with troubleshooting section
- Added error message reference guide
- Documented all validation rules and limits

### 🧪 Testing
- Created test suite foundation in `tests/`
- Added unit tests for validation functions
- Added test coverage for profile and secrets utilities

### ⚠️ Breaking Changes
None - all changes are backward compatible

### 🔒 Security Improvements
- API key validation before use
- Email format validation
- Input length limits to prevent abuse
- Protected against invalid file uploads

### 📊 Performance Notes
- Slight increase in request time due to validation (<100ms)
- Retry logic adds ~1-2s per failed API call (with exponential backoff)
- PDF validation happens client-side (instant for most files)

### 🙏 Contributors
- Development Team

---

## [1.1.0] - 2026-01-22

### 🎯 New Features
- **Encryption Support**: Optional AES encryption for API keys using master password
- **Profile Management**: Support for multiple user profiles/personas
- **Editable Output**: Users can edit generated cover letters before export
- **Enhanced Exports**: Support for Word, PDF, and LaTeX formats

### 🔧 Technical Improvements
- Modular code structure with separate utilities
- Support for multiple AI providers (OpenAI, Google Gemini)
- Session-based state management

### 🐛 Bug Fixes
- Fixed git merge conflicts in README

---

## [1.0.0] - 2026-01-21

### 🎯 Initial Release
- Basic cover letter generation using OpenAI
- PDF resume upload
- Job description input
- Privacy-first architecture with local storage
