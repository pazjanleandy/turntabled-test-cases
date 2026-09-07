import os

import pytest
import requests
from dotenv import load_dotenv

from fixtures.auth_state import (
    FRIEND_STATE,
    PRIMARY_STATE,
    authenticated_username,
)

load_dotenv()


def _required_env(*names):
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    pytest.fail("Missing required environment variable: " + " or ".join(names))


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "storage_state": os.getenv("STORAGE_STATE", ".auth/state.json"),
        "record_video_dir": "videos/",
    }


@pytest.fixture
def two_user_pages(browser):
    missing_states = [
        str(path.relative_to(path.parents[1]))
        for path in (PRIMARY_STATE, FRIEND_STATE)
        if not path.exists()
    ]
    if missing_states:
        pytest.fail(
            "Missing authentication state: "
            + ", ".join(missing_states)
            + ". Run python scripts/generate_friend_state.py."
        )

    primary_context = browser.new_context(
        storage_state=str(PRIMARY_STATE), record_video_dir="videos/"
    )
    friend_context = browser.new_context(
        storage_state=str(FRIEND_STATE), record_video_dir="videos/"
    )
    primary_page = primary_context.new_page()
    friend_page = friend_context.new_page()

    try:
        primary_username = authenticated_username(primary_page)
        friend_username = authenticated_username(friend_page)
        if primary_username.lower() == friend_username.lower():
            pytest.fail("The two authentication states resolve to the same account.")
        yield {
            "primary": (primary_page, primary_username),
            "friend": (friend_page, friend_username),
        }
    finally:
        friend_context.close()
        primary_context.close()


@pytest.fixture
def supabase_url():
    return _required_env("SUPABASE_URL").rstrip("/")


@pytest.fixture
def supabase_key():
    return _required_env("SUPABASE_KEY")


@pytest.fixture
def test_user_email():
    return _required_env("TEST_EMAIL", "TURNTABLED_USER_EMAIL")


@pytest.fixture
def test_user_password():
    return _required_env("TEST_PASSWORD", "TURNTABLED_USER_PASSWORD")


@pytest.fixture
def api_headers(supabase_url, supabase_key, test_user_email, test_user_password):
    try:
        response = requests.post(
            f"{supabase_url}/auth/v1/token?grant_type=password",
            headers={
                "apikey": supabase_key,
                "Content-Type": "application/json",
            },
            json={
                "email": test_user_email,
                "password": test_user_password,
            },
            timeout=15,
        )
    except requests.RequestException as error:
        pytest.fail(f"Supabase login request failed: {error.__class__.__name__}")

    if response.status_code != 200:
        pytest.fail(f"Supabase login failed: {response.status_code} {response.text}")

    access_token = response.json().get("access_token")
    if not access_token:
        pytest.fail("Supabase login response did not include an access_token.")

    return {
        "apikey": supabase_key,
        "Authorization": f"Bearer {access_token}",
    }
