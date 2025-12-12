from .models import SearchParams, Flight
from .types import TicketType
from .constants.selectors import (
    FLIGHT_TYPE_SELECTOR,
    TICKET_TYPE_SELECTOR,
    SEARCH_BUTTON_SELECTOR,
    PASSENGER_BUTTON_SELECTOR,
    FLIGHTS_SELECTOR
)
from .constants.settings import STOP_AFTER_ATTEMPTS
import asyncio
from playwright.async_api import Page, async_playwright
from .errors import AdultPerInfantsOnLapError, NoFlightsFoundError

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_not_exception_type
)

from .utils import process_flight, show_no_flights_found_error
from .forms import (
    fill_multi_city_form,
    fill_one_way_and_round_trip_form,
    fill_passenger_form
)
from .browser import (
    create_browser_instance,
    create_page_instance
)
from .logging import logger


async def fill_search_form(page: Page, params: SearchParams) -> None:
    ticket_type_div = page.locator(TICKET_TYPE_SELECTOR).first
    flight_type_div = page.locator(FLIGHT_TYPE_SELECTOR).first
    passengers_button_div = page.locator(PASSENGER_BUTTON_SELECTOR).first
    
    await ticket_type_div.click()
    await page.locator("li").filter(has_text=params.ticket_type.value).nth(0).click()

    logger.info("Ticket type selected: %s", params.ticket_type.value)

    await passengers_button_div.scroll_into_view_if_needed()
    await passengers_button_div.wait_for(state='visible')
    await passengers_button_div.click()

    logger.info("Passengers button clicked")

    await fill_passenger_form(page, params)

    logger.info("Passengers form filled")

    await flight_type_div.click()
    await page.locator("li").filter(has_text=params.flight_type.value).nth(0).click()

    logger.info("Flight type selected: %s", params.flight_type.value)

    if params.ticket_type == TicketType.multi_city:
        await fill_multi_city_form(page, params)
    else:
        await fill_one_way_and_round_trip_form(page, params)

    logger.info("Flight form filled")

    await page.locator(SEARCH_BUTTON_SELECTOR).first.click()


async def extract_flights(page: Page) -> list[dict]:
    await show_no_flights_found_error(page)
    await page.locator(FLIGHTS_SELECTOR).first.wait_for(state='visible', timeout=30000)
    flights = await page.query_selector_all(FLIGHTS_SELECTOR)

    flight_tasks = [
        process_flight(flight) for flight in flights
    ]

    logger.info(f"Extracted {len(flights)} flights")

    return await asyncio.gather(*flight_tasks)


@retry(
    stop=stop_after_attempt(STOP_AFTER_ATTEMPTS), 
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_not_exception_type((AdultPerInfantsOnLapError, NoFlightsFoundError))
)
async def search_flights(params: SearchParams) -> list[Flight]:
    async with async_playwright() as playwright:
        browser = await create_browser_instance(playwright)
        page = await create_page_instance(browser)

        logger.info("Filling search form")
        
        await fill_search_form(page, params)

        logger.info("Filled search form")


        logger.info("Extracting flights")
        
        flights = await extract_flights(page)

        await browser.close()
        
        return flights
