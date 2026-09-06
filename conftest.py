import os

import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "storage_state": os.getenv("STORAGE_STATE", ".auth/state.json"),
        "record_video_dir": "videos/",
    }
