
from pathlib import Path
import json
from datetime import datetime


class DevMindDesktopBackend:

    """
    Backend interface for the future DevMind-X
    PySide6 desktop application.
    """

    def __init__(self):

        self.project_path = None

        self.last_report = None


    def select_project(self, project_path):

        path = Path(project_path)

        if not path.exists():

            raise FileNotFoundError(
                f"Project does not exist: {project_path}"
            )

        if not path.is_dir():

            raise ValueError(
                "Selected path is not a directory."
            )

        self.project_path = str(path)

        return {

            "status": "PROJECT_SELECTED",

            "project":
                self.project_path
        }


    def get_project_info(self):

        if not self.project_path:

            return {
                "status":
                    "NO_PROJECT_SELECTED"
            }

        path = Path(
            self.project_path
        )

        files = [
            p for p in path.rglob("*")
            if p.is_file()
        ]

        python_files = [
            p for p in files
            if p.suffix == ".py"
        ]

        return {

            "project":
                str(path),

            "total_files":
                len(files),

            "python_files":
                len(python_files)
        }


    def load_report(self, report_path):

        path = Path(
            report_path
        )

        if not path.exists():

            raise FileNotFoundError(
                str(path)
            )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            self.last_report = json.load(f)

        return self.last_report


    def dashboard_data(self):

        if not self.last_report:

            return {

                "status":
                    "NO_REPORT"
            }

        testing = self.last_report.get(
            "testing",
            {}
        )

        verification = self.last_report.get(
            "verification",
            {}
        )

        return {

            "project":
                self.last_report.get(
                    "project",
                    {}
                ),

            "tests":
                testing,

            "verification":
                verification,

            "agents":
                self.last_report.get(
                    "agents",
                    {}
                ),

            "system":
                self.last_report.get(
                    "system",
                    {}
                )
        }
