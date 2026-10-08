
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
    return eval(expression)


def run_code(source):
    exec(source)


def fetch_data():
    response = requests.get("https://example.com")
    return response.text


def authenticate():
    password = os.getenv("APP_PASSWORD")

    if password is None:
        raise ValueError(
            "Application password is not configured"
        )

    return password
