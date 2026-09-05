import re

from playwright.sync_api import Page, expect

from fixtures.test_data import BASE_URL
from pages.explore_page import ExplorePage


def test_turntabled_homepage_loads(page: Page):
    page.goto(BASE_URL)

    expect(page).to_have_title("turntabled")


def test_explore_link_is_visible(page: Page):
    page.goto(BASE_URL)

    explore_link = page.get_by_role("link", name="Explore")
    expect(explore_link).to_be_visible()


def test_album_catalog_loads(page: Page):
    explore_page = ExplorePage(page)
    explore_page.open()

    expect(explore_page.album_cards.first).to_be_visible()
    expect(explore_page.page_indicator(1)).to_be_visible()
    expect(explore_page.next_button).to_be_enabled()


def test_decade_filter_includes_and_excludes_known_albums(page: Page):
    explore_page = ExplorePage(page)
    explore_page.open()

    explore_page.select_decade("2010")

    expect(explore_page.decade_filter).to_have_value("2010")
    expect(
        explore_page.album_link("Blonde by Frank Ocean")
    ).to_be_visible()
    expect(
        explore_page.album_link("After Hours by The Weeknd")
    ).to_be_hidden()


def test_search_remains_applied_with_decade_filter(page: Page):
    explore_page = ExplorePage(page)
    explore_page.open()

    explore_page.select_decade("2010")
    explore_page.search("Blonde")

    expect(explore_page.decade_filter).to_have_value("2010")
    expect(
        explore_page.album_link("Blonde by Frank Ocean")
    ).to_be_visible()
    expect(explore_page.album_cards).to_have_count(1)


def test_next_and_previous_catalog_pages_restore_results(page: Page):
    explore_page = ExplorePage(page)
    explore_page.open()
    expect(explore_page.album_cards.first).to_be_visible()
    first_page_albums = explore_page.visible_album_names()

    explore_page.go_to_next_page()

    expect(page).to_have_url(re.compile(r"[?&]page=2(?:&|$)"))
    expect(explore_page.page_indicator(2)).to_be_visible()
    second_page_albums = explore_page.visible_album_names()
    assert second_page_albums != first_page_albums

    explore_page.go_to_previous_page()

    expect(page).not_to_have_url(re.compile(r"[?&]page=2(?:&|$)"))
    expect(explore_page.page_indicator(1)).to_be_visible()
    expect(explore_page.album_cards).to_have_count(len(first_page_albums))
    assert explore_page.visible_album_names() == first_page_albums
