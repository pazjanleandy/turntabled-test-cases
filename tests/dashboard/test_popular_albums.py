from playwright.sync_api import Page, expect

from fixtures.test_data import HOME_URL, ALBUM_SEARCH_TERMS, ARTIST_SEARCH_TERMS
from pages.dashboard_page import DashboardPage

def test_search_popular_albums(page: Page):
    page.goto(HOME_URL)

    dashboard_page = DashboardPage(page)
    dashboard_page.popular_albums_search(ALBUM_SEARCH_TERMS[0]["complete"])
    search_result = page.get_by_role("link", name="Frank Ocean", exact=True)
    expect(search_result).to_be_visible()
    hidden_album = page.get_by_role("link", name="Arctic Monkeys", exact=True)
    expect(hidden_album).to_be_hidden()

def test_search_popular_partial_albums(page: Page):
    page.goto(HOME_URL)

    dashboard_page = DashboardPage(page)
    dashboard_page.popular_albums_search(ALBUM_SEARCH_TERMS[0]["partial"])
    search_result = page.get_by_role("link", name="Frank Ocean", exact=True)
    expect(search_result).to_be_visible()

def test_search_complete_artists(page: Page):
    page.goto(HOME_URL)

    dashboard_page = DashboardPage(page)
    dashboard_page.popular_albums_search(ARTIST_SEARCH_TERMS[0]["complete"])
    search_result = page.get_by_role("link", name="Frank Ocean", exact=True)
    expect(search_result).to_be_visible()

def test_search_partial_artists(page: Page):
    page.goto(HOME_URL)

    dashboard_page = DashboardPage(page)
    dashboard_page.popular_albums_search(ARTIST_SEARCH_TERMS[0]["partial"])
    search_result = page.get_by_role("link", name="Frank Ocean", exact=True)
    expect(search_result).to_be_visible()

def test_search_trailing_album(page: Page):
    page.goto(HOME_URL)

    dashboard_page = DashboardPage(page)
    dashboard_page.popular_albums_search(ALBUM_SEARCH_TERMS[0]["trailing"])
    search_result = page.get_by_role("link", name="Frank Ocean", exact=True)
    expect(search_result).to_be_visible()
