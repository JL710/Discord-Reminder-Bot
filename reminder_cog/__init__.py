import discord
from discord.ext import commands
from . import db
from . import views_stuff
import datetime


class ReminderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self) -> None:
        self.bot.loaded_extensions.remove("ReminderCog")
        return super().cog_unload()

    @commands.slash_command(name="create_category")
    @commands.has_permissions(administrator=True)
    async def create_category(self, ctx: discord.ApplicationContext, name: discord.Option(str, max_length=50)):
        if len(db.get_categorys(ctx.guild_id)) >=25:
            await ctx.respond(embed=discord.Embed(title="Maximum amount of Categorys exist!", color=self.bot.error_color), ephemeral=True)
            return
        
        db.create_category(ctx.user.id, ctx.guild_id, name)
        await ctx.respond(embed=discord.Embed(title="Successfully created!", color=self.bot.success_color), ephemeral=True)

    @commands.slash_command(name="categorys")
    async def select_category(self, ctx: discord.ApplicationContext):
        categorys = db.get_categorys(ctx.guild_id)
        owned_categorys = db.get_owned_category(ctx.user.id)
        if len(categorys) <= 0:
            await ctx.respond(embed=discord.Embed(title="No Category exists!", color=self.bot.error_color), ephemeral=True)
            return

        await ctx.respond(view=discord.ui.View(views_stuff.SelectCategorySelect(self.bot, categorys, owned_categorys)), ephemeral=True)

    @commands.slash_command(name="delete_category")
    @commands.has_permissions(administrator=True)
    async def delete_category(self, ctx: discord.ApplicationContext, category_id: int):
        if not db.category_exists(category_id):
            await ctx.respond(embed=discord.Embed(title="Category does not exist!", color=self.bot.error_color), ephemeral=True)
            return
        
        db.delete_category(category_id)
        await ctx.respond(embed=discord.Embed(title="Successfully deleted!", color=self.bot.success_color), ephemeral=True)
    
    @commands.slash_command(name="create")
    async def create(self, ctx: discord.ApplicationContext,
            year: discord.Option(int, min_value=0),
            month: discord.Option(int, min_value=1, max_value=12),
            day: discord.Option(int, min_value=1, max_value=31),
            hour: discord.Option(int, min_value=0, max_value=24),
            message: discord.Option(str, max_length=3000)
            ):
        pass
        point_in_time = datetime.datetime(year, month, day, hour)
    
    @commands.slash_command(name="delete", description="")
    async def delete(self, ctx: discord.ApplicationContext, reminder_id: int):
        pass

def setup(bot):
    bot.add_cog(ReminderCog(bot))



