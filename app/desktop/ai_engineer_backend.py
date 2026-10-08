
import json
from pathlib import Path

from llm_provider import LLMProvider


class DevMindAIEngineer:

    """
    Real AI Engineering Assistant.

    Pipeline:

        Engineering Data
              ↓
        Verified Context
              ↓
        LLM
              ↓
        Engineering Answer
    """

    def __init__(self):

        self.project_root = (
            Path(__file__).resolve().parents[2]
        )

        self.data_file = (
            self.project_root
            / "reports"
            / "desktop_engineering_data.json"
        )

        self.data = {}

        self.llm = LLMProvider()

        self.load_data()

    # ==============================================================
    # LOAD ENGINEERING DATA
    # ==============================================================

    def load_data(self):

        if not self.data_file.exists():

            self.data = {}

            return

        with open(
            self.data_file,
            "r",
            encoding="utf-8"
        ) as file:

            self.data = json.load(file)

    # ==============================================================
    # ENGINEERING CONTEXT
    # ==============================================================

    def get_context(self):

        self.load_data()

        return {

            "bugs": self.data.get(
                "bugs",
                {}
            ),

            "security": self.data.get(
                "security",
                {}
            ),

            "performance": self.data.get(
                "performance",
                {}
            ),

            "testing": self.data.get(
                "testing",
                {}
            )
        }

    # ==============================================================
    # BUILD LLM CONTEXT
    # ==============================================================

    def build_llm_context(self):

        context = self.get_context()

        bugs = context["bugs"]
        security = context["security"]
        performance = context["performance"]
        testing = context["testing"]

        return f"""
VERIFIED DEVMIND-X ENGINEERING STATE

BUG INTELLIGENCE
================

Findings detected:
{bugs.get("findings_detected", 0)}

Confirmed:
{bugs.get("confirmed", 0)}

Likely:
{bugs.get("likely", 0)}

Fixes generated:
{bugs.get("fixes_generated", 0)}

Findings after fix:
{bugs.get("findings_after_fix", 0)}

Regression:
{bugs.get("regression", False)}


SECURITY INTELLIGENCE
=====================

Vulnerabilities detected:
{security.get("vulnerabilities_detected", 0)}

Recommendations generated:
{security.get("recommendations_generated", 0)}

Vulnerabilities after remediation:
{security.get("vulnerabilities_after_fix", 0)}


PERFORMANCE INTELLIGENCE
========================

Issues before optimization:
{performance.get("issues_before_fix", 0)}

False positive removed:
{performance.get("false_positive_removed", False)}

Issues after optimization:
{performance.get("issues_after_fix", 0)}

Optimized version passed:
{performance.get("optimized_version_passed", False)}


TEST INTELLIGENCE
=================

Tests generated:
{testing.get("generated", 0)}

Tests executed:
{testing.get("executed", 0)}

Tests passed:
{testing.get("passed", 0)}

Tests failed:
{testing.get("failed", 0)}
"""

    # ==============================================================
    # SYSTEM PROMPT
    # ==============================================================

    def build_system_prompt(self):

        return """
You are DevMind-X AI Engineer.

You are an autonomous software engineering assistant.

Your job is to help developers understand and improve
software projects.

You have access to VERIFIED engineering results produced
by the DevMind-X analysis pipeline.

IMPORTANT RULES:

1. Use the provided engineering context.
2. Do not invent test results.
3. Do not invent vulnerabilities.
4. Do not claim a bug was fixed unless the context supports it.
5. Clearly distinguish verified facts from suggestions.
6. Give technically useful answers.
7. When recommending a fix, explain why.
8. When discussing security, prioritize safe practices.
9. When discussing tests, use the actual test results.
10. Keep answers concise but useful.

You are not a generic chatbot.

You are a software engineering intelligence assistant.
"""

    # ==============================================================
    # REAL LLM QUESTION
    # ==============================================================

    def ask(self, question):

        if not question:

            return {
                "success": False,
                "answer": (
                    "Please enter an engineering question."
                )
            }

        context = self.build_llm_context()

        user_prompt = f"""
Here is the verified DevMind-X engineering context:

{context}

Developer question:

{question}

Answer the developer using the verified context.
If the context does not contain enough information,
say that clearly instead of inventing details.
"""

        result = self.llm.chat(
            self.build_system_prompt(),
            user_prompt
        )

        return result

    # ==============================================================
    # PROVIDER STATUS
    # ==============================================================

    def provider_status(self):

        return self.llm.status()
