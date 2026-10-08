
class ProjectRiskProfiler:

    def __init__(
        self,
        project_profile=None,
        technology_result=None
    ):
        self.project_profile = project_profile
        self.technology_result = technology_result

    def calculate_overall_risk(self):
        return "MEDIUM"

    def analyze(self):
        return {
            "overall_risk": self.calculate_overall_risk()
        }
