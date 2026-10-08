import ast
import json
import os
from datetime import datetime

from src.analyzer.project_analyzer import ProjectAnalyzer
from src.analyzer.deep_analyzer import DeepProjectAnalyzer
from src.analyzer.technology_intelligence import TechnologyIntelligence


class ProjectEngine:

    IGNORE_DIRS = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        "dist",
        "build",
    }

    def __init__(self, project_path):
        self.project_path = os.path.abspath(project_path)

        self.project_analyzer = ProjectAnalyzer(
            self.project_path
        )

        self.deep_analyzer = DeepProjectAnalyzer(
            self.project_path
        )

        self.technology_analyzer = TechnologyIntelligence(
            self.project_path
        )

    # ---------------------------------------------------------
    # FILE DISCOVERY
    # ---------------------------------------------------------

    def discover_python_files(self):
        files = []

        for root, dirs, filenames in os.walk(self.project_path):

            dirs[:] = [
                d for d in dirs
                if d not in self.IGNORE_DIRS
            ]

            for filename in filenames:

                if filename.endswith(".py"):

                    files.append(
                        os.path.join(root, filename)
                    )

        return sorted(files)

    # ---------------------------------------------------------
    # AST PARSING
    # ---------------------------------------------------------

    def parse_file(self, file_path):

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as f:

                source = f.read()

            return ast.parse(source)

        except Exception:

            return None

    # ---------------------------------------------------------
    # STRUCTURE ANALYSIS
    # ---------------------------------------------------------

    def count_structure(self, python_files):

        functions = 0
        classes = 0

        for file_path in python_files:

            tree = self.parse_file(file_path)

            if tree is None:
                continue

            for node in ast.walk(tree):

                if isinstance(
                    node,
                    (
                        ast.FunctionDef,
                        ast.AsyncFunctionDef
                    )
                ):

                    functions += 1

                elif isinstance(
                    node,
                    ast.ClassDef
                ):

                    classes += 1

        return functions, classes

    # ---------------------------------------------------------
    # BUG DETECTION
    # ---------------------------------------------------------

    def detect_bugs(self, python_files):

        findings = []

        for file_path in python_files:

            tree = self.parse_file(file_path)

            if tree is None:
                continue

            for node in ast.walk(tree):

                # Mutable default argument
                if isinstance(
                    node,
                    (
                        ast.FunctionDef,
                        ast.AsyncFunctionDef
                    )
                ):

                    defaults = list(node.args.defaults)

                    defaults += [
                        d
                        for d in node.args.kw_defaults
                        if d is not None
                    ]

                    for default in defaults:

                        if isinstance(
                            default,
                            (
                                ast.List,
                                ast.Dict,
                                ast.Set
                            )
                        ):

                            findings.append({
                                "type": "mutable_default_argument",
                                "severity": "HIGH",
                                "file": file_path,
                                "line": node.lineno,
                                "message":
                                    "Mutable default argument detected."
                            })

                # Bare except
                if isinstance(
                    node,
                    ast.ExceptHandler
                ):

                    if node.type is None:

                        findings.append({
                            "type": "bare_except",
                            "severity": "MEDIUM",
                            "file": file_path,
                            "line": node.lineno,
                            "message":
                                "Bare except detected."
                        })

                # eval
                if isinstance(
                    node,
                    ast.Call
                ):

                    if isinstance(
                        node.func,
                        ast.Name
                    ):

                        if node.func.id == "eval":

                            findings.append({
                                "type": "eval_usage",
                                "severity": "HIGH",
                                "file": file_path,
                                "line": node.lineno,
                                "message":
                                    "Use of eval() detected."
                            })

                        # exec
                        if node.func.id == "exec":

                            findings.append({
                                "type": "exec_usage",
                                "severity": "HIGH",
                                "file": file_path,
                                "line": node.lineno,
                                "message":
                                    "Use of exec() detected."
                            })

        return findings

    # ---------------------------------------------------------
    # SECURITY ANALYSIS
    # ---------------------------------------------------------

    def detect_security(self, python_files):

        findings = []

        sensitive_names = {
            "password",
            "passwd",
            "secret",
            "api_key",
            "apikey",
            "token",
            "access_key",
        }

        for file_path in python_files:

            tree = self.parse_file(file_path)

            if tree is None:
                continue

            for node in ast.walk(tree):

                # eval / exec
                if isinstance(
                    node,
                    ast.Call
                ):

                    if isinstance(
                        node.func,
                        ast.Name
                    ):

                        if node.func.id == "eval":

                            findings.append({
                                "type": "eval",
                                "severity": "HIGH",
                                "file": file_path,
                                "line": node.lineno,
                                "message":
                                    "Dynamic eval() execution."
                            })

                        elif node.func.id == "exec":

                            findings.append({
                                "type": "exec",
                                "severity": "HIGH",
                                "file": file_path,
                                "line": node.lineno,
                                "message":
                                    "Dynamic exec() execution."
                            })

                    # subprocess shell=True
                    if isinstance(
                        node.func,
                        ast.Attribute
                    ):

                        if node.func.attr in {
                            "run",
                            "call",
                            "Popen",
                            "check_output"
                        }:

                            for keyword in node.keywords:

                                if (
                                    keyword.arg == "shell"
                                    and
                                    isinstance(
                                        keyword.value,
                                        ast.Constant
                                    )
                                    and
                                    keyword.value.value is True
                                ):

                                    findings.append({
                                        "type": "shell_true",
                                        "severity": "HIGH",
                                        "file": file_path,
                                        "line": node.lineno,
                                        "message":
                                            "subprocess call uses shell=True."
                                    })

                # HTTP URLs
                if isinstance(
                    node,
                    ast.Constant
                ):

                    if (
                        isinstance(
                            node.value,
                            str
                        )
                        and
                        node.value.startswith(
                            "http://"
                        )
                    ):

                        findings.append({
                            "type": "insecure_http",
                            "severity": "MEDIUM",
                            "file": file_path,
                            "line": node.lineno,
                            "message":
                                "Unencrypted HTTP URL detected."
                        })

                # Hardcoded secrets
                if isinstance(
                    node,
                    ast.Assign
                ):

                    for target in node.targets:

                        if isinstance(
                            target,
                            ast.Name
                        ):

                            name = target.id.lower()

                            if any(
                                key in name
                                for key in sensitive_names
                            ):

                                if isinstance(
                                    node.value,
                                    ast.Constant
                                ):

                                    if isinstance(
                                        node.value.value,
                                        str
                                    ):

                                        findings.append({
                                            "type":
                                                "hardcoded_secret",
                                            "severity":
                                                "HIGH",
                                            "file":
                                                file_path,
                                            "line":
                                                node.lineno,
                                            "message":
                                                "Possible hardcoded secret."
                                        })

        return findings

    # ---------------------------------------------------------
    # PERFORMANCE ANALYSIS
    # ---------------------------------------------------------

    def detect_performance(self, python_files):

        findings = []

        for file_path in python_files:

            tree = self.parse_file(file_path)

            if tree is None:
                continue

            for node in ast.walk(tree):

                if isinstance(
                    node,
                    (
                        ast.For,
                        ast.While
                    )
                ):

                    for child in ast.walk(node):

                        if isinstance(
                            child,
                            ast.Call
                        ):

                            if isinstance(
                                child.func,
                                ast.Attribute
                            ):

                                if child.func.attr == "sort":

                                    findings.append({
                                        "type":
                                            "sort_inside_loop",
                                        "severity":
                                            "MEDIUM",
                                        "file":
                                            file_path,
                                        "line":
                                            child.lineno,
                                        "message":
                                            "Sorting inside a loop detected."
                                    })

                            elif isinstance(
                                child.func,
                                ast.Name
                            ):

                                if child.func.id == "sorted":

                                    findings.append({
                                        "type":
                                            "sorted_inside_loop",
                                        "severity":
                                            "MEDIUM",
                                        "file":
                                            file_path,
                                        "line":
                                            child.lineno,
                                        "message":
                                            "sorted() inside a loop detected."
                                    })

        return findings

    # ---------------------------------------------------------
    # TEST FILE DETECTION
    # ---------------------------------------------------------

    def detect_test_files(self, python_files):

        test_files = []

        for file_path in python_files:

            filename = os.path.basename(
                file_path
            ).lower()

            if (
                filename.startswith("test_")
                or
                filename.endswith("_test.py")
                or
                "test" in filename
            ):

                test_files.append(file_path)

        return test_files

    # ---------------------------------------------------------
    # REPORT
    # ---------------------------------------------------------

    def build_report(self):

        python_files = self.discover_python_files()

        functions, classes = self.count_structure(
            python_files
        )

        bugs = self.detect_bugs(
            python_files
        )

        security = self.detect_security(
            python_files
        )

        performance = self.detect_performance(
            python_files
        )

        test_files = self.detect_test_files(
            python_files
        )

        try:

            technology = (
                self.technology_analyzer.analyze()
            )

        except Exception:

            technology = {
                "requirements": [],
                "imports": [],
                "technologies": []
            }

        relative_files = []

        for path in python_files:

            relative_files.append(
                os.path.relpath(
                    path,
                    self.project_path
                )
            )

        report = {

            "project": {

                "name":
                    os.path.basename(
                        self.project_path
                    ),

                "path":
                    self.project_path,

                "total_files":
                    len(relative_files),

                "python_files":
                    len(python_files),

                "functions":
                    functions,

                "classes":
                    classes,

                "files":
                    relative_files
            },

            "technology": {

                "technologies":
                    technology.get(
                        "technologies",
                        []
                    ),

                "dependencies":
                    technology.get(
                        "imports",
                        []
                    ),

                "requirements":
                    technology.get(
                        "requirements",
                        []
                    )
            },

            "bugs": {

                "count":
                    len(bugs),

                "findings":
                    bugs
            },

            "security": {

                "count":
                    len(security),

                "findings":
                    security
            },

            "performance": {

                "count":
                    len(performance),

                "findings":
                    performance
            },

            "testing": {

                "test_file_count":
                    len(test_files),

                "test_files":
                    [
                        os.path.relpath(
                            f,
                            self.project_path
                        )
                        for f in test_files
                    ]
            },

            "metadata": {

                "generated_at":
                    datetime.now().isoformat(),

                "engine":
                    "DevMind-X ProjectEngine",

                "version":
                    "1.0"
            }
        }

        return report

    # ---------------------------------------------------------
    # SAVE REPORT
    # ---------------------------------------------------------

    def save_report(self, report):

        output_dir = os.path.join(
            self.project_path,
            ".devmind"
        )

        os.makedirs(
            output_dir,
            exist_ok=True
        )

        output_file = os.path.join(
            output_dir,
            "analysis_report.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                report,
                f,
                indent=4
            )

        return output_file

    # ---------------------------------------------------------
    # MAIN ENGINE
    # ---------------------------------------------------------

    def run(self):

        report = self.build_report()

        report_file = self.save_report(
            report
        )

        report["_report_file"] = report_file

        return report