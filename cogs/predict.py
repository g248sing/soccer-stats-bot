# import structlog
# from nextcord.ext import commands

# from utils.objects import Embed, Prediction, Emoji, Leaderboard
# from utils.mongo import MongoDB

# log = structlog.get_logger(__name__)


# class MatchPrediction(commands.Cog, name="Match Prediction"):
#     def __init__(self, bot):
#         self.bot = bot
#         self.pred = None
#         self.db = MongoDB("predictions")
#         self.lb = Leaderboard(self.db)

#     @commands.command(aliases=['vote'])
#     async def predict(self, ctx, score1: int, score2: int):
#         if ctx.invoked_subcommand is None:
#             if self.pred.is_running:
#                 self.pred.add_vote(ctx.author.id, score1, score2)
#                 new_embed = self.pred.get_match_embed()
#                 await self.pred.message.edit(embed=new_embed)
#             else:
#                 await ctx.send("Prediction is closed")

#     @commands.command(aliases=['lb', 'top'])
#     async def leaderboard(self, ctx, page: int = 1):
#         embed = self.lb.get_lb_embed(page - 1)
#         await ctx.send(embed=embed)

#     @commands.group()
#     @commands.has_guild_permissions(administrator=True)
#     async def match(self, ctx):
#         if ctx.invoked_subcommand is None:
#             pass  # Todo: show help

#     @match.command()
#     async def create(self, ctx, team1: str, team2: str):
#         if self.pred:
#             await ctx.send("Another prediction exists! Can't create new.")
#             return
#         self.pred = Prediction(team1, team2)
#         embed = Embed(title=f"{self.pred.match}", description="Status: Running")
#         self.pred.message = await ctx.send(embed=embed)
#         await self.pred.message.add_reaction(Emoji.lock)
#         await self.pred.message.add_reaction(Emoji.unlock)

#     @match.command()
#     async def result(self, ctx, score1: int, score2: int):
#         points = self.pred.get_winners_points(score1, score2)
#         await self.lb.update(points)
#         embed = self.pred.get_winners_embed(points)
#         await ctx.send(embed=embed)
#         self.pred = None

#     @match.command()
#     async def lock(self, ctx):
#         await self.pred.change_status(lock=True)

#     @match.command()
#     async def unlock(self, ctx):
#         await self.pred.change_status(lock=False)

#     @commands.Cog.listener()
#     @commands.has_guild_permissions(administrator=True)
#     async def on_raw_reaction_add(self, payload):
#         guild = await self.bot.fetch_guild(payload.guild_id)
#         member = await guild.fetch_member(payload.user_id)
#         if self.pred is None:
#             return
#         if payload is not None and payload.message_id == self.pred.message.id and member != self.bot.user:
#             if member.guild_permissions.administrator:
#                 if payload.emoji.name == Emoji.lock:
#                     await self.pred.change_status(lock=True)
#                 elif payload.emoji.name == Emoji.unlock:
#                     await self.pred.change_status(lock=False)
#             await self.pred.message.remove_reaction(payload.emoji, member)

#     async def cog_command_error(self, ctx, error):
#         log.error(error)
#         if isinstance(error, commands.CheckFailure):
#             await ctx.reply("Don't try to be a mod dude")
#         elif isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
#             await ctx.reply("What are you retar...? Give a valid argument bruh")


def setup(bot):
    # bot.add_cog(MatchPrediction(bot))
    ...
