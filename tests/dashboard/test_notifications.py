from playwright.sync_api import Page

from fixtures.test_data import HOME_URL
from pages.dashboard_page import DashboardPage


def test_notification_bell_is_visible(page: Page):
    page.goto(HOME_URL)

    DashboardPage(page).expect_notification_bell_visible()
