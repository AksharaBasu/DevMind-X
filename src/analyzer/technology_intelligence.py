
import os


class TechnologyIntelligence:

    def __init__(self, project_path):
        self.project_path = project_path

    def read_requirements(self):
        path = os.path.join(
            self.project_path,
            "requirements.txt"
        )

        if not os.path.exists(path):
            return []

        with open(path, "r", encoding="utf-8") as f:
            return [
                line.strip()
                for line in f
                if line.strip()
            ]

    def find_python_imports(self):
        imports = set()

        for root, _, files in os.walk(self.project_path):
            for filename in files:
                if filename.endswith(".py"):
                    path = os.path.join(root, filename)

                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            source = f.read()

                        import ast

                        tree = ast.parse(source)

                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    imports.add(alias.name)

                            elif isinstance(node, ast.ImportFrom):
                                if node.module:
                                    imports.add(node.module)

                    except Exception:
                        pass

        return sorted(imports)

    def detect_technologies(self):
        imports = self.find_python_imports()

        technologies = []

        mapping = {
            "django": "Django",
            "flask": "Flask",
            "fastapi": "FastAPI",
            "torch": "PyTorch",
            "tensorflow": "TensorFlow",
            "numpy": "NumPy",
            "pandas": "Pandas"
        }

        for name, technology in mapping.items():
            if any(name in item.lower() for item in imports):
                technologies.append(technology)

        return technologies

    def categorize(self):
        return {
            "web": self.detect_technologies(),
            "libraries": self.find_python_imports()
        }

    def analyze(self):
        return {
            "requirements": self.read_requirements(),
            "imports": self.find_python_imports(),
            "technologies": self.detect_technologies()
        }
