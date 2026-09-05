from playwright.sync_api import Locator, Page, expect

from fixtures.test_data import PROFILE_URL


class ProfilePage:
    def __init__(self, page: Page):
        self.page = page
        self.edit_profile_button = page.get_by_role(
            "button", name="Edit profile", exact=True
        )
        self.share_profile_button = page.get_by_role(
            "button", name="Share profile", exact=True
        )
        self.manage_favorites_button = page.get_by_role(
            "button", name="Manage", exact=True
        )
        self.edit_dialog = page.get_by_role("dialog").filter(
            has_text="Update your details"
        )
        self.name_input = self.edit_dialog.get_by_role(
            "textbox", name="Change name", exact=True
        )
        self.bio_input = self.edit_dialog.get_by_role(
            "textbox", name="Change bio", exact=True
        )
        self.save_profile_button = self.edit_dialog.get_by_role(
            "button", name="Save changes", exact=True
        )
        self.cancel_profile_button = self.edit_dialog.get_by_role(
            "button", name="Cancel", exact=True
        )
        self.close_profile_button = self.edit_dialog.get_by_role(
            "button", name="Close edit profile", exact=True
        )
        self.favorites_dialog = page.get_by_role("dialog").filter(
            has_text="Reorder top albums"
        )
        self.review_dialog = page.get_by_role("dialog").filter(
            has_text="Write a review"
        )
        self.review_input = self.review_dialog.get_by_placeholder(
            "Share your thoughts on the album."
        )
        self.save_review_button = self.review_dialog.get_by_role(
            "button", name="Save review", exact=True
        )

    def expect_profile_link_visible(self, avatar_name: str):
        profile_link = self.page.get_by_role("link", name=avatar_name)
        expect(profile_link).to_be_visible()

    def open(self):
        with self.page.expect_response(
            lambda response: response.url.rstrip("/").endswith("/api/profile"),
            timeout=60_000,
        ):
            self.page.goto(PROFILE_URL, wait_until="domcontentloaded")
        expect(self.edit_profile_button).to_be_visible()

    def open_edit_profile(self):
        self.edit_profile_button.click()
        expect(self.edit_dialog).to_be_visible()

    def update_profile_fields(self, name: str, bio: str):
        self.name_input.fill(name)
        self.bio_input.fill(bio)

    def save_profile_changes(self):
        self.save_profile_button.click()

    def cancel_profile_changes(self):
        self.cancel_profile_button.click()

    def choose_avatar(self, file_payload: dict):
        with self.page.expect_file_chooser() as file_chooser:
            self.edit_dialog.get_by_role(
                "button", name="Edit profile image", exact=True
            ).click()
        file_chooser.value.set_files(file_payload)

    def choose_banner(self, file_payload: dict):
        with self.page.expect_file_chooser() as file_chooser:
            self.edit_dialog.get_by_role(
                "button", name="Edit banner image", exact=True
            ).click()
        file_chooser.value.set_files(file_payload)

    def open_favorites_manager(self):
        self.manage_favorites_button.click()
        expect(self.favorites_dialog).to_be_visible()

    def first_review_card(self) -> Locator:
        edit_button = self.page.get_by_role(
            "button", name="Edit", exact=True
        ).first
        return edit_button.locator("xpath=ancestor::article[1]")

    def open_first_review_for_editing(self) -> tuple[str, str]:
        card = self.first_review_card()
        title = card.get_by_role("heading").inner_text()
        card.get_by_role("button", name="Edit", exact=True).click()
        expect(self.review_dialog).to_be_visible()
        expect(self.review_input).not_to_have_value("")
        return title, self.review_input.input_value()

    def save_review(self):
        self.save_review_button.click()
