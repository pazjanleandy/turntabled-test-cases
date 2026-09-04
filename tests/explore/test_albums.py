from playwright.sync_api import Page, expect

from fixtures.test_data import BASE_URL


def test_turntabled_homepage_loads(page: Page):
    page.goto(BASE_URL)

    expect(page).to_have_title("turntabled")


def test_explore_link_is_visible(page: Page):
    page.goto(BASE_URL)

    explore_link = page.get_by_role("link", name="Explore")
    expect(explore_link).to_be_visible()
