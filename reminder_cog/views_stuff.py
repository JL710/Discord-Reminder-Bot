import discord
from . import db
import datetime


class SelectCategorySelect(discord.ui.Select):
    def __init__(self, bot, categorys: list, owned_categorys: list):
        self.bot = bot
        options = [discord.SelectOption(label=f"[{x[0]}] {x[3]}", value=str(x[0]), default=x[0] in owned_categorys) for x in categorys]
        super().__init__(options=options, max_values=len(options))

    async def callback(self, interaction: discord.Interaction):
        db.set_user_categorys([int(x) for x in self.values], interaction.user.id)
        await interaction.response.send_message(embed=discord.Embed(title="Successfully changed!", color=self.bot.success_color), ephemeral=True)




# view stuff for create reminder

class SelectCategoryForReminderSelect(discord.ui.Select):
    def __init__(self, bot, guild_id: int, date, message: str):
        self.bot = bot
        self.__date = date
        self.__message = message

        options = [discord.SelectOption(label=f"[{x[0]}] {x[3]}", value=str(x[0])) for x in db.get_categorys(guild_id)]
        super().__init__(options=options)

    async def callback(self, interaction: discord.Interaction):
        db.create_reminder(self.__date.timestamp(), interaction.user.id, int(self.values[0]) , self.__message)
        await interaction.response.send_message(embed=discord.Embed(title="Successfully Created!", color=self.bot.success_color), ephemeral=True)

