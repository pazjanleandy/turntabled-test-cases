import pytest
from playwright.sync_api import Page, expect

from pages.list_page import ListPage


@pytest.mark.parametrize(
    ("sort_name", "expected_first"),
    [
        pytest.param("Trending", "Music I listen to while coding", id="trending"),
        pytest.param("Recent", "test", id="recent"),
        pytest.param(
            "Most favorited",
            "Music I listen to while coding",
            id="most-favorited",
        ),
        pytest.param(
            "Most reviewed",
            "Top songs",
            id="most-reviewed",
        ),
    ],
)
# LST-DIS-002
def test_sort_tab_orders_published_lists(
    page: Page, sort_name: str, expected_first: str
):
    lists = ListPage(page)
    lists.open()

    lists.select_sort(sort_name)

    expect(lists.feed_titles.first).to_have_text(expected_first)
    assert len(lists.visible_list_titles()) == 5


@pytest.mark.parametrize(
    ("category", "expected_title"),
    [
        pytest.param("Jazz-Pop/Modern Jazz", "Top songs", id="jazz-modern"),
        pytest.param("Night Drive", "Albums to drive to", id="night-drive"),
    ],
)
# LST-DIS-003
def test_category_filter_shows_matching_list(
    page: Page, category: str, expected_title: str
):
    lists = ListPage(page)
    lists.open()

    lists.select_category(category)

    lists.expect_shown_count(1)
    expect(lists.feed_titles).to_have_count(1)
    expect(lists.feed_titles.first).to_have_text(expected_title)


@pytest.mark.parametrize(
    ("term", "expected_titles"),
    [
        pytest.param(
            "Albums to drive to", ["Albums to drive to"], id="title"
        ),
        pytest.param(
            "PunishedMopy",
            ["Music I listen to while coding", "Albums to drive to"],
            id="creator",
        ),
    ],
)
# LST-DIS-004
def test_list_search_filters_published_lists(
    page: Page, term: str, expected_titles: list[str]
):
    lists = ListPage(page)
    lists.open()

    lists.search_lists(term)

    lists.expect_shown_count(len(expected_titles))
    expect(lists.feed_titles).to_have_count(len(expected_titles))
    assert lists.visible_list_titles() == expected_titles
