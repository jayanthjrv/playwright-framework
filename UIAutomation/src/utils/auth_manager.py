from pathlib import Path

from UIAutomation.src.pages.login_page import LoginPage
from utils.logger import get_logger

logger = get_logger(__name__)


class AuthManager:
    def __init__(
        self,
        worker_id: str = "main",
        storage_dir: str = "UIAutomation/.auth/auth-sessions",
    ):
        self.worker_id = worker_id
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def get_session_file(self) -> Path:
        return self.storage_dir / f"session_{self.worker_id}.json"

    async def load_or_login_session(self, browser):
        context_args = {"viewport": {"width": 1600, "height": 900}}
        session_file = self.get_session_file()
        if session_file.exists():
            context = await browser.new_context(
                storage_state=str(session_file), **context_args
            )
            context.set_default_navigation_timeout(120000)
            page = await context.new_page()
        else:
            context = await browser.new_context(**context_args)
            page = await context.new_page()
            context.set_default_navigation_timeout(120000)
            await self.login_to_practice_site(page)
            await context.storage_state(path=str(session_file))
        return context, page

    def clear_session(self):
        session_file = self.get_session_file()
        session_file.unlink(missing_ok=True)

    def clear_all_sessions(self):
        for session_file in self.storage_dir.glob("session_*.json"):
            session_file.unlink(missing_ok=True)

    @staticmethod
    async def login_to_practice_site(
        page,
        username: str = None,
        password: str = None,
    ):
        try:
            login_page = LoginPage(page)
            await login_page.login(username=username, password=password)
            logger.info("Login successful")
        except Exception:
            logger.exception("Login process failed")
            raise
