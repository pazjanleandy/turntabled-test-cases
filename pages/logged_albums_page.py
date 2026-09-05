import re

from playwright.sync_api import Locator, Page, expect

from fixtures.test_data import LOGGED_ALBUMS_URL


class LoggedAlbumsPage:
    def __init__(self, page: Page):
        self.page = page
        self.heading = page.get_by_role("heading", name="Logged", exact=True).first
        self.album_links = page.get_by_role(
            "link", name=re.compile(r"^View .+ details$")
        )
        self.album_cards = page.locator("article").filter(has=self.album_links)
        self.shown_count = page.locator("span:visible").filter(
            has_text=re.compile(r"^\d+ shown$", re.IGNORECASE)
        )
        self.rating_filter = page.get_by_role(
            "combobox", name=re.compile(r"^RATING", re.IGNORECASE)
        )
        self.decade_filter = page.get_by_role(
            "combobox", name=re.compile(r"^DECADE", re.IGNORECASE)
        )
        self.genre_filter = page.get_by_role(
            "combobox", name=re.compile(r"^GENRE", re.IGNORECASE)
        )
        self.status_filter = page.get_by_role(
            "combobox", name=re.compile(r"^STATUS", re.IGNORECASE)
        )
        self.sort_control = page.get_by_role(
            "combobox", name=re.compile(r"^SORT", re.IGNORECASE)
        )
        self.empty_state = page.get_by_role("paragraph").filter(
            has_text="No logged albums match your current filters."
        )
        self.artwork = page.get_by_role(
            "img", name=re.compile(r".+ by .+ cover$")
        )

    def open(self):
        with self.page.expect_response(
            lambda response: "/api/backlog?" in response.url,
            timeout=60_000,
        ):
            self.page.goto(LOGGED_ALBUMS_URL, wait_until="domcontentloaded")
        expect(self.heading).to_be_visible()
        expect(self.shown_count).to_be_visible()

    def album_link(self, title: str) -> Locator:
        return self.page.get_by_role(
            "link", name=f"View {title} details", exact=True
        )

    def select_rating(self, value: str):
        self.rating_filter.select_option(value)

    def select_decade(self, value: str):
        self.decade_filter.select_option(value)

    def select_genre(self, value: str):
        self.genre_filter.select_option(value)

    def select_status(self, value: str):
        self.status_filter.select_option(value)

    def select_sort(self, value: str):
        self.sort_control.select_option(value)

    def visible_album_names(self) -> list[str]:
        names = self.album_links.evaluate_all(
            "links => links.map(link => link.getAttribute('aria-label'))"
        )
        return [
            name.removeprefix("View ").removesuffix(" details")
            for name in names
            if name
        ]

    def shown_total(self) -> int:
        match = re.search(r"\d+", self.shown_count.inner_text())
        if not match:
            raise AssertionError("The Logged Albums shown count is not numeric.")
        return int(match.group())

    def card_texts(self) -> list[str]:
        return self.album_cards.all_inner_texts()

    def visible_ratings(self) -> list[float]:
        ratings = []
        for text in self.card_texts():
            match = re.search(r"\b([1-5]\.\d)\b", text)
            if not match:
                raise AssertionError(f"No rating was displayed on card: {text!r}")
            ratings.append(float(match.group(1)))
        return ratings

    def visible_statuses(self) -> list[str]:
        statuses = []
        for text in self.card_texts():
            match = re.search(r"STATUS:\s*(\w+)", text, re.IGNORECASE)
            if not match:
                raise AssertionError(f"No status was displayed on card: {text!r}")
            statuses.append(match.group(1).lower())
        return statuses

    def visible_logged_dates(self) -> list[tuple[int, int]]:
        month_numbers = {
            "JAN": 1,
            "FEB": 2,
            "MAR": 3,
            "APR": 4,
            "MAY": 5,
            "JUN": 6,
            "JUL": 7,
            "AUG": 8,
            "SEP": 9,
            "OCT": 10,
            "NOV": 11,
            "DEC": 12,
        }
        dates = []
        for text in self.card_texts():
            match = re.search(
                r"\b(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s+(\d{1,2})\b",
                text,
                re.IGNORECASE,
            )
            if not match:
                raise AssertionError(
                    f"No logged date was displayed on card: {text!r}"
                )
            dates.append((month_numbers[match.group(1).upper()], int(match.group(2))))
        return dates
