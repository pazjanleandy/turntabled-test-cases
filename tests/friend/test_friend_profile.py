from playwright.sync_api import Page, expect

from fixtures.test_data import FRIEND_USERNAMES
from pages.friend_page import FriendPage


# FR-PV-002
def test_follow_state_can_be_toggled_and_restored(page: Page):
    friends = FriendPage(page)
    friends.open()
    friends.open_user_profile(FRIEND_USERNAMES[0])
    follow_button = friends.follow_button()
    original_state = follow_button.inner_text().strip()
    toggled_state = "Follow" if original_state == "Following" else "Following"
    state_changed = False

    try:
        follow_button.click()
        expect(follow_button).to_have_text(toggled_state, timeout=15_000)
        state_changed = True
    finally:
        if state_changed:
            follow_button.click()
            expect(follow_button).to_have_text(original_state, timeout=15_000)
