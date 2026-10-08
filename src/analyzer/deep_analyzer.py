
import ast
import os


class DeepProjectAnalyzer:

    def __init__(self, project_path):
        self.project_path = project_path

    def scan_files(self):
        files = []

        for root, _, filenames in os.walk(self.project_path):
            for filename in filenames:
                if filename.endswith(".py"):
                    files.append(os.path.join(root, filename))

        return files

    def analyze_python_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()

        tree = ast.parse(source)

        functions = []
        classes = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(node.name)

            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)

        return {
            "file": file_path,
            "functions": functions,
            "classes": classes
        }

    def detect_test_files(self):
        return [
            f for f in self.scan_files()
            if "test" in os.path.basename(f).lower()
        ]

    def detect_dependencies(self):
        dependencies = set()

        for file_path in self.scan_files():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            dependencies.add(alias.name)

                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            dependencies.add(node.module)

            except Exception:
                pass

        return sorted(dependencies)

    def detect_entry_points(self):
        return []

    def analyze(self):
        return {
            "files": [
                self.analyze_python_file(f)
                for f in self.scan_files()
            ],
            "test_files": self.detect_test_files(),
            "dependencies": self.detect_dependencies(),
            "entry_points": self.detect_entry_points()
        }
