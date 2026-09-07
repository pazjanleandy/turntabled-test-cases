from playwright.sync_api import Page, expect
import re, requests
import os
from dotenv import load_dotenv

from pages.artists_page import ArtistsPage

load_dotenv()

SUPABASE_KEY = os.getenv("SUPABASE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
}

def test_artists_search_bar(page: Page):
    artists_page = ArtistsPage(page)
    artists_page.navigate_to_artists_page()
    artists_page.fill_search_bar("Frank Ocean")
    artists_detail = page.get_by_role("link", name="Frank Ocean portrait Frank")
    expect(artists_detail).to_be_visible()
    artist_results = page.locator('a[href^="/artist/"]')
    expect(artist_results).to_have_count(1)

def test_side_bar_buttons(page: Page):
    artists_page = ArtistsPage(page)
    artists_page.navigate_to_artists_page()
    p_button = page.get_by_role("button", name="Jump to P")
    p_button.click()
    p_section = page.locator("div").filter(has_text=re.compile(r"^P$"))
    expect(p_section).to_be_in_viewport()
    a_section = page.locator("div").filter(has_text=re.compile(r"^A$")).first
    expect(a_section).not_to_be_in_viewport()

def test_drop_down_menu(page: Page):
    artists_page = ArtistsPage(page)
    artists_page.navigate_to_artists_page()
    artists_page.check_drop_down_is_visible()
    drop_down_menu = page.get_by_role("combobox")
    drop_down_menu.select_option("Most logged")
    most_logged_heading = page.locator("div").filter(has_text=re.compile(r"^Most logged$"))
    expect(most_logged_heading).to_be_visible()
    drop_down_menu.select_option("Recently logged")
    recently_logged_heading = page.locator("div").filter(has_text=re.compile(r"^Recently logged$"))
    expect(recently_logged_heading).to_be_visible()
    drop_down_menu.select_option("A-Z")
    alphabetical_side_bar = page.get_by_role("navigation", name="Artist alphabetical index")
    expect(alphabetical_side_bar).to_be_visible()

def test_artist_details_page(page: Page):
    artists_page = ArtistsPage(page)
    artists_page.navigate_to_artists_page()
    artist_link = page.get_by_role("link", name="Frank Ocean portrait Frank")
    artist_link.click()

    response = requests.get("https://lztkrofywzzymsteubyv.supabase.co/rest/v1/artist?select=id%2Cmbid%2Cname%2Cmetadata_source%2Ccountry%2Cdisambiguation%2Cimage_url%2Calbum%28id%2Ctitle%2Ccover_art_url%2Crelease_date%2Cprimary_type%2Cbacklog%28rating%2Creview_text%2Cis_favorite%29%29&normalized_name=eq.frank+ocean", 
                            headers = headers)
    print(response.status_code)
    print(response.json())
    assert response.status_code == 200
    data = response.json()

    artist_data = data[0]

    
    artists_name = artist_data["name"]
    artists_image = artist_data["image_url"]
    actual_name = page.get_by_role("heading", name="Frank Ocean")
    expect(actual_name).to_have_text(artists_name)
    actual_image = page.get_by_role("img", name="Frank Ocean portrait")
    expect(actual_image).to_have_attribute("src", artists_image)

def test_return_to_browse_artist_page(page: Page):
    artists_page = ArtistsPage(page)
    artists_page.navigate_to_artists_page()
    artist_link = page.get_by_role("link", name="Frank Ocean portrait Frank")
    artist_link.click()
    artists_page.navigate_to_artists_page()
    page_heading = page.get_by_text("ArtistsArtist directorySearch artistsSort artistsA-ZMost loggedRecently logged", exact=True)
    expect(page_heading).to_be_visible()

def test_click_album_in_artist_page(page: Page):
    artists_page = ArtistsPage(page)
    artists_page.navigate_to_artists_page()
    artist_link = page.get_by_role("link", name="Frank Ocean portrait Frank")
    artist_link.click()
    album_link = page.get_by_role("link", name="01 Blonde cover Blonde Album")
    album_link.click()

    response = requests.get("https://turntabled-backend.onrender.com/api/explore/album?id=f0110296-7327-44e9-9856-0f30d427aae9")
    assert response.status_code == 200

    data = response.json()
    album_data = data["item"]
    expected_artist_name = album_data["artist"]
    expected_album_title = album_data["title"]
    details_section = page.locator("section").filter(has_text="Log this albumRate")
    artist_name = details_section.get_by_text("Frank Ocean", exact=True)
    album_name = page.get_by_role("heading", name = "Blonde")
    expect(artist_name).to_have_text(expected_artist_name)
    expect(album_name).to_have_text(expected_album_title)






