import re
from playwright.sync_api import Page, expect

from fixtures.test_data import HOME_URL
from pages.dashboard_page import DashboardPage

def test_background_themes(page: Page):
    page.goto(HOME_URL)

    dashboard_page = DashboardPage(page)
    dashboard_page.open_profile_menu("PunishedMopy avatar PunishedMopy")
    dashboard_page.toggle_dark_mode()
    expect(page.locator("html")).to_have_attribute("data-theme", "dark")
    dashboard_page.toggle_dark_mode()
    expect(page.locator("html")).to_have_attribute("data-theme", "light")
    dashboard_heading = page.get_by_role("heading", name="Popular albums")
    expect(dashboard_heading).to_be_visible()

def test_notification_bell_is_visible(page: Page):
    page.goto(HOME_URL)

    DashboardPage(page).expect_notification_bell_visible()

def test_dropdown_profile(page: Page):
    page.goto(HOME_URL)

    dashboard_page = DashboardPage(page)
    dashboard_page.open_profile_menu("PunishedMopy avatar PunishedMopy")
    profile_menu = page.get_by_role("link", name="Profile")
    profile_menu.click()
    expect(page).to_have_url(re.compile(".*/profile"))
    edit_button = page.get_by_role("button", name="Edit profile")
    expect(edit_button).to_be_visible()

def test_dropdown_activity(page: Page):
    page.goto(HOME_URL)

    dashboard_page = DashboardPage(page)
    dashboard_page.open_profile_menu("PunishedMopy avatar PunishedMopy")
    activity_menu = page.get_by_role("link", name="Activity")
    activity_menu.click()
    expect(page).to_have_url(re.compile(".*/activity"))
    hero_message = page.get_by_role("heading", name="Logged albums")
    expect(hero_message).to_be_visible()

def test_dropdown_friends(page: Page):
    page.goto(HOME_URL)

    dashboard_page = DashboardPage(page)
    dashboard_page.open_profile_menu("PunishedMopy avatar PunishedMopy")
    activity_menu = page.get_by_role("link", name="Friends")
    activity_menu.click()
    expect(page).to_have_url(re.compile(".*/friends"))
    heading = page.get_by_role("heading", name="Friends")
    expect(heading).to_be_visible()


    


