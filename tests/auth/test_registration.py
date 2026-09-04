from playwright.sync_api import Page, expect

from fixtures.test_data import BASE_URL, REGISTRATION_USER


def test_registration_form_accepts_required_fields(page: Page):
    page.goto(BASE_URL)

    sign_up = page.get_by_role("button", name="Create Account")
    expect(sign_up).to_be_visible()
    sign_up.click()

    page.get_by_role("textbox", name="Email address").fill(REGISTRATION_USER["email"])
    page.get_by_role("textbox", name="Username").fill(REGISTRATION_USER["username"])
    page.get_by_role("textbox", name="Password").fill(REGISTRATION_USER["password"])
    page.get_by_role("checkbox", name="I'm at least 16 years old and").click()
    page.get_by_role("checkbox", name="I accept the Privacy Policy").click()
    page.get_by_role("checkbox", name="I am human").click()
    page.get_by_role("button", name="Sign up").click()
