from playwright.async_api import Page

from UIAutomation.src.utils.environment_configuration import (
    login_password,
    login_url,
    login_username,
)


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.submit_button = page.locator("#submit")
        self.error_message = page.locator("#error")

    async def login(self, username: str = None, password: str = None) -> None:
        await self.page.goto(login_url())
        await self.username_input.fill(username or login_username())
        await self.password_input.fill(password or login_password())
        await self.submit_button.click()
