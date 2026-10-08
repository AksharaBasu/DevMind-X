
import json
from pathlib import Path


class DevMindDesktopData:

    def __init__(self):

        self.project_root = (
            Path(__file__).resolve().parents[2]
        )

        self.data_file = (
            self.project_root
            / "reports"
            / "desktop_engineering_data.json"
        )

        self.data = {}

        self.load()

    # ------------------------------------------------------------
    # LOAD
    # ------------------------------------------------------------

    def load(self):

        if not self.data_file.exists():

            self.data = {}

            return

        with open(
            self.data_file,
            "r",
            encoding="utf-8"
        ) as file:

            self.data = json.load(file)

    # ------------------------------------------------------------
    # TESTING
    # ------------------------------------------------------------

    def testing(self):

        self.load()

        return self.data.get(
            "testing",
            {}
        )

    # ------------------------------------------------------------
    # BUGS
    # ------------------------------------------------------------

    def bugs(self):

        self.load()

        return self.data.get(
            "bugs",
            {}
        )

    # ------------------------------------------------------------
    # SECURITY
    # ------------------------------------------------------------

    def security(self):

        self.load()

        return self.data.get(
            "security",
            {}
        )

    # ------------------------------------------------------------
    # PERFORMANCE
    # ------------------------------------------------------------

    def performance(self):

        self.load()

        return self.data.get(
            "performance",
            {}
        )

    # ------------------------------------------------------------
    # COMPLETE DATA
    # ------------------------------------------------------------

    def all_data(self):

        self.load()

        return self.data
