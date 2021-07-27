from parsers.exchangerates import get_exchange_rates

import pytest


# Don't know how to test it normally
@pytest.mark.asyncio
async def test_get_exchange_rates():
    await get_exchange_rates()
