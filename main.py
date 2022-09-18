import discord
from pathlib import Path
import logging



class Bot(discord.Bot):
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        
        self.default_color = 0x4286f4
        self.success_color = 0x32ad32
        self.error_color = 0xdd5e53

        intents = discord.Intents.all()
        super().__init__(
            intents=intents,
            owner_id=39844029962754457
        )

        self.load_extension("reminder_cog")

    async def on_ready(self):
        print("Bot is online")

    async def on_interaction(self, interaction: discord.Interaction):
        data_dict = {
            "channel_id": interaction.channel_id,
            "guild_id": interaction.guild_id,
            "user_id": interaction.user.id
        }
        self.logger.debug(data_dict)
        return await super().on_interaction(interaction)

    async def on_application_command(self, context: discord.ApplicationContext) -> None:
        data_dict = {
            "full-command": context.command.full_parent_name,
            "command": context.command.name,
            "quialified-command": context.command.qualified_name,
            "author": context.author.id,
            "channel_id": context.channel_id,
            "guild_id": context.guild_id,
            "selected_options": context.selected_options,
            "unselected_options": context.unselected_options
        }
        self.logger.info(data_dict)


if __name__ == "__main__":
    logger = logging.Logger("bot", level=logging.DEBUG)
    stream_handler = logging.StreamHandler()
    format1 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(format1)
    logger.addHandler(stream_handler)

    bot = Bot(logger)
    bot.run(Path("token.txt").read_text(), reconnect=True)

