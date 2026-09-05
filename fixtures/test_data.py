import os

import pytest


BASE_URL = os.getenv("BASE_URL", "https://turntabled-backend.onrender.com/")
HOME_URL = os.getenv("HOME_URL", "https://turntabled-backend.onrender.com/home")
EXPLORE_URL = f"{BASE_URL.rstrip('/')}/explore"
LOGGED_ALBUMS_URL = f"{BASE_URL.rstrip('/')}/backlog"
PROFILE_URL = f"{BASE_URL.rstrip('/')}/profile"

USERS = [
    {
        "email": os.getenv("TURNTABLED_USER_EMAIL", ""),
        "password": os.getenv("TURNTABLED_USER_PASSWORD", ""),
        "avatar_name": os.getenv("TURNTABLED_USER_AVATAR", ""),
    },
    {
        "email": os.getenv("TURNTABLED_SECOND_USER_EMAIL", ""),
        "password": os.getenv("TURNTABLED_SECOND_USER_PASSWORD", ""),
        "avatar_name": os.getenv("TURNTABLED_SECOND_USER_AVATAR", ""),
    },
]

REGISTRATION_USER = {
    "email": os.getenv("TURNTABLED_REGISTRATION_EMAIL", "portfolio-example@example.com"),
    "username": os.getenv("TURNTABLED_REGISTRATION_USERNAME", "PortfolioUser"),
    "password": os.getenv("TURNTABLED_REGISTRATION_PASSWORD", "Password_123"),
}

ALBUM_SEARCH_TERMS = [
    {
        "complete": "Blonde",
        "partial": "Blo",
        "trailing": "Blonde   "
    },
    {
        "complete": "The French Operation",
        "partial": "Fren",
        "trailing": "The French Operation   "
    },
    {
        "complete": "AM",
        "partial": "A",
        "trailing": "AM   "
    },
]

ARTIST_SEARCH_TERMS = [
    {
        "complete": "Frank Ocean",
        "partial": "Oce",
        "trailing": "Frank Ocean   "
    },
    {
        "complete": "Arctic Monkeys",
        "partial": "Tic",
        "trailing": "Arctic Monkeys   "
    },
    {
        "complete": "GIRLS BE",
        "partial": "Girls",
        "trailing": "GIRLS BE   "
    },
]


def require_user(index: int = 0) -> dict[str, str]:
    user = USERS[index]
    if not user["email"] or not user["password"] or not user["avatar_name"]:
        pytest.skip("Set Turntabled user credentials in environment variables to run this test.")
    return user
