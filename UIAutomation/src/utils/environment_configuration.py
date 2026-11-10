import os


def login_url() -> str:
    url = os.getenv("LOGIN_URL")
    if not url:
        raise ValueError("LOGIN_URL is not set in the environment")
    return url


def login_username() -> str:
    username = os.getenv("LOGIN_USERNAME")
    if not username:
        raise ValueError("LOGIN_USERNAME is not set in the environment")
    return username


def login_password() -> str:
    password = os.getenv("LOGIN_PASSWORD")
    if not password:
        raise ValueError("LOGIN_PASSWORD is not set in the environment")
    return password
