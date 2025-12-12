from .models import SearchParams
from .types import TicketType, PassengerType
from playwright.async_api import Page, expect
from .utils import (
    spawn_multi_city_selectors,
    ensure_popover_is_closed,
    process_multi_city_selectors,
    process_date_selectors,
    process_flight_selectors,
    show_adult_per_infants_on_lap_error,
)
from .constants.selectors import (
    FROM_SELECTOR,
    TO_SELECTOR,
    DEPARTURE_DATE_SELECTOR,
    RETURN_DATE_SELECTOR,
    ADULT_PASSENGERS_SELECTOR,
    CHILDREN_PASSENGERS_SELECTOR,
    INFANTS_SEAT_PASSENGERS_SELECTOR,
    INFANTS_LAP_PASSENGERS_SELECTOR,
    PASSENGER_INCREMENT_BUTTON,
    PASSENGER_DECREMENT_BUTTON,
    PASSENGER_DONE_BUTTON,
)
from .constants.settings import FLIGHTS_AUTOMATIC_MULTI_CITY_SPAWN
from .logging import logger


async def fill_multi_city_form(page: Page, params: SearchParams) -> None:
    await spawn_multi_city_selectors(page, params.city_amount)

    logger.info(f"Spawned {params.city_amount} multi city selectors")
        
    total_legs = params.city_amount + FLIGHTS_AUTOMATIC_MULTI_CITY_SPAWN

    from_inputs = page.locator(f"{FROM_SELECTOR}:visible")
    to_inputs = page.locator(f"{TO_SELECTOR}:visible")
    departure_date_inputs = page.locator(f"{DEPARTURE_DATE_SELECTOR}:visible")

    await expect(from_inputs).to_have_count(total_legs)
    await expect(to_inputs).to_have_count(total_legs)
    await expect(departure_date_inputs).to_have_count(total_legs)

    # Ensures index safe lookup on departure, destination and departure_date params 
    legs = min(total_legs, len(params.departure), len(params.destination))
    date_legs = min(total_legs, len(params.departure_date))

    for i in range(legs):
        from_input = from_inputs.nth(i)
        to_input = to_inputs.nth(i)

        departure_selectors = params.departure[i]
        destination_selectors = params.destination[i]

        logger.info(f"Setting multi-city departure cities: {departure_selectors}")
        await ensure_popover_is_closed(page)
        await process_multi_city_selectors(from_input, departure_selectors)
        await page.locator("li").filter(has_text=departure_selectors).first.click()

        logger.info(f"Setting multi-city destination cities: {destination_selectors}")
        await ensure_popover_is_closed(page)
        await process_multi_city_selectors(to_input, destination_selectors)
        await page.locator("li").filter(has_text=destination_selectors).first.click()

    for i in range(date_legs):
        await ensure_popover_is_closed(page)

        dep_input = departure_date_inputs.nth(i)
        
        logger.info(f"Setting multi-city departure dates: {params.departure_date[i]}")
        await process_multi_city_selectors(dep_input, params.departure_date[i])
        await dep_input.press("Enter")


async def fill_one_way_and_round_trip_form(page: Page, params: SearchParams) -> None:
    await process_flight_selectors(page, FROM_SELECTOR, params.departure)
    await process_flight_selectors(page, TO_SELECTOR, params.destination)

    match params.ticket_type:
        case TicketType.round_trip:
            logger.info("Setting round trip dates")
            await process_date_selectors(page, DEPARTURE_DATE_SELECTOR, params.departure_date)
            await process_date_selectors(page, RETURN_DATE_SELECTOR, params.return_date)
        case TicketType.one_way:
            logger.info("Setting one way dates")
            await process_date_selectors(page, DEPARTURE_DATE_SELECTOR, params.departure_date)

    # If the date dialog popped open
    # Close it by clicking its own 'Done' button (scoped to the dialog)
    try:
        date_dialog = page.get_by_role("dialog").first
        await date_dialog.wait_for(state='visible', timeout=800)
        await date_dialog.get_by_role("button", name="Done").click()
    except:
        # Dialog not present or not visible; proceed without clicking Done
        pass


async def fill_passenger_form(page: Page, params: SearchParams) -> None:
    dialog = page.get_by_role("dialog").first
    await dialog.wait_for(state="visible")

    targets = {
        PassengerType.adult: params.passengers.get(PassengerType.adult, 1),
        PassengerType.children: params.passengers.get(PassengerType.children, 0),
        PassengerType.infant_seat: params.passengers.get(PassengerType.infant_seat, 0),
        PassengerType.infant_lap: params.passengers.get(PassengerType.infant_lap, 0),
    }

    selectors = {
        PassengerType.adult: ADULT_PASSENGERS_SELECTOR,
        PassengerType.children: CHILDREN_PASSENGERS_SELECTOR,
        PassengerType.infant_seat: INFANTS_SEAT_PASSENGERS_SELECTOR,
        PassengerType.infant_lap: INFANTS_LAP_PASSENGERS_SELECTOR,
    }

    for passenger_type, selector in selectors.items():
        container = dialog.locator(selector)
        current_amount = int(await container.get_attribute("aria-valuenow")) or 0
        target = targets[passenger_type]

        logger.info(f"Selecting {target} for {passenger_type}")

        click_amount = target - current_amount

        if click_amount > 0:
            await container.locator(PASSENGER_INCREMENT_BUTTON).click(click_count=click_amount)
        elif click_amount < 0:
            await container.locator(PASSENGER_DECREMENT_BUTTON).click(click_count=abs(click_amount))

    await show_adult_per_infants_on_lap_error(page)

    await dialog.locator(PASSENGER_DONE_BUTTON).click()
        