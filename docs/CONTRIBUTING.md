# Contributing to SignSpeak

First off, thank you for considering contributing to SignSpeak! We welcome contributions from everyone.

## Development Setup

1. Fork the repository.
2. Clone your fork locally.
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Run tests: `pytest`

## Code Standards

We enforce strict clean code and security standards:

- **Linting**: Ensure your code passes `flake8`.
- **Formatting**: We recommend using `black` for Python formatting.
- **Secrets**: Never commit secrets or `.env` files. Ensure `.gitignore` is respected. GitGuardian checks run on all PRs.
- **Testing**: Any new logic added to `src/core/services/` must be accompanied by a unit test in `tests/`.

## Pull Request Process

1. Create a feature branch (`git checkout -b feature/amazing-feature`).
2. Commit your changes (`git commit -m 'feat: Add amazing feature'`).
3. Push to the branch (`git push origin feature/amazing-feature`).
4. Open a Pull Request against the `main` branch.
5. Ensure the GitHub Actions CI pipeline passes successfully.
6. Wait for a code review from a maintainer.
