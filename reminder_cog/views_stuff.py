import discord
from . import db



class SelectCategorySelect(discord.ui.Select):
    def __init__(self, bot, categorys: list, owned_categorys: list):
        self.bot = bot
        options = [discord.SelectOption(label=f"[{x[0]}] {x[3]}", value=str(x[0]), default=x[0] in owned_categorys) for x in categorys]
        super().__init__(options=options, max_values=len(options))

    async def callback(self, interaction: discord.Interaction):
        db.set_user_categorys([int(x) for x in self.values], interaction.user.id)
        await interaction.response.send_message(embed=discord.Embed(title="Successfully changed!", color=self.bot.success_color), ephemeral=True)


