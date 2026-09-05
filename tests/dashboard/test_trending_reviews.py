from playwright.sync_api import Page, expect
import requests

from fixtures.test_data import HOME_URL, ALBUM_SEARCH_TERMS, ARTIST_SEARCH_TERMS
from pages.dashboard_page import DashboardPage


def test_featured_review_routing(page: Page):
    page.goto(HOME_URL)

    dashboard_page = DashboardPage(page)
    dashboard_page.trending_reviews_visible()

    response = requests.get("https://turntabled-backend.onrender.com/api/explore/trending-reviews?limit=4")
    data = response.json()

    assert response.status_code == 200 
    items = data["items"]

    interaction_counts = [item["engagement"]["interactionCount"]
    for item in items]

    assert interaction_counts == sorted(interaction_counts, reverse = True)

    top_review = max(items, key = lambda item: item["engagement"]["interactionCount"])

    top_album = top_review["album"]["title"]

    featured_review = page.get_by_role("link", name = f"Featured excerpt {top_album}")

    expect(featured_review).to_be_visible()
    featured_review.click()

def test_second_review_routing(page: Page):
    page.goto(HOME_URL)

    dashboard_page = DashboardPage(page)
    dashboard_page.trending_reviews_visible()

    trending_reviews_section = page.locator("section").filter(has_text="Trending ReviewsCommunity").nth(1)

    response = requests.get("https://turntabled-backend.onrender.com/api/explore/trending-reviews?limit=4")
    data = response.json()

    assert response.status_code == 200 
    items = data["items"]

    interaction_counts = [item["engagement"]["interactionCount"]
    for item in items]

    assert interaction_counts == sorted(interaction_counts, reverse = True)

    ranked_reviews = dashboard_page.rank_reviews(items)

    second_review = ranked_reviews[1]

    second_album = second_review["album"]["title"]
    second_review_link = trending_reviews_section.get_by_role("link", name = second_album, exact=True)

    expect(second_review_link).to_be_visible()
    second_review_link.click()
    