
from pathlib import Path
import json


class DevMindDashboardBackend:

    """
    Reads the real DevMind-X engineering report
    and exposes dashboard-ready information.
    """

    def __init__(
        self,
        project_root
    ):

        self.project_root = Path(
            project_root
        )

        self.report_file = (
            self.project_root /
            "reports" /
            "devmind_x_final_report.json"
        )


    def load_report(self):

        if not self.report_file.exists():

            raise FileNotFoundError(
                f"Report not found: {self.report_file}"
            )

        with open(
            self.report_file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)


    def dashboard_data(self):

        report = self.load_report()

        testing = report.get(
            "testing",
            {}
        )

        verification = report.get(
            "verification",
            {}
        )

        project = report.get(
            "project",
            {}
        )

        agents = report.get(
            "agents",
            {}
        )


        return {

            "project": {

                "path":
                    project.get(
                        "path",
                        ""
                    ),

                "python_files":
                    project.get(
                        "python_files",
                        0
                    )
            },


            "testing": {

                "tests_generated":
                    testing.get(
                        "tests_generated",
                        0
                    ),

                "tests_executed":
                    testing.get(
                        "tests_executed",
                        0
                    ),

                "tests_passed":
                    testing.get(
                        "tests_passed",
                        0
                    ),

                "tests_failed":
                    testing.get(
                        "tests_failed",
                        0
                    ),

                "success_rate":
                    testing.get(
                        "success_rate",
                        0
                    )
            },


            "verification": {

                "final_verdict":
                    verification.get(
                        "final_verdict",
                        "UNKNOWN"
                    ),

                "regression_detected":
                    verification.get(
                        "regression_detected",
                        False
                    ),

                "critic_enabled":
                    verification.get(
                        "critic_enabled",
                        False
                    ),

                "fix_validation":
                    verification.get(
                        "fix_validation",
                        False
                    ),

                "regression_testing":
                    verification.get(
                        "regression_testing",
                        False
                    )
            },


            "agents": agents
        }
