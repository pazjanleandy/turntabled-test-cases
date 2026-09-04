# Turntabled Playwright

Playwright end-to-end tests for the Turntabled web app, organized by product area for portfolio review and future growth.

## Structure

- `tests/auth`: login, logout, and registration coverage.
- `tests/dashboard`: authenticated dashboard checks.
- `tests/explore`: public explore and discovery checks.
- `tests/profile`: profile navigation and activity checks.
- `pages`: page object helpers shared by tests.
- `fixtures`: shared test data.
- `.auth/state.json`: local authenticated browser state.
- `screenshots`: local debugging screenshots.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install
```

## Run Tests

```bash
pytest
```

Login and profile tests read credentials from environment variables. Use `.env.example` as a reference for the names to set in your shell or CI.

To refresh authenticated state, save the Playwright storage state to `.auth/state.json`.
