import re

import pytest
from playwright.sync_api import Page, expect

from pages.logged_albums_page import LoggedAlbumsPage


# ALB-LOG-001, ALB-LOG-002, ALB-LOG-005, ALB-LOG-006, ALB-LOG-022
def test_logged_albums_page_loads_with_card_metadata(page: Page):
    logged_albums = LoggedAlbumsPage(page)
    logged_albums.open()

    expect(logged_albums.album_links.first).to_be_visible()
    album_count = logged_albums.album_links.count()

    assert album_count > 0
    assert logged_albums.shown_total() == album_count
    assert len(logged_albums.visible_ratings()) == album_count
    assert len(logged_albums.visible_logged_dates()) == album_count
    expect(logged_albums.artwork).to_have_count(album_count)


# ALB-LOG-003
def test_logged_album_opens_its_matching_detail_page(page: Page):
    logged_albums = LoggedAlbumsPage(page)
    logged_albums.open()
    first_album = logged_albums.album_links.first
    accessible_name = first_album.get_attribute("aria-label")
    destination = first_album.get_attribute("href")

    assert accessible_name is not None
    assert destination is not None
    album_title = accessible_name.removeprefix("View ").removesuffix(" details")

    first_album.click()

    expect(page).to_have_url(re.compile(rf"{re.escape(destination)}$"))
    expect(
        page.get_by_role("heading", name=album_title, exact=True).first
    ).to_be_visible(timeout=15_000)


# ALB-LOG-007, ALB-LOG-016
def test_rating_filter_updates_results_and_shown_count(page: Page):
    logged_albums = LoggedAlbumsPage(page)
    logged_albums.open()
    initial_count = logged_albums.shown_total()

    logged_albums.select_rating("5")

    expect(logged_albums.rating_filter).to_have_value("5")
    expect(logged_albums.album_links.first).to_be_visible()
    ratings = logged_albums.visible_ratings()
    assert ratings
    assert all(rating >= 5 for rating in ratings)
    assert logged_albums.shown_total() == len(ratings) < initial_count


@pytest.mark.parametrize(
    ("status_value", "expected_status"),
    [
        pytest.param("listened", "listened", id="listened"),
        pytest.param("backloggd", "backloggd", id="backloggd"),
    ],
)
# ALB-LOG-013, ALB-LOG-016
def test_status_filter_only_shows_matching_albums(
    page: Page, status_value: str, expected_status: str
):
    logged_albums = LoggedAlbumsPage(page)
    logged_albums.open()

    logged_albums.select_status(status_value)

    expect(logged_albums.status_filter).to_have_value(status_value)
    expect(logged_albums.album_links.first).to_be_visible()
    statuses = logged_albums.visible_statuses()
    assert statuses
    assert all(status == expected_status for status in statuses)
    assert logged_albums.shown_total() == len(statuses)


@pytest.mark.parametrize(
    ("filter_name", "filtered_value"),
    [
        pytest.param("rating", "5", id="rating"),
        pytest.param("status", "listened", id="status"),
    ],
)
# ALB-LOG-008, ALB-LOG-014, ALB-LOG-025
def test_filter_reset_restores_original_collection(
    page: Page, filter_name: str, filtered_value: str
):
    logged_albums = LoggedAlbumsPage(page)
    logged_albums.open()
    original_albums = logged_albums.visible_album_names()
    filter_control = getattr(logged_albums, f"{filter_name}_filter")

    filter_control.select_option(filtered_value)
    expect(logged_albums.album_links).not_to_have_count(len(original_albums))

    filter_control.select_option("all")

    expect(logged_albums.album_links).to_have_count(len(original_albums))
    assert logged_albums.visible_album_names() == original_albums
    assert logged_albums.shown_total() == len(original_albums)


# ALB-LOG-015, ALB-LOG-016
def test_rating_and_status_filters_apply_together(page: Page):
    logged_albums = LoggedAlbumsPage(page)
    logged_albums.open()

    logged_albums.select_rating("4")
    logged_albums.select_status("backloggd")

    expect(logged_albums.album_links.first).to_be_visible()
    ratings = logged_albums.visible_ratings()
    statuses = logged_albums.visible_statuses()
    assert ratings
    assert all(rating >= 4 for rating in ratings)
    assert all(status == "backloggd" for status in statuses)
    assert logged_albums.shown_total() == len(ratings) == len(statuses)


# ALB-LOG-017
def test_filters_can_produce_an_empty_state(page: Page):
    logged_albums = LoggedAlbumsPage(page)
    logged_albums.open()

    logged_albums.select_rating("5")
    logged_albums.select_status("backloggd")

    expect(logged_albums.empty_state).to_be_visible()
    expect(logged_albums.album_links).to_have_count(0)
    assert logged_albums.shown_total() == 0


@pytest.mark.parametrize(
    ("sort_value", "reverse"),
    [
        pytest.param("date-logged-desc", True, id="newest"),
        pytest.param("date-logged-asc", False, id="oldest"),
    ],
)
# ALB-LOG-018, ALB-LOG-019
def test_logged_date_sorting(page: Page, sort_value: str, reverse: bool):
    logged_albums = LoggedAlbumsPage(page)
    logged_albums.open()

    logged_albums.select_sort(sort_value)

    expect(logged_albums.sort_control).to_have_value(sort_value)
    dates = logged_albums.visible_logged_dates()
    assert dates == sorted(dates, reverse=reverse)


# ALB-LOG-021
def test_sorting_preserves_active_status_filter(page: Page):
    logged_albums = LoggedAlbumsPage(page)
    logged_albums.open()

    logged_albums.select_status("listened")
    logged_albums.select_sort("date-logged-asc")

    expect(logged_albums.status_filter).to_have_value("listened")
    expect(logged_albums.sort_control).to_have_value("date-logged-asc")
    assert all(
        status == "listened"
        for status in logged_albums.visible_statuses()
    )
    dates = logged_albums.visible_logged_dates()
    assert dates == sorted(dates)


# ALB-LOG-025, ALB-LOG-026
def test_collection_is_restored_after_filter_reset_and_refresh(page: Page):
    logged_albums = LoggedAlbumsPage(page)
    logged_albums.open()
    original_albums = logged_albums.visible_album_names()

    logged_albums.select_rating("5")
    expect(logged_albums.album_links).not_to_have_count(len(original_albums))
    logged_albums.select_rating("all")
    expect(logged_albums.album_links).to_have_count(len(original_albums))

    with page.expect_response(
        lambda response: "/api/backlog?" in response.url,
        timeout=60_000,
    ):
        page.reload(wait_until="domcontentloaded")

    expect(logged_albums.album_links).to_have_count(len(original_albums))
    refreshed_albums = logged_albums.visible_album_names()
    assert refreshed_albums == original_albums
    assert len(refreshed_albums) == len(set(refreshed_albums))
