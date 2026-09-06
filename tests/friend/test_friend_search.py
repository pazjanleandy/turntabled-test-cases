import re

import pytest
from playwright.sync_api import Page, expect

from fixtures.test_data import FRIEND_USERNAMES
from pages.friend_page import FriendPage


@pytest.mark.parametrize("username", FRIEND_USERNAMES)
# FR-FLT-001
def test_search_user_by_username(page: Page, username: str):
    friends = FriendPage(page)
    friends.open()

    card = friends.search_for_user(username)

    expect(card).to_contain_text(f"@{username}")
    expect(friends.friend_cards).to_have_count(1)


# FR-CRD-002
def test_open_user_profile_from_search_result(page: Page):
    username = FRIEND_USERNAMES[0]
    friends = FriendPage(page)
    friends.open()

    friends.open_user_profile(username)

    expect(page).to_have_url(re.compile(r"/friends/[^/?#]+$"))
    expect(page.get_by_role("heading", name=username, exact=True)).to_be_visible()
