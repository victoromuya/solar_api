import json
from functools import lru_cache
from math import ceil
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from django.conf import settings


FALLBACK_PRICE_RANGES_NAIRA = {
    "inverter_per_kva": {"min": 150_000, "max": 250_000},
    "battery_200ah": {"min": 100_000, "max": 150_000},
    "panel_200w": {"min": 85_000, "max": 110_000},
}

FALLBACK_SOURCES = [
    "https://kara.com.ng/solar-panels-price/",
    "https://solarinverterinstallation.com/how-much-does-solar-installation-cost-in-nigeria-a-complete-2025-guide/",
    "https://afrotools.com/blog/solar-panel-costs-nigeria-2026/",
]


def midpoint(price_range):
    return round((price_range["min"] + price_range["max"]) / 2)


def normalize_price_range(value):
    if isinstance(value, dict):
        if "price" in value:
            price = int(value["price"])
            return {"min": price, "max": price}

        if "min" in value and "max" in value:
            return {"min": int(value["min"]), "max": int(value["max"])}

    if isinstance(value, (int, float)):
        price = int(value)
        return {"min": price, "max": price}

    return None


def normalize_public_prices(payload):
    data = payload.get("prices", payload) if isinstance(payload, dict) else {}

    keys = {
        "inverter_per_kva": ["inverter_per_kva", "inverter_1kva", "inverter_kva"],
        "battery_200ah": ["battery_200ah", "battery_12v_200ah"],
        "panel_200w": ["panel_200w", "solar_panel_200w"],
    }

    prices = {}
    for target, aliases in keys.items():
        for alias in aliases:
            normalized = normalize_price_range(data.get(alias))
            if normalized:
                prices[target] = normalized
                break

    if len(prices) != len(keys):
        return None

    return {
        "prices": prices,
        "source": payload.get("source") or getattr(settings, "SOLAR_PRICE_SOURCE_URL", ""),
        "source_type": "public_json",
    }


@lru_cache(maxsize=1)
def get_public_price_data():
    source_url = getattr(settings, "SOLAR_PRICE_SOURCE_URL", "")

    if not source_url:
        return None

    try:
        with urlopen(source_url, timeout=3) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, ValueError, OSError):
        return None

    return normalize_public_prices(payload)


def get_price_data():
    public_data = get_public_price_data()

    if public_data:
        return public_data

    return {
        "prices": FALLBACK_PRICE_RANGES_NAIRA,
        "source": FALLBACK_SOURCES,
        "source_type": "fallback_public_pages",
    }


def estimate_recommendation_costs(recommendation):
    price_data = get_price_data()
    prices = price_data["prices"]

    inverter_units = max(1, ceil(recommendation.inverter_kva))
    battery_units = max(1, ceil(recommendation.battery_capacity_ah / 200))
    panel_units = max(0, recommendation.panel_quantity)

    inverter_cost = inverter_units * midpoint(prices["inverter_per_kva"])
    battery_cost = battery_units * midpoint(prices["battery_200ah"])
    panel_cost = panel_units * midpoint(prices["panel_200w"])
    total_cost = inverter_cost + battery_cost + panel_cost

    if price_data["source_type"] == "public_json":
        cost_note = (
            "Estimated component-only cost in Naira from the configured public "
            "JSON price feed. Installation, wiring, mounting, delivery, brand, "
            "and vendor margin can change the final quote."
        )
    else:
        cost_note = (
            "Estimated component-only cost in Naira using fallback public market "
            "price ranges"
        )

    return {
        "inverter_estimated_cost_naira": inverter_cost,
        "battery_estimated_cost_naira": battery_cost,
        "panel_estimated_cost_naira": panel_cost,
        "total_estimated_cost_naira": total_cost,
        "cost_note": cost_note,
        "cost_source_type": price_data["source_type"],
        "cost_source": price_data["source"],
    }
