import re

from playwright.sync_api import Locator, Page, expect

from fixtures.test_data import LISTS_URL


class ListPage:
    def __init__(self, page: Page):
        self.page = page
        self.heading = page.get_by_role("heading", name="Lists", exact=True)
        self.publish_button = page.get_by_role(
            "button", name="Publish list", exact=True
        ).first
        self.category_filter = page.get_by_role(
            "combobox", name="Filter", exact=True
        )
        self.list_search = page.get_by_role(
            "textbox", name="Search", exact=True
        )
        self.published_heading = page.get_by_role(
            "heading", name="Published lists", exact=True
        )
        self.feed = page.locator("section").filter(has=self.published_heading)
        self.shown_count = self.feed.get_by_text(
            re.compile(r"^\d+ shown$", re.IGNORECASE)
        )
        self.feed_titles = self.feed.get_by_role("heading", level=3)
        self.publish_heading = page.get_by_role(
            "heading", name="Publish list", exact=True
        )
        self.album_search = page.get_by_placeholder("Search albums", exact=True)
        self.move_up_buttons = page.get_by_role("button", name="Move album up")
        self.move_down_buttons = page.get_by_role(
            "button", name="Move album down"
        )
        self.remove_buttons = page.get_by_role("button", name="Remove album")

    def open(self):
        self.page.goto(LISTS_URL, wait_until="domcontentloaded")
        expect(self.heading).to_be_visible()
        expect(self.feed_titles.first).to_be_visible(timeout=60_000)

    def sort_button(self, name: str) -> Locator:
        return self.page.get_by_role("button", name=name, exact=True)

    def select_sort(self, name: str):
        button = self.sort_button(name)
        button.click()
        expect(button).to_have_class(re.compile(r"\bborder-accent\b"))
        self.page.evaluate(
            """() => new Promise(resolve => requestAnimationFrame(
                () => requestAnimationFrame(resolve)
            ))"""
        )
        expect(self.feed_titles.first).to_be_visible()

    def visible_list_titles(self) -> list[str]:
        return self.feed_titles.all_inner_texts()

    def select_category(self, category: str):
        self.category_filter.select_option(label=category)
        expect(self.category_filter).to_have_value(category)

    def search_lists(self, term: str):
        self.list_search.fill(term)

    def expect_shown_count(self, count: int):
        expect(self.shown_count).to_have_text(
            f"{count} shown", ignore_case=True
        )

    def open_publish_modal(self):
        self.publish_button.click()
        expect(self.publish_heading).to_be_visible()
        expect(self.album_search).to_be_visible()

    def add_album(self, title: str):
        self.album_search.fill(title)
        expect(self.page.get_by_text(title, exact=True).last).to_be_visible()
        self.page.get_by_role("button", name="Add", exact=True).click()

    def tracklist_item_texts(self) -> list[str]:
        return self.remove_buttons.evaluate_all(
            r"""buttons => buttons.map(button => {
                const lines = button.parentElement.parentElement.innerText
                    .split(/\n+/)
                    .map(line => line.trim())
                    .filter(Boolean);
                return (Boolean(lines[0].match(/^\d{2}$/)) ? lines.slice(1) : lines)
                    .join(' — ');
            })"""
        )

    def cancel_modal(self):
        self.page.get_by_role("button", name="Cancel", exact=True).click()
        expect(self.publish_heading).to_be_hidden()

    def open_owned_list(self, title: str):
        self.open()
        self.feed.get_by_role("heading", name=title, exact=True).click()
        expect(
            self.page.get_by_role("heading", name="Albums in this list")
        ).to_be_visible()

    def enter_edit_mode(self):
        self.page.get_by_role("button", name="Edit", exact=True).click()
        expect(
            self.page.get_by_role("button", name="Save", exact=True)
        ).to_be_visible()
        expect(self.remove_buttons.first).to_be_visible()

    def move_first_album_down(self):
        self.move_down_buttons.first.click()

    def remove_album_at(self, index: int):
        self.remove_buttons.nth(index).click()

    def cancel_edit(self):
        self.page.get_by_role("button", name="Cancel", exact=True).click()
        expect(
            self.page.get_by_role("button", name="Edit", exact=True)
        ).to_be_visible()
