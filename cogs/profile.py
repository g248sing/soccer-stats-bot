import nextcord
import structlog
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

from utils.objects import Embed, TESTING_GUILD_IDS

log = structlog.get_logger(__name__)


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name = "pfp", guild_ids=TESTING_GUILD_IDS, description="Shows profile pics")
    async def pfp_slash(self, interaction: Interaction, member: nextcord.Member = SlashOption(name='member', required=True)):
        if not isinstance(member, nextcord.Member):
            member = interaction.user
        embed = Embed(description=f"Profile pic of {member.mention}", author=interaction.user, show_time=True)
        embed.set_image(url=member.display_avatar.url)
        # await ctx.reply(embed=embed)
        await interaction.response.send_message(embed=embed)

    @commands.command(name="pfp")
    async def pfp_cmd(self, ctx, member: commands.MemberConverter = None):
        if not isinstance(member, nextcord.Member):
            member = ctx.author
        embed = Embed(description=f"Profile pic of {member.mention}", author=ctx.author, show_time=True)
        embed.set_image(url=member.display_avatar.url)
        await ctx.reply(embed=embed)

    @commands.command()
    async def profile(self, ctx, member: commands.MemberConverter = None):
        if not isinstance(member, nextcord.Member):
            member = ctx.author
        embed = Embed(title=f"{member.display_name}'s profile", author=ctx.author, show_time=True)
        embed.add_field(name="Joined at", value=member.joined_at)
        embed.add_field(name="Top role", value=member.top_role.name)
        await ctx.reply(embed=embed)

    async def cog_command_error(self, ctx, error):
        log.error(error)
        if isinstance(error, commands.MemberNotFound):
            await ctx.reply("Member not found")


def setup(bot):
    bot.add_cog(Profile(bot))
