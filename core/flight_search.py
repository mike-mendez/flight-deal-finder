from core.config import settings
from datetime import datetime
from dateutil.relativedelta import relativedelta
from requests import get
from typing import Any

ENDPOINT = "https://api.tequila.kiwi.com"
LOCATIONS_ENDPOINT = f"{ENDPOINT}/locations/query"
SEARCH_ENDPOINT = f"{ENDPOINT}/v2/search"
HEADERS = dict(accept="application/json", apikey=settings.TEQUILA_API_KEY)

MIN_NIGHTS = 7
MAX_NIGHTS = 28
tomorrow = datetime.now() + relativedelta(days=+1)
six_months = tomorrow + relativedelta(months=+6)


class FlightSearch:
    def __init__(self, data):
        self.data = data

    def find_iata_code(self):
        location_params = {
            "term": f"{self.data.city}",
            "location_type": "city",
            "limit": 1,
        }
        response = get(url=LOCATIONS_ENDPOINT, params=location_params, headers=HEADERS)
        results = response.json()
        iata_code: Any | None = results["locations"][0]["code"] if results["locations"] else None
        return iata_code

    def search_flights(self):
        search_params = {
            "fly_from": "SEL",  # departing_iata
            "fly_to": self.data.iata_code,
            "date_from": tomorrow.strftime("%d/%m/%Y"),  # date_from
            "date_to": six_months.strftime("%d/%m/%Y"),  # date_to
            "nights_in_dst_from": MIN_NIGHTS,  # min_nights
            "nights_in_dst_to": MAX_NIGHTS,  # max_nights
            "flight_type": "round",
            "curr": "USD",
            "locale": "en",
            "price_to": self.data.lowest_price,
            "limit": 1,
        }
        response = get(url=SEARCH_ENDPOINT, params=search_params, headers=HEADERS)
        results = response.json()
        flight_deal: Any | None = results if results["data"] else None
        return flight_deal
