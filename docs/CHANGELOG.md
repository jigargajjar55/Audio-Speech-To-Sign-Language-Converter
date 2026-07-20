# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Enterprise-grade directory structure (`src/`, `config/`, `docs/`, `tests/`).
- `NLPService` abstraction for handling complex language processing logic.
- Modular Django views (`auth.py`, `home.py`, `animation.py`).
- GitHub Actions CI pipeline for linting (`flake8`) and testing (`pytest`).
- GitGuardian-compliant security measures (`.env`, `SECURITY.md`).
- Comprehensive documentation (`ARCHITECTURE.md`, `CONTRIBUTING.md`).
- Improved UI/UX with Inter font, custom scrollbars, and toast notifications.
- Accessibility improvements (ARIA labels).

### Changed
- Refactored `A2SL` config directory to `config`.
- Moved core application logic from monolithic `views.py` into `src.core` app.
- Extracted inline CSS and JavaScript from templates to static assets.

### Security
- Removed hardcoded `SECRET_KEY` and `DEBUG` variables from `settings.py`.
- Added comprehensive `.gitignore` to prevent secret leakage.
