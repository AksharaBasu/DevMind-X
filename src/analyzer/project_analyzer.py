
import ast
import os


class ProjectAnalyzer:

    def __init__(self, project_path):
        self.project_path = project_path

    def scan_files(self):
        files = []

        for root, _, filenames in os.walk(self.project_path):
            for filename in filenames:
                files.append(
                    os.path.join(root, filename)
                )

        return files

    def analyze_python_file(self, file_path):
        result = {
            "file": file_path,
            "functions": 0,
            "classes": 0
        }

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())

            result["functions"] = sum(
                isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                for n in ast.walk(tree)
            )

            result["classes"] = sum(
                isinstance(n, ast.ClassDef)
                for n in ast.walk(tree)
            )

        except Exception:
            pass

        return result

    def detect_dependencies(self):
        return []

    def detect_entry_points(self):
        return []

    def analyze(self):
        files = self.scan_files()

        python_files = [
            f for f in files
            if f.endswith(".py")
        ]

        return {
            "project_path": self.project_path,
            "total_files": len(files),
            "python_files": len(python_files),
            "details": [
                self.analyze_python_file(f)
                for f in python_files
            ]
        }
