import os

import pytest


BASE_URL = os.getenv("BASE_URL", "https://turntabled-backend.onrender.com/")
HOME_URL = os.getenv("HOME_URL", "https://turntabled-backend.onrender.com/home")

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


def require_user(index: int = 0) -> dict[str, str]:
    user = USERS[index]
    if not user["email"] or not user["password"] or not user["avatar_name"]:
        pytest.skip("Set Turntabled user credentials in environment variables to run this test.")
    return user
