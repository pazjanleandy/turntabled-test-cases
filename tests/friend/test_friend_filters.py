import pytest
from playwright.sync_api import Page, expect

from pages.friend_page import FriendPage


@pytest.mark.parametrize(
    "filter_name",
    ["Online / Now spinning", "Recently active", "Same city"],
)
# FR-FLT-002
def test_quick_filter_can_be_activated(page: Page, filter_name: str):
    friends = FriendPage(page)
    friends.open()
    friends.wait_for_results()

    friends.activate_filter(filter_name)

    friends.wait_for_results()
    expect(friends.heading).to_be_visible()


@pytest.mark.parametrize(
    "sort_name",
    [
        "Recently active",
        "Most logs",
        "Highest avg rating",
        "Longest streak",
    ],
)
# FR-FLT-003
def test_sort_option_can_be_applied(page: Page, sort_name: str):
    friends = FriendPage(page)
    friends.open()
    friends.wait_for_results()

    friends.select_sort(sort_name)

    friends.wait_for_results()
    expect(friends.heading).to_be_visible()
