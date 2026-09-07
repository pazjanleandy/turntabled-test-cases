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


def test_grammy_winners_does_not_exceed_display_limit():
    response = requests.get("https://turntabled-backend.onrender.com/api/explore/grammy-winners")
    data = response.json()
    assert response.status_code == 200
    assert data["total"] == 7
    assert len(data["items"]) <= 7 

def test_trending_reviews_sorted_by_interaction_count():
    response = requests.get("https://turntabled-backend.onrender.com/api/explore/trending-reviews?limit=4")
    data = response.json()

    assert response.status_code == 200 
    items = data["items"]

    interaction_counts = [item["engagement"]["interactionCount"]
    for item in items]

    assert interaction_counts == sorted(interaction_counts, reverse = True)

def test_notification_unread_count(api_headers):
    response = requests.get(
        "https://turntabled-backend.onrender.com/api/notifications/unread-count",
        headers=api_headers,
    )
    data = response.json()
    assert response.status_code == 200
    assert "unreadCount" in data
    unread_count = data["unreadCount"]
    assert type(unread_count) is int
    assert unread_count >= 0

def test_user_endpoint(api_headers, supabase_url, test_user_email):
    response = requests.get(f"{supabase_url}/auth/v1/user", headers=api_headers)
    data = response.json()
    assert response.status_code == 200
    assert data["email"] == test_user_email

def test_activity_summary_respects_limit(api_headers):
    response = requests.get("https://turntabled-backend.onrender.com/api/backlog/summary?activityLimit=5", headers = api_headers)
    data = response.json()

    assert response.status_code == 200
    assert "activity" in data
    assert len(data["activity"]) <= 5

