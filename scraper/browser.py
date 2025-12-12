from playwright.async_api import Playwright, BrowserContext, Page, Route
import os
from .constants.settings import (
    BROWSER_ARGS, 
    USER_AGENT, 
    FLIGHTS_PAGE_URL, 
    BLOCKED_DOMAINS, 
    BLOCKED_EXTENSIONS
)


async def create_browser_instance(playwright: Playwright) -> BrowserContext:
    brave_path = os.getenv(
        "BRAVE_EXECUTABLE_PATH", 
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
    )
    
    browser = await playwright.chromium.launch(
        headless=False,
        args=BROWSER_ARGS,
        executable_path=brave_path,
        ignore_default_args=['--disable-http-compression'],
        chromium_sandbox=False,
        handle_sigint=False,
        handle_sigterm=False,
        handle_sighup=False,
    )

    context = await browser.new_context(
        viewport={'width': 1280, 'height': 800},
        user_agent=USER_AGENT.strip(),
        locale='en-US',
        timezone_id='UTC',
        color_scheme='light',
        ignore_https_errors=True
    )

    return context


async def block_resources(route: Route) -> None:
    if any(route.request.url.endswith(ext) for ext in BLOCKED_EXTENSIONS):
        await route.abort()
    elif any(domain in route.request.url for domain in BLOCKED_DOMAINS):
        await route.abort()
    else:
        await route.continue_()


async def create_page_instance(context: BrowserContext) -> Page:
    page = await context.new_page()
    await page.route("**/*", block_resources)
    await page.goto(FLIGHTS_PAGE_URL, wait_until='domcontentloaded')
    return page
