
import ast
import os


class PerformanceIntelligenceAgent:

    def __init__(self, project_path):
        self.project_path = project_path

    def scan_files(self):
        files = []

        if not os.path.exists(self.project_path):
            return files

        for root, _, filenames in os.walk(self.project_path):
            for filename in filenames:
                if filename.endswith(".py"):
                    files.append(os.path.join(root, filename))

        return files

    def analyze_python_file(self, file_path):
        if not os.path.exists(file_path):
            return {
                "file": file_path,
                "functions": [],
                "complexity": 0
            }

        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()

        tree = ast.parse(source)

        functions = [
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]

        return {
            "file": file_path,
            "functions": functions,
            "complexity": len(functions)
        }

    def analyze(self):
        files = self.scan_files()

        results = []

        for file_path in files:
            results.append(
                self.analyze_python_file(file_path)
            )

        return {
            "project_path": self.project_path,
            "files": results
        }
