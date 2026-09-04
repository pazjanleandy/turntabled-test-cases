from playwright.sync_api import Page, expect

from fixtures.test_data import BASE_URL, HOME_URL, require_user
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage


def test_user_can_sign_out(page: Page):
    user = require_user()
    page.goto(BASE_URL)

    LoginPage(page).login(user["email"], user["password"])
    expect(page).to_have_url(HOME_URL)

    dashboard_page = DashboardPage(page)
    dashboard_page.open_profile_menu(user["avatar_name"])
    dashboard_page.sign_out()

    expect(page.get_by_role("button", name="Sign In")).to_be_visible()
