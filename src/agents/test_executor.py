
import time
import traceback
from dataclasses import dataclass


@dataclass
class TestExecutionResult:
    test_name: str
    source_file: str
    status: str
    passed: bool
    output: str
    error: str
    execution_time: float


class TestExecutionAgent:

    def __init__(self, generated_tests=None):
        self.generated_tests = generated_tests or []
        self.results = []

    def execute_test(self, generated_test):

        start_time = time.time()

        test_name = getattr(
            generated_test,
            "test_name",
            getattr(generated_test, "name", "unknown_test")
        )

        source_file = getattr(
            generated_test,
            "source_file",
            getattr(generated_test, "file_path", "")
        )

        code = getattr(
            generated_test,
            "test_code",
            getattr(generated_test, "code", "")
        )

        if not code:

            return TestExecutionResult(
                test_name=test_name,
                source_file=source_file,
                status="FAILED",
                passed=False,
                output="",
                error="No executable test code",
                execution_time=time.time() - start_time
            )

        namespace = {
            "__name__": "__main__"
        }

        try:

            exec(code, namespace)

            result = TestExecutionResult(
                test_name=test_name,
                source_file=source_file,
                status="PASSED",
                passed=True,
                output="Test executed successfully",
                error="",
                execution_time=time.time() - start_time
            )

        except Exception:

            result = TestExecutionResult(
                test_name=test_name,
                source_file=source_file,
                status="FAILED",
                passed=False,
                output="",
                error=traceback.format_exc(),
                execution_time=time.time() - start_time
            )

        self.results.append(result)

        return result

    def execute_all(self):

        results = []

        for test in self.generated_tests:

            results.append(
                self.execute_test(test)
            )

        return results
