from playwright.sync_api import Locator,Page,expect

from fixtures.test_data import ARTISTS_URL

class ArtistsPage:
    def __init__(self, page: Page):
        self.page = page
        self.page_heading = page.get_by_role("heading", name="Artist directory")
        self.search_bar = page.get_by_role("textbox", name="Search artists")
        self.drop_down = page.get_by_role("combobox")

    def navigate_to_artists_page(self):
        self.page.goto(ARTISTS_URL)
        expect(self.page_heading).to_be_visible()

    def fill_search_bar(self, search_text):
        self.page.goto(ARTISTS_URL)
        expect(self.search_bar).to_be_visible()
        self.search_bar.fill(search_text)
        return self

    def check_drop_down_is_visible(self):
        self.page.goto(ARTISTS_URL)
        expect(self.drop_down).to_be_visible()


        


 