import requests


def test_popular_album_limit():
    response = requests.get("https://turntabled-backend.onrender.com/api/explore/popular?page=1&limit=20")
    data = response.json()

    assert response.status_code == 200
    assert data["limit"] == 20
    assert len(data["items"]) <= 20

def test_popular_albums_api_returns_success():
    response = requests.get("https://turntabled-backend.onrender.com/api/explore?page=1&limit=48&filter=popular-week")
    data = response.json()
    print(data)

    assert response.status_code == 200

def test_popular_week_filter_uses_popular_sort():
    response = requests.get(
        "https://turntabled-backend.onrender.com/api/explore?page=1&limit=48&filter=popular-week"
    )

    data = response.json()

    assert response.status_code == 200
    assert data["sort"] == "popular-week"


def test_trending_reviews_limit():
    response = requests.get("https://turntabled-backend.onrender.com/api/explore/trending-reviews?limit=4")
    data = response.json()
    assert response.status_code == 200
    assert data["limit"] == 4
    assert len(data["items"]) <= 4


def test_grammy_winners_total():
    response = requests.get("https://turntabled-backend.onrender.com/api/explore/grammy-winners")
    data = response.json()
    assert response.status_code == 200
    assert data["total"] == 7
    assert len(data["items"]) <= 7 

def test_trending_review_interaction():
    response = requests.get("https://turntabled-backend.onrender.com/api/explore/trending-reviews?limit=4")
    data = response.json()

    assert response.status_code == 200 
    items = data["items"]

    interaction_counts = [item["engagement"]["interactionCount"]
    for item in items]

    assert interaction_counts == sorted(interaction_counts, reverse = True)


