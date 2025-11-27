from .models import SearchParams, Flight
from .types import TicketType
from .constants import (
    FLIGHT_TYPE_SELECTOR,
    STOP_AFTER_ATTEMPTS,
    TICKET_TYPE_SELECTOR,
    SEARCH_BUTTON_SELECTOR,
    PASSENGER_BUTTON_SELECTOR,
)
import asyncio
from playwright.async_api import Page, async_playwright

from tenacity import retry, stop_after_attempt, wait_exponential

from .utils import process_flight
from .forms import (
    fill_multi_city_form,
    fill_one_way_and_round_trip_form,
    fill_passenger_form
)
from .browser import (
    create_browser_instance,
    create_page_instance
)


async def fill_search_form(page: Page, params: SearchParams) -> None:
    ticket_type_div = page.locator(TICKET_TYPE_SELECTOR).first
    flight_type_div = page.locator(FLIGHT_TYPE_SELECTOR).first
    passengers_button_div = page.locator(PASSENGER_BUTTON_SELECTOR).first
    
    await ticket_type_div.click()
    await page.locator("li").filter(has_text=params.ticket_type.value).nth(0).click()

    await passengers_button_div.scroll_into_view_if_needed()
    await passengers_button_div.wait_for(state='visible')
    await passengers_button_div.click()

    await fill_passenger_form(page, params)

    await flight_type_div.click()
    await page.locator("li").filter(has_text=params.flight_type.value).nth(0).click()

    if params.ticket_type == TicketType.multi_city:
        await fill_multi_city_form(page, params)
    else:
        await fill_one_way_and_round_trip_form(page, params)

    await page.locator(SEARCH_BUTTON_SELECTOR).first.click()


async def extract_flights(page: Page) -> list[dict]:
    await page.locator("li.pIav2d").first.wait_for(state='visible', timeout=30000)
    flights = await page.query_selector_all("li.pIav2d")

    if not flights:
        return []

    flight_tasks = [
        process_flight(flight) for flight in flights
    ]

    return await asyncio.gather(*flight_tasks)


@retry(
    stop=stop_after_attempt(STOP_AFTER_ATTEMPTS), 
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def search_flights(params: SearchParams) -> list[Flight]:
    async with async_playwright() as playwright:
        browser = await create_browser_instance(playwright)
        page = await create_page_instance(browser)

        await fill_search_form(page, params)
        flights = await extract_flights(page)

        await browser.close()
        
        return flights
