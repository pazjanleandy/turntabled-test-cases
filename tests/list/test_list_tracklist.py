from playwright.sync_api import Page, expect

from pages.list_page import ListPage


OWNED_LIST = "Albums for a rainy day"


# LST-PUB-002
def test_albums_can_be_searched_and_added_to_unpublished_tracklist(page: Page):
    lists = ListPage(page)
    lists.open()
    lists.open_publish_modal()

    try:
        lists.add_album("Blonde")
        first_tracklist = lists.tracklist_item_texts()
        expect(lists.remove_buttons).to_have_count(1)
        assert "Blonde" in first_tracklist[0]

        lists.add_album("The French Operation")
        final_tracklist = lists.tracklist_item_texts()
        expect(lists.remove_buttons).to_have_count(2)
        assert "Blonde" in final_tracklist[0]
        assert "The French Operation" in final_tracklist[1]
    finally:
        lists.cancel_modal()


# LST-EDT-002
def test_owned_list_tracklist_can_be_reordered_without_saving(page: Page):
    lists = ListPage(page)
    lists.open_owned_list(OWNED_LIST)
    lists.enter_edit_mode()
    original_order = lists.tracklist_item_texts()

    try:
        lists.move_first_album_down()
        reordered = lists.tracklist_item_texts()

        assert reordered[0] == original_order[1]
        assert reordered[1] == original_order[0]
        assert reordered[2:] == original_order[2:]
    finally:
        lists.cancel_edit()


# LST-EDT-003
def test_album_can_be_removed_from_owned_list_without_saving(page: Page):
    lists = ListPage(page)
    lists.open_owned_list(OWNED_LIST)
    lists.enter_edit_mode()
    original_tracklist = lists.tracklist_item_texts()
    removed_album = original_tracklist[0]

    try:
        lists.remove_album_at(0)
        updated_tracklist = lists.tracklist_item_texts()

        expect(lists.remove_buttons).to_have_count(len(original_tracklist) - 1)
        assert removed_album not in updated_tracklist
        assert updated_tracklist == original_tracklist[1:]
    finally:
        lists.cancel_edit()
