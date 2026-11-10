import pytest
from playwright.async_api import expect

from UIAutomation.src.pages.logged_in_page import LoggedInPage
from UIAutomation.src.pages.login_page import LoginPage


@pytest.mark.smoke
@pytest.mark.description("A valid user can log in successfully")
async def test_login_happy_path(page):
    await LoginPage(page).login()

    await expect(
        page.get_by_role("heading", name="Logged In Successfully")
    ).to_be_visible()
    await expect(LoggedInPage(page).logout_link).to_be_visible()
    assert page.url.endswith("/logged-in-successfully/")


@pytest.mark.description("Invalid username shows the error message")
async def test_invalid_username_shows_error(page):
    login_page = LoginPage(page)
    await login_page.login(username="incorrectUser", password="Password123")

    expected_error = "Your username is invalid!"
    await expect(login_page.error_message).to_have_text(expected_error)


@pytest.mark.description("Invalid password shows the error message")
async def test_invalid_password_shows_error(page):
    login_page = LoginPage(page)
    await login_page.login(username="student", password="incorrectPassword")

    expected_error = "Your password is invalid!"
    await expect(login_page.error_message).to_have_text(expected_error)


@pytest.mark.description("Logging out returns the user to the login page")
async def test_logout_returns_to_login_page(page):
    login_page = LoginPage(page)
    await login_page.login()
    await LoggedInPage(page).logout()

    await expect(page).to_have_url(
        "https://practicetestautomation.com/practice-test-login/"
    )
    await expect(login_page.username_input).to_be_visible()
    await expect(login_page.password_input).to_be_visible()
