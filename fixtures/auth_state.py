import re
from pathlib import Path

from playwright.sync_api import Page, expect

from fixtures.test_data import HOME_URL


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRIMARY_STATE = PROJECT_ROOT / ".auth" / "state.json"
FRIEND_STATE = PROJECT_ROOT / ".auth" / "friend-state.json"


def authenticated_username(page: Page) -> str:
    page.goto(HOME_URL, wait_until="domcontentloaded")
    profile_link = page.get_by_role("navigation").get_by_role(
        "link", name=re.compile(r"^.+ avatar .+$")
    )
    expect(profile_link).to_be_visible(timeout=60_000)
    username = profile_link.inner_text().strip()
    if not username:
        raise RuntimeError("Could not determine the authenticated navbar username.")
    return username
