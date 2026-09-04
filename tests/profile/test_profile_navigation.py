from playwright.sync_api import Page

from fixtures.test_data import HOME_URL, require_user
from pages.profile_page import ProfilePage


def test_profile_link_is_visible_for_authenticated_user(page: Page):
    user = require_user()
    page.goto(HOME_URL)

    ProfilePage(page).expect_profile_link_visible(user["avatar_name"])
