import re

from playwright.sync_api import Locator, Page, expect

from fixtures.test_data import FRIENDS_URL


class FriendPage:
    def __init__(self, page: Page):
        self.page = page
        self.heading = page.get_by_role("heading", name="Friends", exact=True)
        self.search_input = page.get_by_role(
            "searchbox", name="Search users by username"
        )
        self.sort_control = page.get_by_label("Sort friends")
        self.friend_cards = page.locator('a[href^="/friends/"]:visible')
        self.loading_message = page.get_by_text("Loading friends...", exact=True)
        self.empty_state = page.get_by_text(
            re.compile(r'^No results for ".*"$')
        )

    def open(self):
        self.page.goto(FRIENDS_URL, wait_until="domcontentloaded")
        expect(self.heading).to_be_visible()
        expect(self.search_input).to_be_visible()

    def wait_for_results(self):
        expect(self.loading_message).to_be_hidden(timeout=60_000)
        expect(self.friend_cards.first.or_(self.empty_state)).to_be_visible()

    def search(self, username: str):
        self.search_input.fill(username)

    def user_card(self, username: str) -> Locator:
        return self.friend_cards.filter(has_text=f"@{username}")

    def search_for_user(self, username: str) -> Locator:
        self.search(username)
        card = self.user_card(username)
        expect(card).to_be_visible(timeout=30_000)
        return card

    def filter_button(self, name: str) -> Locator:
        return self.page.get_by_role("button", name=name, exact=True)

    def activate_filter(self, name: str):
        button = self.filter_button(name)
        button.click()
        expect(button).to_have_attribute("aria-pressed", "true")

    def select_sort(self, label: str):
        self.sort_control.select_option(label=label)
        expect(self.sort_control).to_have_value(
            {
                "Recently active": "recent",
                "Most logs": "logs",
                "Highest avg rating": "rating",
                "Longest streak": "streak",
            }[label]
        )

    def open_user_profile(self, username: str):
        self.search_for_user(username).click()
        expect(
            self.page.get_by_role("heading", name=username, exact=True)
        ).to_be_visible(timeout=30_000)
        expect(self.page.get_by_role("main")).to_contain_text(f"@{username}")

    def follow_button(self) -> Locator:
        return self.page.get_by_role(
            "button", name=re.compile(r"^(Follow|Following)$")
        )

    def is_following(self) -> bool:
        button = self.follow_button()
        expect(button).to_be_visible(timeout=60_000)
        return button.inner_text().strip() == "Following"

    def set_following(self, username: str, following: bool):
        self.open()
        self.open_user_profile(username)
        button = self.follow_button()
        current_state = self.is_following()
        if current_state != following:
            button.click()
            expect(button).to_have_text(
                "Following" if following else "Follow", timeout=30_000
            )

    def expect_friend_connection(self, username: str, connected: bool):
        self.open()
        self.page.reload(wait_until="domcontentloaded")
        self.wait_for_results()
        card = self.user_card(username)
        if connected:
            expect(card).to_be_visible(timeout=30_000)
        else:
            expect(card).to_be_hidden(timeout=30_000)
