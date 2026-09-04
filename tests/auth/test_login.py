from playwright.sync_api import Page, expect

from fixtures.test_data import BASE_URL, HOME_URL, require_user
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage


def test_successful_login_shows_profile_menu(page: Page):
    user = require_user()
    page.goto(BASE_URL)

    LoginPage(page).login(user["email"], user["password"])

    expect(page).to_have_url(HOME_URL)
    ProfilePage(page).expect_profile_link_visible(user["avatar_name"])


def test_invalid_password_shows_error(page: Page):
    user = require_user()
    page.goto(BASE_URL)
    login_page = LoginPage(page)

    login_page.open_login_modal()
    login_page.fill_credentials(user["email"], "definitely-wrong-password")
    login_page.submit()

    error_message = page.get_by_text("Invalid login credentials")
    expect(error_message).to_be_visible()


def test_empty_login_form_shows_validation(page: Page):
    page.goto(BASE_URL)
    login_page = LoginPage(page)

    login_page.open_login_modal()
    login_page.submit()

    error_message = page.get_by_text("Please enter your email or username and password.")
    expect(error_message).to_be_visible()
