from .constants.selectors import (
    RESULTS_SELECTORS,
    ADD_FLIGHT_BUTTON_SELECTOR,
    ADULT_PER_INFANTS_ON_LAP_ERROR_SELECTOR,
    NO_FLIGHTS_ERROR_SELECTOR,
    FLIGHTS_SELECTOR
)

from playwright.async_api import Page, ElementHandle, Locator
from .errors import AdultPerInfantsOnLapError, NoFlightsFoundError


async def process_flight(page: ElementHandle) -> dict:
    flight_info = {}

    for key, selector in RESULTS_SELECTORS.items():
        element = await page.query_selector(selector)
        flight_info[key] = await element.text_content() if element else None

    return flight_info


async def process_date_selectors(page: Page, date_selector_type: str, date: str) -> None:
    date_input = page.locator(date_selector_type).first
    await date_input.fill(date)
    await date_input.press("Enter")


async def process_flight_selectors(page: Page, flight_selector: str, value: str) -> None:
    flight_input = page.locator(flight_selector).first
    await flight_input.fill(value)
    await page.locator("li").filter(has_text=value).nth(0).click()


async def process_multi_city_selectors(locator: Locator, value: str) -> None:
    await locator.scroll_into_view_if_needed()
    await locator.focus()
    await locator.fill(value)
    

async def spawn_multi_city_selectors(page: Page, city_amount: int) -> None:
    await page.locator(ADD_FLIGHT_BUTTON_SELECTOR).first.wait_for(state='visible', timeout=800)
    await page.locator(ADD_FLIGHT_BUTTON_SELECTOR).first.click(click_count=city_amount)
    await page.wait_for_timeout(500)


async def ensure_popover_is_closed(page: Page) -> None:
    try:
        await page.keyboard.press("Escape")
        await page.get_by_role("dialog").first.wait_for(state='hidden', timeout=1000)
    except Exception:
        pass


async def show_adult_per_infants_on_lap_error(page: Page) -> None:
    error_message = await page.locator(
        ADULT_PER_INFANTS_ON_LAP_ERROR_SELECTOR
    ).first.text_content()
    if error_message:
        raise AdultPerInfantsOnLapError(error_message)


async def show_no_flights_found_error(page: Page) -> None:
    # TEMPORAL SOLUTION. TODO: Should not be waiting for 1s for the user to have response
    # TEMPORAL SOLUTION. TODO: Sometimes the search takes too long and when that happens, it does not show the error 
    try:
        error_element = page.locator(NO_FLIGHTS_ERROR_SELECTOR).first
        await error_element.wait_for(state='visible', timeout=10_000)

        error_message = await error_element.text_content()
        if error_message:
            raise NoFlightsFoundError(error_message)
    except NoFlightsFoundError:
        # Re-raise the NoFlightsFoundError to propagate it
        raise
    except Exception:
        # If the error element doesn't exist (timeout), it means flights are present
        pass
