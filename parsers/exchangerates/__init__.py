import aiohttp
import config

from .types import ExchangeRates

_request_url = 'http://api.exchangeratesapi.io/v1/latest'
_params = {
    'access_key': config.EXCHANGE_REST_API_KEY,
    'symbols': 'USD,RUB'
}


async def get_exchange_rates() -> ExchangeRates:
    """Returns exchange rates for USD and EUR in RUB."""
    async with aiohttp.ClientSession() as session:
        async with session.get(_request_url, params=_params) as response:
            status = response.status
            if status != 200:
                raise ConnectionError(f'Response status is not ok. Response status: {status}')

            data = await response.json()
            rates = data['rates']

            eur = rates['RUB']
            usd = eur / rates['USD']

            return ExchangeRates(
                EUR=round(eur, 2),
                USD=round(usd, 2)
            )
