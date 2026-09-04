from playwright.sync_api import Page, expect

from fixtures.test_data import BASE_URL


def test_artists_link_is_visible(page: Page):
    page.goto(BASE_URL)

    artists_link = page.get_by_role("link", name="Artists")
    expect(artists_link).to_be_visible()
