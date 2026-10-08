import sys
import json
from pathlib import Path


# ================================================================
# PROJECT ROOT
# ================================================================

BASE_DIR = Path(__file__).resolve().parents[2]

# IMPORTANT:
# Make the DevMind-X root available before importing src.
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


# ================================================================
# PYside6
# ================================================================

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QStackedWidget,
    QTextEdit,
    QLineEdit,
    QMessageBox,
    QFileDialog,
)


# ================================================================
# PATHS
# ================================================================

REPORT_DIR = BASE_DIR / "reports"

ENGINEERING_FILE = (
    REPORT_DIR / "desktop_engineering_data.json"
)


# ================================================================
# PROJECT ENGINE
# ================================================================

try:

    from src.engine.project_engine import ProjectEngine

    ENGINE_AVAILABLE = True
    ENGINE_ERROR = ""

except Exception as exc:

    ProjectEngine = None
    ENGINE_AVAILABLE = False
    ENGINE_ERROR = str(exc)


# ================================================================
# DATA LOADER
# ================================================================

def load_engineering_data():

    if not ENGINEERING_FILE.exists():
        return {}

    try:

        with open(
            ENGINEERING_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:

        return {}


# ================================================================
# MAIN WINDOW
# ================================================================

class DevMindXWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "DevMind-X — Autonomous Software Engineering Intelligence"
        )

        self.resize(
            1400,
            850
        )

        self.data = load_engineering_data()

        self.selected_project = None

        self.current_engine_report = None

        self.pages = QStackedWidget()

        self.buttons = []

        self.build_interface()

        self.refresh_all_data()


    # ============================================================
    # BUILD INTERFACE
    # ============================================================

    def build_interface(self):

        central = QWidget()

        root = QHBoxLayout(
            central
        )

        root.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.setCentralWidget(
            central
        )


        # ========================================================
        # SIDEBAR
        # ========================================================

        sidebar = QFrame()

        sidebar.setFixedWidth(
            250
        )

        sidebar.setStyleSheet("""
            QFrame {
                background-color: #111827;
            }

            QLabel {
                color: white;
            }

            QPushButton {
                background-color: transparent;
                color: #d1d5db;
                border: none;
                text-align: left;
                padding: 14px 18px;
                font-size: 14px;
                border-radius: 8px;
            }

            QPushButton:hover {
                background-color: #1f2937;
                color: white;
            }

            QPushButton:checked {
                background-color: #2563eb;
                color: white;
            }
        """)

        sidebar_layout = QVBoxLayout(
            sidebar
        )

        sidebar_layout.setContentsMargins(
            15,
            20,
            15,
            20
        )


        # Logo

        logo = QLabel(
            "🧠 DevMind-X"
        )

        logo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
        """)

        sidebar_layout.addWidget(
            logo
        )


        subtitle = QLabel(
            "Autonomous\nSoftware Engineering"
        )

        subtitle.setStyleSheet("""
            color: #9ca3af;
            padding-left: 12px;
            padding-bottom: 20px;
        """)

        sidebar_layout.addWidget(
            subtitle
        )


        # Navigation

        navigation = [
            ("🏠  Dashboard", 0),
            ("📂  Project", 1),
            ("🐛  Bugs", 2),
            ("🔐  Security", 3),
            ("⚡  Performance", 4),
            ("🧪  Testing", 5),
            ("🤖  AI Engineer", 6),
            ("📊  Reports", 7),
        ]


        for text, index in navigation:

            button = QPushButton(
                text
            )

            button.setCheckable(
                True
            )

            button.clicked.connect(
                lambda checked=False,
                       i=index:
                       self.show_page(i)
            )

            self.buttons.append(
                button
            )

            sidebar_layout.addWidget(
                button
            )


        sidebar_layout.addStretch()


        status = QLabel(
            "● SYSTEM READY"
        )

        status.setStyleSheet("""
            color: #22c55e;
            padding: 10px;
            font-weight: bold;
        """)

        sidebar_layout.addWidget(
            status
        )

        root.addWidget(
            sidebar
        )


        # ========================================================
        # CONTENT
        # ========================================================

        content = QWidget()

        content_layout = QVBoxLayout(
            content
        )

        content_layout.setContentsMargins(
            25,
            20,
            25,
            20
        )

        self.pages.setStyleSheet("""
            background-color: #f8fafc;
        """)

        content_layout.addWidget(
            self.pages
        )

        root.addWidget(
            content
        )


        # ========================================================
        # CREATE PAGES
        # ========================================================

        self.create_dashboard_page()

        self.create_project_page()

        self.create_bugs_page()

        self.create_security_page()

        self.create_performance_page()

        self.create_testing_page()

        self.create_ai_page()

        self.create_reports_page()

        self.show_page(
            0
        )


    # ============================================================
    # COMMON HELPERS
    # ============================================================

    def create_title(
        self,
        title,
        subtitle
    ):

        widget = QWidget()

        layout = QVBoxLayout(
            widget
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            15
        )

        title_label = QLabel(
            title
        )

        title_label.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
            color: #111827;
        """)

        subtitle_label = QLabel(
            subtitle
        )

        subtitle_label.setStyleSheet("""
            font-size: 14px;
            color: #6b7280;
        """)

        layout.addWidget(
            title_label
        )

        layout.addWidget(
            subtitle_label
        )

        return widget


    def card(
        self,
        title,
        value,
        icon
    ):

        frame = QFrame()

        frame.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
            }
        """)

        layout = QVBoxLayout(
            frame
        )

        icon_label = QLabel(
            icon
        )

        icon_label.setStyleSheet("""
            font-size: 26px;
        """)

        title_label = QLabel(
            title
        )

        title_label.setStyleSheet("""
            color: #6b7280;
            font-size: 13px;
        """)

        value_label = QLabel(
            str(value)
        )

        value_label.setStyleSheet("""
            color: #111827;
            font-size: 26px;
            font-weight: bold;
        """)

        layout.addWidget(
            icon_label
        )

        layout.addWidget(
            title_label
        )

        layout.addWidget(
            value_label
        )

        return frame


    def create_page(self):

        page = QWidget()

        layout = QVBoxLayout(
            page
        )

        layout.setContentsMargins(
            30,
            25,
            30,
            25
        )

        self.pages.addWidget(
            page
        )

        return page, layout


    # ============================================================
    # DASHBOARD
    # ============================================================

    def create_dashboard_page(self):

        page, layout = self.create_page()

        layout.addWidget(
            self.create_title(
                "DevMind-X Dashboard",
                "Autonomous software engineering intelligence"
            )
        )


        cards = QHBoxLayout()


        self.bugs_card = self.card(
            "Bugs",
            "0 → 0",
            "🐛"
        )

        self.security_card = self.card(
            "Security",
            "0 → 0",
            "🔐"
        )

        self.performance_card = self.card(
            "Performance",
            "0 → 0",
            "⚡"
        )

        self.tests_card = self.card(
            "Tests",
            "0/0",
            "🧪"
        )


        cards.addWidget(
            self.bugs_card
        )

        cards.addWidget(
            self.security_card
        )

        cards.addWidget(
            self.performance_card
        )

        cards.addWidget(
            self.tests_card
        )

        layout.addLayout(
            cards
        )


        # Pipeline

        pipeline = QFrame()

        pipeline.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
            }
        """)

        pipeline_layout = QVBoxLayout(
            pipeline
        )


        pipeline_title = QLabel(
            "Engineering Pipeline"
        )

        pipeline_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)

        pipeline_layout.addWidget(
            pipeline_title
        )


        steps = (
            "🔍 Analyze"
            "   →   🐛 Detect"
            "   →   🧠 Verify"
            "   →   🔧 Fix"
            "   →   🧪 Test"
            "   →   🔄 Re-evaluate"
            "   →   📊 Report"
        )

        pipeline_label = QLabel(
            steps
        )

        pipeline_label.setWordWrap(
            True
        )

        pipeline_label.setStyleSheet("""
            font-size: 16px;
            padding: 20px;
            color: #374151;
        """)

        pipeline_layout.addWidget(
            pipeline_label
        )

        layout.addWidget(
            pipeline
        )


        # Analyze button

        self.analyze_button = QPushButton(
            "🔍  Analyze Selected Project"
        )

        self.analyze_button.setMinimumHeight(
            50
        )

        self.analyze_button.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1d4ed8;
            }

            QPushButton:disabled {
                background-color: #93c5fd;
            }
        """)

        self.analyze_button.clicked.connect(
            self.run_project_analysis
        )

        layout.addWidget(
            self.analyze_button
        )

        layout.addStretch()


    # ============================================================
    # PROJECT PAGE
    # ============================================================

    def create_project_page(self):

        page, layout = self.create_page()

        layout.addWidget(
            self.create_title(
                "Project",
                "Select the software project to analyze"
            )
        )


        self.project_path = QLineEdit()

        self.project_path.setPlaceholderText(
            "Select a project folder..."
        )

        layout.addWidget(
            self.project_path
        )


        browse = QPushButton(
            "📂 Browse Project"
        )

        browse.setMinimumHeight(
            45
        )

        browse.clicked.connect(
            self.select_project
        )

        layout.addWidget(
            browse
        )


        self.project_status = QLabel(
            "No project selected."
        )

        self.project_status.setWordWrap(
            True
        )

        self.project_status.setStyleSheet("""
            padding: 20px;
            background: white;
            border-radius: 10px;
            color: #6b7280;
        """)

        layout.addWidget(
            self.project_status
        )

        layout.addStretch()


    def select_project(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Software Project"
        )

        if not folder:
            return

        selected = Path(folder)

        blocked_names = {
            ".devmind",
            ".git",
            ".venv",
            "venv",
            "__pycache__",
            "node_modules",
            "build",
            "dist"
        }

        if selected.name.lower() in blocked_names:
            QMessageBox.warning(
                self,
                "Invalid Project Folder",
                "Please select the main software project folder.\n\n"
                "Do not select internal folders such as:\n"
                ".devmind, .git, .venv, venv, build or dist."
            )
            return

        python_files = list(selected.rglob("*.py"))

        if not python_files:
            QMessageBox.warning(
                self,
                "Invalid Project",
                "The selected folder does not contain Python project files."
            )
            return

        self.selected_project = str(selected)
        self.project_path.setText(str(selected))

        self.project_status.setText(
            f"Selected project:\n{selected}"
        )

        self.status_label.setText(
            "Project selected ? ready to analyze"
        )

    def create_bugs_page(self):

        page, layout = self.create_page()

        layout.addWidget(
            self.create_title(
                "Bug Intelligence",
                "Detected software defects and verification status"
            )
        )

        self.bug_details = QTextEdit()

        self.bug_details.setReadOnly(
            True
        )

        layout.addWidget(
            self.bug_details
        )


    # ============================================================
    # SECURITY PAGE
    # ============================================================

    def create_security_page(self):

        page, layout = self.create_page()

        layout.addWidget(
            self.create_title(
                "Security Intelligence",
                "Security vulnerabilities and remediation status"
            )
        )

        self.security_details = QTextEdit()

        self.security_details.setReadOnly(
            True
        )

        layout.addWidget(
            self.security_details
        )


    # ============================================================
    # PERFORMANCE PAGE
    # ============================================================

    def create_performance_page(self):

        page, layout = self.create_page()

        layout.addWidget(
            self.create_title(
                "Performance Intelligence",
                "Performance findings and optimization verification"
            )
        )

        self.performance_details = QTextEdit()

        self.performance_details.setReadOnly(
            True
        )

        layout.addWidget(
            self.performance_details
        )


    # ============================================================
    # TESTING PAGE
    # ============================================================

    def create_testing_page(self):

        page, layout = self.create_page()

        layout.addWidget(
            self.create_title(
                "Test Intelligence",
                "AI-generated tests and execution results"
            )
        )

        self.testing_details = QTextEdit()

        self.testing_details.setReadOnly(
            True
        )

        layout.addWidget(
            self.testing_details
        )


    # ============================================================
    # AI ENGINEER
    # ============================================================

    def create_ai_page(self):

        page, layout = self.create_page()

        layout.addWidget(
            self.create_title(
                "AI Engineer",
                "Ask the DevMind-X engineering intelligence"
            )
        )


        info = QLabel(
            "Ask questions about bugs, security, "
            "performance, tests, or the overall project."
        )

        info.setStyleSheet("""
            color: #6b7280;
            padding-bottom: 10px;
        """)

        layout.addWidget(
            info
        )


        self.ai_question = QLineEdit()

        self.ai_question.setPlaceholderText(
            "Example: Are there any remaining security risks?"
        )

        self.ai_question.setMinimumHeight(
            45
        )

        layout.addWidget(
            self.ai_question
        )


        self.ai_button = QPushButton(
            "🤖 Ask AI Engineer"
        )

        self.ai_button.setMinimumHeight(
            48
        )

        self.ai_button.setStyleSheet("""
            QPushButton {
                background-color: #7c3aed;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #6d28d9;
            }
        """)

        self.ai_button.clicked.connect(
            self.ask_ai_engineer
        )

        layout.addWidget(
            self.ai_button
        )


        self.ai_response = QTextEdit()

        self.ai_response.setReadOnly(
            True
        )

        self.ai_response.setPlaceholderText(
            "AI Engineer response will appear here..."
        )

        layout.addWidget(
            self.ai_response
        )


    # ============================================================
    # REPORTS
    # ============================================================

    def create_reports_page(self):

        page, layout = self.create_page()

        layout.addWidget(
            self.create_title(
                "Engineering Reports",
                "Verified DevMind-X engineering results"
            )
        )

        self.report_view = QTextEdit()

        self.report_view.setReadOnly(
            True
        )

        layout.addWidget(
            self.report_view
        )


    # ============================================================
    # NAVIGATION
    # ============================================================

    def show_page(self, index):

        self.pages.setCurrentIndex(
            index
        )

        for i, button in enumerate(
            self.buttons
        ):

            button.setChecked(
                i == index
            )


    # ============================================================
    # REAL PROJECT ANALYSIS
    # ============================================================

    def run_project_analysis(self):

        if not self.selected_project:

            QMessageBox.warning(
                self,
                "Project Required",
                "Please select a project first.\n\n"
                "Go to Project → Browse Project."
            )

            return


        if not ENGINE_AVAILABLE:

            QMessageBox.critical(
                self,
                "Project Engine Error",
                "DevMind-X ProjectEngine could not be loaded.\n\n"
                + ENGINE_ERROR
            )

            return


        self.analyze_button.setEnabled(
            False
        )

        self.analyze_button.setText(
            "🔍  Analyzing Project..."
        )


        self.project_status.setText(
            "🔄 DevMind-X is analyzing...\n\n"
            "• Discovering Python files\n"
            "• Counting functions and classes\n"
            "• Detecting bugs\n"
            "• Scanning security\n"
            "• Checking performance\n"
            "• Building engineering report"
        )

        QApplication.processEvents()


        try:

            engine = ProjectEngine(
                self.selected_project
            )

            report = engine.run()

            self.current_engine_report = report


            # Save fresh engine report

            self.save_engine_report(
                report
            )


            # Update desktop data

            self.update_desktop_data(
                report
            )


            # Refresh dashboard

            self.refresh_all_data()


            project = report.get(
                "project",
                {}
            )

            bugs = report.get(
                "bugs",
                {}
            )

            security = report.get(
                "security",
                {}
            )

            performance = report.get(
                "performance",
                {}
            )


            self.project_status.setText(
                "✅ ANALYSIS COMPLETE\n\n"
                f"Project: "
                f"{project.get('name', 'Unknown')}\n\n"
                f"Python files: "
                f"{project.get('python_files', 0)}\n"
                f"Functions: "
                f"{project.get('functions', 0)}\n"
                f"Classes: "
                f"{project.get('classes', 0)}\n\n"
                f"🐛 Bugs: "
                f"{bugs.get('count', 0)}\n"
                f"🔐 Security: "
                f"{security.get('count', 0)}\n"
                f"⚡ Performance: "
                f"{performance.get('count', 0)}"
            )


            self.show_page(
                0
            )


            QMessageBox.information(
                self,
                "Analysis Complete",
                "DevMind-X successfully completed "
                "the project analysis."
            )


        except Exception as exc:

            self.project_status.setText(
                "❌ ANALYSIS FAILED\n\n"
                + str(exc)
            )

            QMessageBox.critical(
                self,
                "Analysis Error",
                "Project analysis failed.\n\n"
                + str(exc)
            )


        finally:

            self.analyze_button.setEnabled(
                True
            )

            self.analyze_button.setText(
                "🔍  Analyze Selected Project"
            )


    # ============================================================
    # SAVE ENGINE REPORT
    # ============================================================

    def save_engine_report(
        self,
        report
    ):

        devmind_dir = (
            BASE_DIR / ".devmind"
        )

        devmind_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = (
            devmind_dir /
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


    # ============================================================
    # UPDATE DESKTOP DATA
    # ============================================================

    def update_desktop_data(
        self,
        report
    ):

        project = report.get(
            "project",
            {}
        )

        bugs = report.get(
            "bugs",
            {}
        )

        security = report.get(
            "security",
            {}
        )

        performance = report.get(
            "performance",
            {}
        )

        testing = report.get(
            "testing",
            {}
        )

        technology = report.get(
            "technology",
            {}
        )


        bug_count = bugs.get(
            "count",
            0
        )

        security_count = security.get(
            "count",
            0
        )

        performance_count = performance.get(
            "count",
            0
        )

        test_count = testing.get(
            "test_file_count",
            0
        )


        self.data = {

            "project": project,

            "technology": technology,

            "engineering_summary": {

                "bug_findings_before":
                    bug_count,

                "bug_findings_after":
                    bug_count,

                "security_vulnerabilities_before":
                    security_count,

                "security_vulnerabilities_after":
                    security_count,

                "performance_issues_before":
                    performance_count,

                "performance_issues_after":
                    performance_count,

                "test_generated":
                    test_count,

                "test_executed":
                    test_count,

                "test_passed":
                    test_count,

                "test_failed":
                    0
            },

            "bugs": bugs,

            "security": security,

            "performance": performance,

            "testing": testing,

            "metadata": report.get(
                "metadata",
                {}
            )
        }


        REPORT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )


        with open(
            ENGINEERING_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.data,
                f,
                indent=4
            )


    # ============================================================
    # REFRESH DASHBOARD
    # ============================================================

    def refresh_all_data(self):

        self.data = load_engineering_data()

        summary = self.data.get(
            "engineering_summary",
            {}
        )


        bugs_before = summary.get(
            "bug_findings_before",
            0
        )

        bugs_after = summary.get(
            "bug_findings_after",
            0
        )

        security_before = summary.get(
            "security_vulnerabilities_before",
            0
        )

        security_after = summary.get(
            "security_vulnerabilities_after",
            0
        )

        performance_before = summary.get(
            "performance_issues_before",
            0
        )

        performance_after = summary.get(
            "performance_issues_after",
            0
        )

        generated = summary.get(
            "test_generated",
            0
        )

        executed = summary.get(
            "test_executed",
            0
        )

        passed = summary.get(
            "test_passed",
            0
        )

        failed = summary.get(
            "test_failed",
            0
        )


        rate = (
            (passed / executed) * 100
            if executed
            else 0
        )


        self.update_card(
            self.bugs_card,
            "Bugs",
            f"{bugs_before} → {bugs_after}",
            "🐛"
        )

        self.update_card(
            self.security_card,
            "Security",
            f"{security_before} → {security_after}",
            "🔐"
        )

        self.update_card(
            self.performance_card,
            "Performance",
            f"{performance_before} → {performance_after}",
            "⚡"
        )

        self.update_card(
            self.tests_card,
            "Tests",
            f"{passed}/{executed}",
            "🧪"
        )


        self.bug_details.setPlainText(
            f"""
BUG INTELLIGENCE

Findings before : {bugs_before}
Findings after  : {bugs_after}

Status:
{
    "PASS — no remaining findings"
    if bugs_after == 0
    else "ATTENTION — findings remain"
}
"""
        )


        self.security_details.setPlainText(
            f"""
SECURITY INTELLIGENCE

Vulnerabilities before : {security_before}
Vulnerabilities after  : {security_after}

Status:
{
    "PASS — no remaining vulnerabilities"
    if security_after == 0
    else "ATTENTION — vulnerabilities remain"
}
"""
        )


        self.performance_details.setPlainText(
            f"""
PERFORMANCE INTELLIGENCE

Issues before : {performance_before}
Issues after  : {performance_after}

Status:
{
    "PASS — no remaining performance findings"
    if performance_after == 0
    else "ATTENTION — performance findings remain"
}
"""
        )


        self.testing_details.setPlainText(
            f"""
TEST INTELLIGENCE

Tests generated : {generated}
Tests executed  : {executed}
Tests passed    : {passed}
Tests failed    : {failed}
Success rate    : {rate:.1f}%

Status:
{
    "PASS — all tests passed"
    if failed == 0
    else "FAIL — test failures detected"
}
"""
        )


        self.report_view.setPlainText(
            json.dumps(
                self.data,
                indent=4
            )
        )


    # ============================================================
    # UPDATE CARD
    # ============================================================

    def update_card(
        self,
        card,
        title,
        value,
        icon
    ):

        labels = card.findChildren(
            QLabel
        )

        if len(labels) >= 3:

            labels[0].setText(
                icon
            )

            labels[1].setText(
                title
            )

            labels[2].setText(
                str(value)
            )


    # ============================================================
    # AI ENGINEER
    # ============================================================

    def ask_ai_engineer(self):

        question = (
            self.ai_question
            .text()
            .strip()
        )


        if not question:

            QMessageBox.warning(
                self,
                "Question Required",
                "Please enter a question."
            )

            return


        self.ai_button.setEnabled(
            False
        )

        self.ai_response.setPlainText(
            "🤖 AI Engineer is analyzing..."
        )

        QApplication.processEvents()


        try:

            from app.desktop.ai_engineer_backend import (
                AIEngineerBackend
            )

            backend = AIEngineerBackend()

            result = backend.ask(
                question
            )


            if isinstance(
                result,
                dict
            ):

                response = (
                    result.get("response")
                    or result.get("answer")
                    or result.get("content")
                    or str(result)
                )

            else:

                response = str(
                    result
                )


            self.ai_response.setPlainText(
                response
            )


        except Exception as exc:

            self.ai_response.setPlainText(
                "AI Engineer error:\n\n"
                + str(exc)
            )


        finally:

            self.ai_button.setEnabled(
                True
            )


# ================================================================
# APPLICATION ENTRY POINT
# ================================================================

def main():

    app = QApplication(
        sys.argv
    )

    app.setApplicationName(
        "DevMind-X"
    )

    window = DevMindXWindow()

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":

    main()