from playwright.sync_api import Page, expect


class DashboardPage:
    def __init__(self, page: Page):
        self.page = page

    def expect_notification_bell_visible(self):
        notification_bell = self.page.get_by_role("button", name="Open notifications")
        expect(notification_bell).to_be_visible()

    def open_profile_menu(self, avatar_name: str):
        profile_menu = self.page.get_by_role("link", name=avatar_name)
        expect(profile_menu).to_be_visible()
        profile_menu.hover()

    def sign_out(self):
        sign_out = self.page.get_by_role("link", name="Sign out")
        expect(sign_out).to_be_visible()
        sign_out.click()

    def toggle_dark_mode(self):
        dark_mode = self.page.get_by_role("switch", name="Dark mode")
        expect(dark_mode).to_be_visible()
        dark_mode.click()

    def popular_albums_search(self, album_title):
        search_bar = self.page.get_by_placeholder("Filter by artist or album")
        expect(search_bar).to_be_visible()
        search_bar.fill(album_title)

    def trending_reviews_visible(self):
        trending_reviews = self.page.locator("section").filter(has_text="Trending ReviewsCommunity").nth(1)
        expect(trending_reviews).to_be_visible()

    def get_featured_review(self):
        return self.page.get_by_role

    def get_interaction_count(self,item):
     return item["engagement"]["interactionCount"]
    
    def rank_reviews(self,items):
     return sorted(
        items,
        key= self.get_interaction_count,
        reverse=True
    )



        
