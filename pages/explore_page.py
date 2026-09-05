import re

from playwright.sync_api import Locator, Page, expect

from fixtures.test_data import EXPLORE_URL


class ExplorePage:
    def __init__(self, page: Page):
        self.page = page
        self.search_input = page.get_by_placeholder(
            "Search albums, artists, or lists"
        )
        self.decade_filter = page.get_by_label("Filter by decade")
        self.genre_filter = page.get_by_label("Filter by genre")
        self.sort_control = page.get_by_label("Sort and filter")
        self.album_cards = page.locator('a[href^="/album/"]:visible')
        self.catalog_heading = page.get_by_role("heading", name="Album catalog")
        self.no_results_message = page.get_by_text(
            "No albums matched your search.", exact=True
        )
        self.next_button = page.get_by_role("button", name="Next", exact=True)
        self.previous_button = page.get_by_role(
            "button", name="Previous", exact=True
        )

    def open(self):
        self.page.goto(EXPLORE_URL)
        expect(self.catalog_heading).to_be_visible()

    def search(self, term: str):
        expect(self.search_input).to_be_visible()
        self.search_input.fill(term)

    def clear_search(self):
        self.search_input.clear()

    def select_decade(self, value: str):
        self.decade_filter.select_option(value)

    def select_genre(self, value: str):
        self.genre_filter.select_option(value)

    def select_sort(self, value: str):
        self.sort_control.select_option(value)

    def album_link(self, accessible_name: str) -> Locator:
        return self.page.get_by_role(
            "link", name=accessible_name, exact=True
        )

    def page_indicator(self, page_number: int) -> Locator:
        return self.page.get_by_text(
            re.compile(rf"^Page {page_number} of \d+$", re.IGNORECASE)
        )

    def visible_album_names(self) -> list[str]:
        return [
            name
            for name in self.album_cards.evaluate_all(
                "cards => cards.map(card => card.getAttribute('aria-label'))"
            )
            if name
        ]

    def go_to_next_page(self):
        expect(self.next_button).to_be_enabled()
        self.next_button.click()

    def go_to_previous_page(self):
        expect(self.previous_button).to_be_enabled()
        self.previous_button.click()
