import os

import httpx

from app.services.cache import get_cache, set_cache

async def fetch_currency_rates(base_currency: str) -> dict[str, float]:
    """Fetch currency exchange rates from an external API."""
    api_key = os.getenv("EXCHANGERATE_API_KEY")
    if not api_key:
        raise RuntimeError("EXCHANGERATE_API_KEY is not set")

    cache_key = f"currency_{base_currency}"
    cached_data = get_cache(cache_key)

    if cached_data:
        return cached_data

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
        )
        response.raise_for_status()
        data = response.json()
        
        rates = data.get("conversion_rates", {})
        set_cache(cache_key, rates, ttl=3600)  # Cache for 1 hour
        return rates