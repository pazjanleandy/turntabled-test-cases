from playwright.sync_api import Page, expect
import requests, re

from fixtures.test_data import HOME_URL, ALBUM_SEARCH_TERMS, ARTIST_SEARCH_TERMS
from pages.dashboard_page import DashboardPage


def test_featured_community_list_is_highest_engagement (page: Page):
    page.goto(HOME_URL)

    dashboard_page = DashboardPage(page)
    dashboard_page.trending_lists_visible()

    response = requests.get("https://turntabled-backend.onrender.com/api/lists?sort=trending&page=1&limit=12")
    data = response.json()

    assert response.status_code == 200
    items = data["items"]

    interaction_counts = [item["favoriteCount"] + item["commentCount"] for item in items]

    assert interaction_counts == sorted(interaction_counts, reverse=True)

    ranked_lists = dashboard_page.rank_lists(items)
    featured_list = ranked_lists[0]
    top_list = featured_list["title"]
    featured_card = page.locator("section:nth-child(4) > .card")
    expect(featured_card).to_contain_text(top_list)

def test_featured_list_routes_to_modal(page: Page):
    page.goto(HOME_URL)
    dashboard_page = DashboardPage(page)
    dashboard_page.trending_lists_visible()

    featured_open_list = page.get_by_role("link", name="Open list").first
    expected_route = featured_open_list.get_attribute("href")
    featured_open_list.click()
    expect(page).to_have_url(re.compile(re.escape(expected_route)))
    expect(page.locator(""))
    modal_data = page.get_by_text("List viewer")
    modal_data2 = page.get_by_role("button", name="Favorite", exact=True)
    expect(modal_data).to_be_visible()
    expect(modal_data2).to_be_visible()

def test_list_view_all_routing(page: Page):
    page.goto(HOME_URL)
    dashboard_page = DashboardPage(page)
    dashboard_page.trending_lists_visible()

    view_all_link = page.get_by_role("link", name="View all").nth(2)
    view_all_link.click()
    list_page_heading = page.get_by_role("heading", name="Lists", exact=True)
    expect(list_page_heading).to_be_visible()
    list_page_hero_card = page.locator("section").filter(has_text="Featured list · 3/11/")
    expect(list_page_hero_card).to_be_visible()
    list_page_subheading = page.get_by_text("FeedPublished listsFreshly")
    expect(list_page_subheading).to_be_visible()

def test_list_author_routing (page: Page):
    page.goto(HOME_URL)
    
    dashboard_page = DashboardPage(page)
    dashboard_page.trending_lists_visible()
    
    response = requests.get("https://turntabled-backend.onrender.com/api/lists?sort=trending&page=1&limit=12")
    data = response.json()
    
    assert response.status_code == 200
    items = data["items"]

    trending_lists_section = page.locator("section:nth-child(4) > .card")
    selected_list = items[0]
    creator_username = selected_list["creator"]["username"]
    creator_link = trending_lists_section.get_by_role("link", name=creator_username)
    expect(creator_link).to_be_visible()
    creator_link.click()


def test_return_to_dashboard(page: Page):
    page.goto(HOME_URL)
    dashboard_page = DashboardPage(page)
    dashboard_page.trending_lists_visible()

    view_all_link = page.get_by_role("link", name="View all").nth(2)
    view_all_link.click()
    published_list_section = page.locator("section").filter(has_text="FeedPublished listsFreshly")
    list_card = published_list_section.get_by_role("button").first

    expect(list_card).to_be_visible()
    list_card.click()

    modal_data = page.get_by_text("List viewer")
    expect(modal_data).to_be_visible()
    page.go_back()
    expect(page).to_have_url(HOME_URL)
    discovery_showcase = page.get_by_role("main").locator("section").filter(has_text="Discovery showcaseMost loved")
    expect(discovery_showcase).to_be_visible()



    




    
    





