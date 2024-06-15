from datetime import timedelta

import structlog
from nextcord.ext.commands import Context
from nextcord.ext import commands, tasks
from nextcord.ext.commands.bot import Bot

from utils.heavy_task import make_heavy_task
from utils.data import PlayersData

log = structlog.get_logger(__name__)

class Sync(commands.Cog):

    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.group()
    @commands.check_any(commands.is_owner(), commands.has_guild_permissions(administrator=True))
    async def sync(self, ctx: Context):
        ...
    

    @sync.group()
    async def player(self, ctx: Context):
        ...

    @player.command()
    async def start(self, ctx: Context):
        if self._players_stat_update_task.is_running():
            await ctx.reply("It's already running")
        else:
            self._players_stat_update_task.start(ctx)
            await ctx.reply("Player data syncing started")

    @player.command()
    async def stop(self, ctx):
        if self._players_stat_update_task.is_running():
            self._players_stat_update_task.cancel()
            await ctx.reply("Player data syncing stopped!")
        else:
            await ctx.reply("Not running!")
        
    
    @player.command()
    @commands.check(commands.is_owner())
    async def reload(self, ctx: Context):
        msg = await ctx.send("Hard reloading players data for all seasons!")
        update_msg = None
        for season in PlayersData.SEASONS:
            if update_msg is None:
                update_msg = await ctx.send(f"Updating data for {season} season...")
            else:
                await update_msg.edit(f"Updating data for {season} season...")
            PlayersData.scrape_data(season)
        await update_msg.edit("Done!")

    @tasks.loop(seconds=timedelta(weeks=1).total_seconds())
    async def _players_stat_update_task(self, ctx: Context):
        ...
        await ctx.send('Updating Players data for the current season...')
        try:
            make_heavy_task(self._players_stat_update, ctx)()
        except Exception:
            await ctx.send(f'Are you trying to kill me here?? Wait for previous tasks bro :/')


    def _players_stat_update(self, ctx: Context):
        ...
        PlayersData.scrape_data(PlayersData.CURR_SEASON)
        return ctx.send('Updated Players data!')
    
    def cog_unload(self) -> None:
        self._players_stat_update_task.cancel()
        super().cog_unload()
    
    async def cog_command_error(self, ctx, error):
        log.error("Error syncing data", exc_info=error)
        if isinstance(error, commands.CheckFailure):
            await ctx.reply("You don't have the authority to do this operation")
        elif isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            await ctx.reply("What are you retarded? Give a valid argument bruh")



def setup(bot):
    bot.add_cog(Sync(bot))
