import time

import pytest
from playwright.sync_api import Page, expect

from pages.profile_page import ProfilePage


# UP-EPM-001
def test_edit_profile_opens_with_current_profile_data(page: Page):
    profile = ProfilePage(page)
    profile.open()

    profile.open_edit_profile()

    expect(profile.name_input).not_to_have_value("")
    expect(profile.bio_input).to_be_visible()
    expect(profile.edit_dialog.get_by_text("Last.fm connection")).to_be_visible()
    expect(
        profile.edit_dialog.get_by_text(
            "PNG or JPEG. Banner up to 5MB, avatar up to 2MB.",
            exact=False,
        )
    ).to_be_visible()


# UP-EPM-002
def test_display_name_and_bio_can_be_updated_and_restored(page: Page):
    profile = ProfilePage(page)
    profile.open()
    profile.open_edit_profile()
    original_name = profile.name_input.input_value()
    original_bio = profile.bio_input.input_value()
    suffix = str(time.time_ns())[-6:]
    updated_name = f"{original_name} QA {suffix}"
    updated_bio = f"Profile regression check {suffix}"
    update_was_saved = False

    try:
        profile.update_profile_fields(updated_name, updated_bio)
        profile.save_profile_changes()
        expect(profile.edit_dialog).to_be_hidden(timeout=15_000)
        update_was_saved = True
        expect(
            page.get_by_role("heading", name=updated_name, exact=True).first
        ).to_be_visible()
        expect(
            page.get_by_role("paragraph").filter(has_text=updated_bio)
        ).to_have_text(updated_bio)
    finally:
        if update_was_saved:
            profile.open_edit_profile()
            profile.update_profile_fields(original_name, original_bio)
            profile.save_profile_changes()
            expect(profile.edit_dialog).to_be_hidden(timeout=15_000)
            expect(
                page.get_by_role("heading", name=original_name, exact=True).first
            ).to_be_visible()


# UP-EPM-003
def test_saving_unchanged_profile_shows_no_change_state(page: Page):
    profile = ProfilePage(page)
    profile.open()
    profile.open_edit_profile()

    profile.save_profile_changes()

    expect(profile.edit_dialog).to_be_visible()
    expect(
        profile.edit_dialog.get_by_text("No changes to save.", exact=True)
    ).to_be_visible()


@pytest.mark.parametrize(
    ("target", "size", "expected_message"),
    [
        pytest.param(
            "avatar",
            2 * 1024 * 1024 + 1,
            "Image upload failed: maximum size is 2MB.",
            id="avatar",
        ),
        pytest.param(
            "banner",
            5 * 1024 * 1024 + 1,
            "Cover upload failed: maximum size is 5MB.",
            id="banner",
        ),
    ],
)
# UP-EPM-005
def test_oversized_profile_images_are_rejected(
    page: Page, target: str, size: int, expected_message: str
):
    profile = ProfilePage(page)
    profile.open()
    profile.open_edit_profile()
    payload = {
        "name": f"oversized-{target}.png",
        "mimeType": "image/png",
        "buffer": b"0" * size,
    }

    getattr(profile, f"choose_{target}")(payload)

    expect(
        profile.edit_dialog.get_by_text(expected_message, exact=True)
    ).to_be_visible()
    expect(profile.edit_dialog).to_be_visible()


# UP-EPM-006
def test_unsupported_avatar_type_is_rejected(page: Page):
    profile = ProfilePage(page)
    profile.open()
    profile.open_edit_profile()

    profile.choose_avatar(
        {
            "name": "unsupported.txt",
            "mimeType": "text/plain",
            "buffer": b"not an image",
        }
    )

    expect(
        profile.edit_dialog.get_by_text(
            "Image upload failed: only PNG or JPEG files are supported.",
            exact=True,
        )
    ).to_be_visible()
    expect(profile.edit_dialog).to_be_visible()


# UP-EPM-008
def test_cancel_discards_unsaved_profile_changes(page: Page):
    profile = ProfilePage(page)
    profile.open()
    profile.open_edit_profile()
    original_name = profile.name_input.input_value()
    original_bio = profile.bio_input.input_value()

    profile.update_profile_fields(
        f"{original_name} unsaved",
        f"{original_bio} unsaved",
    )
    profile.cancel_profile_changes()

    expect(profile.edit_dialog).to_be_hidden()
    expect(
        page.get_by_role("heading", name=original_name, exact=True).first
    ).to_be_visible()
    profile.open_edit_profile()
    expect(profile.name_input).to_have_value(original_name)
    expect(profile.bio_input).to_have_value(original_bio)


# UP-FAV-002
def test_manage_favorites_opens_reorder_interface(page: Page):
    profile = ProfilePage(page)
    profile.open()

    profile.open_favorites_manager()

    expect(
        profile.favorites_dialog.get_by_role(
            "heading", name="Reorder top albums", exact=True
        )
    ).to_be_visible()
    expect(
        profile.favorites_dialog.get_by_text(
            "Drag and drop albums to change their order.", exact=True
        )
    ).to_be_visible()
    expect(
        profile.favorites_dialog.get_by_role(
            "button", name="Save order", exact=True
        )
    ).to_be_enabled()


# UP-REV-002, UP-REV-003
def test_existing_review_can_be_edited_and_restored(page: Page):
    profile = ProfilePage(page)
    profile.open()
    review_title, original_text = profile.open_first_review_for_editing()
    updated_text = f"{original_text} QA edit"
    update_was_saved = False

    try:
        profile.review_input.fill(updated_text)
        profile.save_review()
        expect(profile.review_dialog).to_be_hidden(timeout=15_000)
        update_was_saved = True
        expect(
            page.get_by_role("paragraph").filter(has_text=updated_text)
        ).to_have_text(updated_text)
    finally:
        if update_was_saved:
            review_card = page.locator("article:visible").filter(
                has=page.get_by_role(
                    "heading", name=review_title, exact=True
                )
            ).filter(
                has=page.get_by_role("button", name="Edit", exact=True)
            )
            review_card.get_by_role("button", name="Edit", exact=True).click()
            expect(profile.review_dialog).to_be_visible()
            profile.review_input.fill(original_text)
            profile.save_review()
            expect(profile.review_dialog).to_be_hidden(timeout=15_000)
            expect(
                page.get_by_role("paragraph").filter(has_text=original_text)
            ).to_have_text(original_text)
