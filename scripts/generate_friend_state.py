import sys
from pathlib import Path

from dotenv import load_dotenv
from playwright.sync_api import Page, expect, sync_playwright

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
load_dotenv(PROJECT_ROOT / "tests" / ".env")

from fixtures.auth_state import (
    FRIEND_STATE,
    PRIMARY_STATE,
    authenticated_username,
)
from fixtures.test_data import BASE_URL, HOME_URL, USERS
from pages.login_page import LoginPage


def complete_users() -> list[dict[str, str]]:
    users = [
        user
        for user in USERS
        if user["email"] and user["password"] and user["avatar_name"]
    ]
    if len(users) != 2:
        raise RuntimeError("Two complete Turntabled test accounts are required.")
    return users


def main():
    if not PRIMARY_STATE.exists():
        raise RuntimeError("Generate .auth/state.json for the Pudge account first.")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        primary_context = browser.new_context(storage_state=str(PRIMARY_STATE))
        primary_page = primary_context.new_page()
        primary_username = authenticated_username(primary_page)
        primary_context.close()

        candidates = [
            user
            for user in complete_users()
            if primary_username.lower() not in user["avatar_name"].lower()
        ]
        if len(candidates) != 1:
            raise RuntimeError(
                "Could not uniquely map the configured account identities."
            )

        friend_context = browser.new_context()
        friend_page = friend_context.new_page()
        friend_page.goto(BASE_URL, wait_until="domcontentloaded")
        LoginPage(friend_page).login(
            candidates[0]["email"], candidates[0]["password"]
        )
        expect(friend_page).to_have_url(HOME_URL, timeout=60_000)
        friend_username = authenticated_username(friend_page)
        if friend_username.lower() == primary_username.lower():
            raise RuntimeError("Both authenticated states resolve to the same account.")

        FRIEND_STATE.parent.mkdir(parents=True, exist_ok=True)
        friend_context.storage_state(path=str(FRIEND_STATE))
        friend_context.close()

        verification_context = browser.new_context(storage_state=str(FRIEND_STATE))
        verification_page = verification_context.new_page()
        verified_username = authenticated_username(verification_page)
        verification_context.close()
        browser.close()

    if verified_username.lower() != friend_username.lower():
        raise RuntimeError("The saved friend authentication state failed validation.")
    print(f"Primary state: @{primary_username}")
    print(f"Friend state: @{friend_username}")


if __name__ == "__main__":
    main()
