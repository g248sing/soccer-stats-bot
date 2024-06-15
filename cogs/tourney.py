import structlog
from nextcord.ext import commands

from utils.objects import Embed

log = structlog.get_logger(__name__)


class Tourney:
    def __init__(self, name):
        self.name = name
        self.players = {}
        self.fixtures = {}

    def add_player(self, player):
        self.players[player.id] = {"name": player.display_name}

    def remove_player(self, player):
        self.players.pop(player.id)

    def swap_player(self, p1, p2):
        pass

    def draw_matchday(self):
        #  Todo: shuffle players
        if len(self.players) % 2:
            self.players[-1] = {"name": "-"}
        first, *rest = self.players.keys()
        n = len(self.players)
        for md in range(n - 1):
            players = [first] + rest[n - md:] + rest[:n - md]
            self.fixtures[md] = [(players[i], players[n - i - 1]) for i in range(n // 2)]


class Tournament(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tourney = None

    @commands.group()
    async def tourney(self, ctx):
        pass

    @tourney.command()
    @commands.check_any(commands.is_owner(), commands.has_guild_permissions(administrator=True))
    async def create(self, name):
        self.tourney = Tourney(name)

    async def add(self, ctx, member: commands.MemberConverter):
        self.tourney.add_player(member)
        await ctx.reply(embed=Embed(description=f"added {member.mention}", author=ctx.author, show_time=True))

    async def remove(self, ctx, member: commands.MemberConverter):
        self.tourney.remove_player(member)
        await ctx.reply(embed=Embed(description=f"removed {member.mention}", author=ctx.author, show_time=True))


def setup(bot):
    bot.add_cog(Tournament(bot))
