import pytest

from fixtures.auth_state import (
    FRIEND_STATE,
    PRIMARY_STATE,
    authenticated_username,
)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "storage_state": ".auth/state.json",
        "record_video_dir": "videos/",
    }


@pytest.fixture
def two_user_pages(browser):
    missing_states = [
        str(path.relative_to(path.parents[1]))
        for path in (PRIMARY_STATE, FRIEND_STATE)
        if not path.exists()
    ]
    if missing_states:
        pytest.fail(
            "Missing authentication state: "
            + ", ".join(missing_states)
            + ". Run python scripts/generate_friend_state.py."
        )

    primary_context = browser.new_context(
        storage_state=str(PRIMARY_STATE), record_video_dir="videos/"
    )
    friend_context = browser.new_context(
        storage_state=str(FRIEND_STATE), record_video_dir="videos/"
    )
    primary_page = primary_context.new_page()
    friend_page = friend_context.new_page()

    try:
        primary_username = authenticated_username(primary_page)
        friend_username = authenticated_username(friend_page)
        if primary_username.lower() == friend_username.lower():
            pytest.fail("The two authentication states resolve to the same account.")
        yield {
            "primary": (primary_page, primary_username),
            "friend": (friend_page, friend_username),
        }
    finally:
        friend_context.close()
        primary_context.close()
