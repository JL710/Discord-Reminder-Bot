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
        self.__active: bool = True

        options = [discord.SelectOption(label=f"[{x[0]}] {x[3]}", value=str(x[0])) for x in db.get_categorys(guild_id)]
        super().__init__(options=options)

    async def callback(self, interaction: discord.Interaction):
        if not self.__active:
            await interaction.response.send_message(embed=discord.Embed(title="Already created!", color=self.bot.error_color), ephemeral=True)
            await interaction.response.defer()
            return
        self.__active = False
        db.create_reminder(self.__date.timestamp(), interaction.user.id, int(self.values[0]) , self.__message)
        await interaction.response.send_message(embed=discord.Embed(title="Successfully created!", color=self.bot.success_color), ephemeral=True)



# view stuff for editing a reminder

class EditModal(discord.ui.Modal):
    def __init__(self, id):
        super().__init__(title="Edit")

        self.__id = id

        self.__reminder = db.get_reminder(id)
        self.date = datetime.datetime.fromtimestamp(self.__reminder[2])

        # add items
        self.__inputtext_text = discord.ui.InputText(label="Text", value=self.__reminder[4], max_length=3000, min_length=3)
        self.add_item(self.__inputtext_text)
        self.__inputtext_year = discord.ui.InputText(label="Year", value=self.date.year, min_length=4)
        self.add_item(self.__inputtext_year)
        self.__inputtext_month = discord.ui.InputText(label="Month", value=self.date.month, min_length=1)
        self.add_item(self.__inputtext_month)
        self.__inputtext_day = discord.ui.InputText(label="Day", value=self.date.day, min_length=1)
        self.add_item(self.__inputtext_day)
        self.__inputtext_hour = discord.ui.InputText(label="Hour", value=self.date.hour, min_length=1)
        self.add_item(self.__inputtext_hour)

    async def callback(self, interaction: discord.Interaction):
        try:
            # try to convert a date
            date = datetime.datetime(
                int(self.__inputtext_year.value),
                int(self.__inputtext_month.value),
                int(self.__inputtext_day.value),
                int(self.__inputtext_hour.value)
            )
            date.timestamp()
        except (ValueError, OSError):
            await interaction.response.send_message(embed=discord.Embed(title="Somethings is wrong with the time!", color=0xdd5e53), ephemeral=True)
            return
        # overwride db
        db.update_reminder(self.__id, int(date.timestamp()), self.__inputtext_text.value)
        await interaction.response.send_message(embed=discord.Embed(title="Geändert", color=0x32ad32), ephemeral=True)

