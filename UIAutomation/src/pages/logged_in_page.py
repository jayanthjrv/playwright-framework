from playwright.async_api import Page


class LoggedInPage:
    def __init__(self, page: Page):
        self.page = page
        self.logout_link = page.get_by_role("link", name="Log out")

    async def logout(self) -> None:
        await self.logout_link.click()
