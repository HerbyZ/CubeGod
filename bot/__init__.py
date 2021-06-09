from discord.ext import commands


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def launch(self, token):
        self.run(token)

    async def on_ready(self):
        print('Bot is ready')

    async def on_message(self, message):
        if not message.author.bot:
            await message.channel.send(message.content)
