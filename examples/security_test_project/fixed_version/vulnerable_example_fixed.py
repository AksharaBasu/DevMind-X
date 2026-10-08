
import os
import subprocess
import requests


def execute_command(command, arguments):
    subprocess.run(
        [command] + arguments,
        shell=False,
        check=True
    )


def calculate(expression):
    allowed_operations = {
        "double": lambda value: value * 2,
        "square": lambda value: value * value
    }

    operation, value = expression

    if operation not in allowed_operations:
        raise ValueError("Unsupported operation")

    return allowed_operations[operation](value)


def run_code(source):
    raise ValueError(
        "Dynamic code execution is disabled"
    )


def fetch_data():
    response = requests.get("https://example.com")
    response.raise_for_status()
    return response.text


def authenticate():
    password = os.getenv("APP_PASSWORD")

    if password is None:
        raise ValueError(
            "Application password is not configured"
        )

    return password
