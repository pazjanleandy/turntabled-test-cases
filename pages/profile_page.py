from playwright.sync_api import Page, expect


class ProfilePage:
    def __init__(self, page: Page):
        self.page = page

    def expect_profile_link_visible(self, avatar_name: str):
        profile_link = self.page.get_by_role("link", name=avatar_name)
        expect(profile_link).to_be_visible()
