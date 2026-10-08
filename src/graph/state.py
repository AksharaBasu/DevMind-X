
from typing import TypedDict, List, Dict, Any


class DevMindGraphState(TypedDict, total=False):

    project_path: str

    project_analysis: Dict[str, Any]

    deep_analysis: Dict[str, Any]

    technology_analysis: Dict[str, Any]

    bug_findings: List[Dict[str, Any]]

    security_findings: List[Dict[str, Any]]

    performance_findings: List[Dict[str, Any]]

    test_targets: List[Dict[str, Any]]

    generated_tests: List[Dict[str, Any]]

    test_results: List[Dict[str, Any]]

    fixes: List[Dict[str, Any]]

    verification: Dict[str, Any]

    final_report: Dict[str, Any]

    status: str
