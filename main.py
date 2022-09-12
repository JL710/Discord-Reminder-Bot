import discord
from pathlib import Path



class Bot(discord.Bot):
    def __init__(self):
        self.default_color = 0x4286f4
        self.success_color = 0x32ad32
        self.error_color = 0xdd5e53

        intents = discord.Intents.all()
        super().__init__(
            intents=intents,
            owner_id=398440299627544577,
            debug_guilds=[883284695205412874]
        )

        self.load_extension("reminder_cog")

    async def on_ready(self):
        print("Bot is online")

if __name__ == "__main__":
    bot = Bot()
    bot.run(Path("token.txt").read_text(), reconnect=True)

