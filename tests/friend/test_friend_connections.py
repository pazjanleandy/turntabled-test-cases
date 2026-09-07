from playwright.sync_api import Page

from pages.friend_page import FriendPage


def relationship_state(page: Page, target_username: str) -> bool:
    friends = FriendPage(page)
    friends.open()
    friends.open_user_profile(target_username)
    return friends.is_following()


def restore_relationship(
    primary_page: Page,
    primary_username: str,
    primary_original: bool,
    friend_page: Page,
    friend_username: str,
    friend_original: bool,
):
    FriendPage(primary_page).set_following(friend_username, primary_original)
    FriendPage(friend_page).set_following(primary_username, friend_original)


# FR-CON-001
def test_mutual_follow_creates_friend_connection(two_user_pages):
    primary_page, primary_username = two_user_pages["primary"]
    friend_page, friend_username = two_user_pages["friend"]
    primary_original = relationship_state(primary_page, friend_username)
    friend_original = relationship_state(friend_page, primary_username)

    try:
        FriendPage(primary_page).set_following(friend_username, True)
        FriendPage(friend_page).set_following(primary_username, False)
        FriendPage(primary_page).expect_friend_connection(friend_username, False)
        FriendPage(friend_page).expect_friend_connection(primary_username, False)

        FriendPage(friend_page).set_following(primary_username, True)
        FriendPage(primary_page).expect_friend_connection(friend_username, True)
        FriendPage(friend_page).expect_friend_connection(primary_username, True)
    finally:
        restore_relationship(
            primary_page,
            primary_username,
            primary_original,
            friend_page,
            friend_username,
            friend_original,
        )


# FR-CON-002
def test_unfollow_removes_friend_connection(two_user_pages):
    primary_page, primary_username = two_user_pages["primary"]
    friend_page, friend_username = two_user_pages["friend"]
    primary_original = relationship_state(primary_page, friend_username)
    friend_original = relationship_state(friend_page, primary_username)

    try:
        FriendPage(primary_page).set_following(friend_username, True)
        FriendPage(friend_page).set_following(primary_username, True)
        FriendPage(primary_page).expect_friend_connection(friend_username, True)
        FriendPage(friend_page).expect_friend_connection(primary_username, True)

        FriendPage(primary_page).set_following(friend_username, False)
        FriendPage(primary_page).expect_friend_connection(friend_username, False)
        FriendPage(friend_page).expect_friend_connection(primary_username, False)
    finally:
        restore_relationship(
            primary_page,
            primary_username,
            primary_original,
            friend_page,
            friend_username,
            friend_original,
        )
