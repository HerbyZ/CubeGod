from discord.ext import commands, tasks
from dhooks import Webhook, Embed
from parsers.exchangerates import get_exchange_rates

import config
import datetime


class ExchangeRatesModule(commands.Cog):
    def __init__(self, bot):
        self._bot = bot
        self._webhook = Webhook.Async(config.EXCHANGE_RATES_WEBHOOK_URL)

        self._check_time_loop.start()

    @tasks.loop(minutes=10)
    async def _check_time_loop(self):
        now = datetime.datetime.now().time()
        time_from = datetime.time(hour=10)
        time_to = datetime.time(hour=10, minute=10)

        if time_from <= now <= time_to:
            await self._send_exchange_rates()

    async def _send_exchange_rates(self):
        date = datetime.date.today().strftime('%d.%m.%y')
        rates = await get_exchange_rates()

        embed = Embed(title=f'Курсы валют на {date}')
        embed.add_field(name="USD", value=str(rates.USD))
        embed.add_field(name="EUR", value=str(rates.EUR))
        embed.set_footer('Daily exchange rates. Have a good day!')

        await self._webhook.send(embed=embed)


def setup(bot):
    bot.add_cog(ExchangeRatesModule(bot))
