import discord
from discord.ext import commands, pages, tasks
from . import db
from . import views_stuff
import datetime, time


class ReminderCog(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Bot = bot

    def cog_unload(self) -> None:
        self.check_and_remind.stop()
        return super().cog_unload()

    @commands.Cog.listener()
    async def on_ready(self):
        self.check_and_remind.start()

    @commands.slash_command(name="create_category", description="create a category")
    @commands.has_permissions(administrator=True)
    async def create_category(self, ctx: discord.ApplicationContext, name: discord.Option(str, max_length=50)):
        if len(db.get_categorys(ctx.guild_id)) >=25:
            await ctx.respond(embed=discord.Embed(title="Maximum amount of Categorys exist!", color=self.bot.error_color), ephemeral=True)
            return
        
        db.create_category(ctx.user.id, ctx.guild_id, name)
        await ctx.respond(embed=discord.Embed(title="Successfully created!", color=self.bot.success_color), ephemeral=True)

    @commands.slash_command(name="categorys", description="shows categorys and lets you choose if you want to get remembered")
    async def select_category(self, ctx: discord.ApplicationContext):
        categorys = db.get_categorys(ctx.guild_id)
        owned_categorys = db.get_owned_category(ctx.user.id)
        if len(categorys) <= 0:
            await ctx.respond(embed=discord.Embed(title="No Category exists!", color=self.bot.error_color), ephemeral=True)
            return

        await ctx.respond(view=discord.ui.View(views_stuff.SelectCategorySelect(self.bot, categorys, owned_categorys)), ephemeral=True)

    @commands.slash_command(name="delete_category", description="deletes a category")
    @commands.has_permissions(administrator=True)
    async def delete_category(self, ctx: discord.ApplicationContext, category_id: int):
        if not db.category_exists(category_id):
            await ctx.respond(embed=discord.Embed(title="Category does not exist!", color=self.bot.error_color), ephemeral=True)
            return
        
        db.delete_category(category_id)
        await ctx.respond(embed=discord.Embed(title="Successfully deleted!", color=self.bot.success_color), ephemeral=True)
    
    @commands.slash_command(name="create", description="creates a reminder")
    async def create(self, ctx: discord.ApplicationContext,
            year: discord.Option(int, min_value=2000), # need to be above x to not crash the timestamp
            month: discord.Option(int, min_value=1, max_value=12),
            day: discord.Option(int, min_value=1, max_value=31),
            hour: discord.Option(int, min_value=0, max_value=24),
            message: discord.Option(str, max_length=3000)
            ):
        # check if any category exist
        if len(db.get_categorys(ctx.guild_id)) <= 0:
            await ctx.respond(embed=discord.Embed(title="Categorys do not exist!", color=self.bot.error_color), ephemeral=True)
            return

        point_in_time = datetime.datetime(year, month, day, hour)
        await ctx.respond("Choose a Category for the Reminder.", view=discord.ui.View(views_stuff.SelectCategoryForReminderSelect(self.bot, ctx.guild_id, point_in_time, message)), ephemeral=True)
    
    @commands.slash_command(name="reminders", description="lists reminders")
    async def reminders(self, ctx: discord.ApplicationContext):
        # get the reminders
        reminders = []
        categorys = db.get_categorys(ctx.guild_id)
        for category in categorys:
            reminders += db.get_reminders(category[0])
        
        # check if there is a reminder
        if len(reminders) <= 0:
            await ctx.respond(embed=discord.Embed(title="No reminder exist!", color=self.bot.error_color), ephemeral=True)
            return

        # create embeds
        categorys = {x[0]: x[1:4] for x in categorys}
        embeds = []
        for reminder in reminders:
            embed = discord.Embed(title="Reminder", description=reminder[3])
            embed.add_field(name="Creator", value=f"<@{reminder[1]}>")
            embed.add_field(name="Zeit", value=f"<t:{reminder[2]}>")
            embed.add_field(name="Category", value=f"[{reminder[4]}] {categorys[reminder[4]][2]}")
            embed.add_field(name="ID", value=f"{reminder[0]}")
            embeds.append(embed)

        # ctx respond
        paginator = pages.Paginator(pages=embeds)
        await paginator.respond(ctx.interaction, ephemeral=True)

    @commands.slash_command(name="delete", description="deletes a reminder")
    async def delete(self, ctx: discord.ApplicationContext, reminder_id: int):
        # check if reminder exists
        if not db.reminder_exist(reminder_id):
            await ctx.respond(embed=discord.Embed(title="No reminder exist!", color=self.bot.error_color), ephemeral=True)
            return

        # check if user is owner of the reminder or has admin perms
        if ctx.user.id != db.get_reminder(reminder_id)[3] and not ctx.user.guild_permissions.administrator:
            await ctx.respond(embed=discord.Embed(title="No Permission!", color=self.bot.error_color), ephemeral=True)
            return

        # delete reminder
        db.delete_reminder(reminder_id)
        await ctx.respond(embed=discord.Embed(title="Successfully deleted!", color=self.bot.success_color), ephemeral=True)


    @tasks.loop(seconds=10)
    async def check_and_remind(self):
        print("\ncheck remind")
        now = time.time()

        # get reminders
        reminders = db.get_reminders_for_reminding(now)

        for reminder in reminders:
            users = db.get_users(reminder[3])
            for user in users:
                user_object = self.bot.get_user(user[1])
                if user_object:
                    channel = await user_object.create_dm()
                    try:
                        await channel.send(embed=discord.Embed(title="Reminder", description=reminder[4]))
                    except discord.Forbidden:
                        print("forbidden") # TODO: delete user from table

            # delete reminder
            db.delete_reminder(reminder[0])




def setup(bot):
    bot.add_cog(ReminderCog(bot))



