from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def open_login_modal(self):
        sign_in = self.page.get_by_role("button", name="Sign In")
        expect(sign_in).to_be_visible()
        sign_in.click()

    def fill_credentials(self, email: str, password: str):
        email_input = self.page.get_by_role("textbox", name="Email or username")
        password_input = self.page.get_by_role("textbox", name="Password")
        expect(email_input).to_be_visible()
        expect(password_input).to_be_visible()
        email_input.fill(email)
        password_input.fill(password)

    def submit(self):
        self.page.get_by_role("button", name="Sign in").nth(3).click()

    def login(self, email: str, password: str):
        self.open_login_modal()
        self.fill_credentials(email, password)
        self.submit()
