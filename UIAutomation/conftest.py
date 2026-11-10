import os
from datetime import datetime
from pathlib import Path
import pytest
from playwright.async_api import async_playwright

from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture
async def browser(request):
    browser_option = request.config.getoption("--browser") or ["chromium"]
    browser_name = (
        browser_option[0]
        if isinstance(browser_option, (list, tuple))
        else browser_option
    )
    channel_option = request.config.getoption("--browser-channel")
    browser_channel = (
        channel_option[0]
        if isinstance(channel_option, (list, tuple)) and channel_option
        else channel_option
    )
    browser_channel = browser_channel or (
        "chrome" if browser_name == "chromium" else None
    )

    assert browser_name in [
        "chromium",
        "firefox",
        "webkit",
    ], f"Unsupported browser: {browser_name}"
    assert browser_channel in [
        None,
        "chrome",
        "msedge",
    ], f"Unsupported browser channel: {browser_channel}"

    browser = None
    async with async_playwright() as p:
        browsers = {
            "chromium": p.chromium,
            "firefox": p.firefox,
            "webkit": p.webkit,
        }

        try:
            browser = await browsers[browser_name].launch(
                headless=is_headless(),
                channel=browser_channel,
                slow_mo=50,
                ignore_default_args=["--disable-extensions"],
            )
            yield browser
        except Exception as e:
            message = f"Failed to initialize browser session: {e}"
            raise RuntimeError(message) from e
        finally:
            if browser:
                await browser.close()


def is_headless() -> bool:
    return os.getenv("HEADLESS", "true").lower() == "true"


@pytest.fixture
async def page(browser, request):
    viewport = {"width": 1600, "height": 900}
    context = await browser.new_context(viewport=viewport)
    context.set_default_navigation_timeout(120000)
    page = await context.new_page()

    try:
        yield page
    except Exception as e:
        message = f"Failed to initialize page: {e}"
        raise RuntimeError(message) from e
    finally:
        call_report = getattr(request.node, "rep_call", None)
        if call_report and call_report.failed:
            await capture_failure_screenshot(page, request)
        await context.close()


async def capture_failure_screenshot(page, request):
    try:
        current_attempt = getattr(request.node, "execution_count", 1)
        max_attempts = 1 + getattr(request.config, "reruns", 0)

        if current_attempt >= max_attempts:
            screenshot_dir = Path("UIAutomation/screenshots/failures")
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            screenshot_name = f"{request.node.name}_{timestamp}.png"
            screenshot_path = screenshot_dir / screenshot_name
            await page.screenshot(path=str(screenshot_path))

    except Exception as e:
        logger.info("Failed to capture screenshot: %s", e)
