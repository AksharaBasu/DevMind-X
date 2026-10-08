
import json
from pathlib import Path


class DevMindDashboardData:

    def __init__(self, project_root=None):

        if project_root is None:
            project_root = Path(__file__).resolve().parents[2]

        self.project_root = Path(project_root)

        self.report_path = (
            self.project_root
            / "reports"
            / "devmind_x_final_report.json"
        )

        self.report = {}
        self.load_report()

    # ---------------------------------------------------------
    # LOAD REPORT
    # ---------------------------------------------------------

    def load_report(self):

        if not self.report_path.exists():
            self.report = {}
            return

        with open(
            self.report_path,
            "r",
            encoding="utf-8"
        ) as file:

            self.report = json.load(file)

    # ---------------------------------------------------------
    # COMPLETE REPORT
    # ---------------------------------------------------------

    def get_report(self):

        self.load_report()
        return self.report

    # ---------------------------------------------------------
    # PROJECT PAGE
    # ---------------------------------------------------------

    def get_project_data(self):

        project = self.report.get(
            "project",
            {}
        )

        return {
            "project_name": project.get(
                "name",
                "DevMind-X Project"
            ),

            "project_path": project.get(
                "path",
                str(self.project_root)
            ),

            "python_files": project.get(
                "python_files",
                0
            ),

            "total_files": project.get(
                "files",
                project.get(
                    "total_files",
                    0
                )
            )
        }

    # ---------------------------------------------------------
    # TESTING PAGE
    # ---------------------------------------------------------

    def get_testing_data(self):

        testing = self.report.get(
            "testing",
            {}
        )

        executed = testing.get(
            "tests_executed",
            0
        )

        passed = testing.get(
            "tests_passed",
            0
        )

        failed = testing.get(
            "tests_failed",
            0
        )

        generated = testing.get(
            "tests_generated",
            0
        )

        if executed:
            success_rate = round(
                (passed / executed) * 100,
                2
            )
        else:
            success_rate = 0.0

        return {
            "generated": generated,
            "executed": executed,
            "passed": passed,
            "failed": failed,
            "success_rate": success_rate
        }

    # ---------------------------------------------------------
    # VERIFICATION PAGE
    # ---------------------------------------------------------

    def get_verification_data(self):

        verification = self.report.get(
            "verification",
            {}
        )

        return {
            "status": verification.get(
                "status",
                "UNKNOWN"
            ),

            "verdict": verification.get(
                "verdict",
                "NOT AVAILABLE"
            ),

            "regression": verification.get(
                "regression",
                False
            )
        }

    # ---------------------------------------------------------
    # AGENT PAGE
    # ---------------------------------------------------------

    def get_agent_data(self):

        if isinstance(self.report.get("agents"), dict):

            agents = self.report["agents"]

            registered = agents.get(
                "registered",
                agents.get(
                    "count",
                    0
                )
            )

        elif isinstance(self.report.get("agents"), list):

            registered = len(
                self.report["agents"]
            )

        else:

            registered = 0

        return {
            "registered": registered
        }

    # ---------------------------------------------------------
    # REPORT PAGE
    # ---------------------------------------------------------

    def get_report_data(self):

        return {
            "report_path": str(
                self.report_path
            ),

            "report_exists":
                self.report_path.exists(),

            "report": self.report
        }
