import pytest
from playwright.sync_api import Page, expect

from fixtures.test_data import ALBUM_SEARCH_TERMS, ARTIST_SEARCH_TERMS
from pages.explore_page import ExplorePage


BLONDE_RESULT = "Blonde by Frank Ocean"


@pytest.mark.parametrize(
    ("term", "expected_result"),
    [
        pytest.param(
            ALBUM_SEARCH_TERMS[0]["complete"],
            BLONDE_RESULT,
            id="complete-album-title",
        ),
        pytest.param(
            ARTIST_SEARCH_TERMS[0]["complete"],
            BLONDE_RESULT,
            id="complete-artist-name",
        ),
        pytest.param(
            ALBUM_SEARCH_TERMS[0]["partial"],
            BLONDE_RESULT,
            id="partial-album-title",
        ),
        pytest.param(
            ARTIST_SEARCH_TERMS[0]["partial"],
            BLONDE_RESULT,
            id="partial-artist-name",
        ),
        pytest.param(
            ALBUM_SEARCH_TERMS[0]["trailing"],
            BLONDE_RESULT,
            id="trailing-whitespace",
        ),
    ],
)
# EXP-ALB-007, EXP-ALB-008, EXP-ALB-009
def test_search_finds_matching_album(
    page: Page, term: str, expected_result: str
):
    explore_page = ExplorePage(page)
    explore_page.open()

    explore_page.search(term)

    expect(explore_page.album_link(expected_result)).to_be_visible()
    expect(explore_page.album_cards).to_have_count(1)


# EXP-ALB-010
def test_search_is_case_insensitive(page: Page):
    explore_page = ExplorePage(page)
    explore_page.open()

    explore_page.search(ALBUM_SEARCH_TERMS[0]["complete"].lower())

    expect(explore_page.album_link(BLONDE_RESULT)).to_be_visible()
    expect(explore_page.album_cards).to_have_count(1)


# EXP-ALB-011
def test_search_with_no_match_shows_empty_state(page: Page):
    explore_page = ExplorePage(page)
    explore_page.open()

    explore_page.search("NO_ALBUM_SHOULD_MATCH_7F3C9A")

    expect(explore_page.no_results_message).to_be_visible()
    expect(explore_page.album_cards).to_have_count(0)


# EXP-ALB-012
def test_clearing_search_restores_catalog(page: Page):
    explore_page = ExplorePage(page)
    explore_page.open()
    expect(explore_page.album_cards.first).to_be_visible()
    initial_album_names = explore_page.visible_album_names()

    explore_page.search(ALBUM_SEARCH_TERMS[0]["complete"])
    expect(explore_page.album_cards).to_have_count(1)

    explore_page.clear_search()

    expect(explore_page.album_cards).to_have_count(len(initial_album_names))
    assert explore_page.visible_album_names() == initial_album_names
