from nextcord.ext import commands

from music import config
from music import utils
from music.audiocontroller import AudioController
from music.settings import Settings
from music.utils import guild_to_audiocontroller, guild_to_settings


class General(commands.Cog):
    """ A collection of the commands for moving the bot around in you server.

            Attributes:
                bot: The instance of the bot that is executing the commands.
    """

    def __init__(self, bot):
        self.bot = bot

    # logic is split to uconnect() for wide usage
    @commands.command(name='connect', description=config.HELP_CONNECT_LONG, help=config.HELP_CONNECT_SHORT,
                      aliases=['c'])
    async def _connect(self, ctx):  # dest_channel_name: str
        current_guild = utils.get_guild(self.bot, ctx.message)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        await audiocontroller.uconnect(ctx)

    @commands.command(name='disconnect', description=config.HELP_DISCONNECT_LONG, help=config.HELP_DISCONNECT_SHORT,
                      aliases=['dc'])
    async def _disconnect(self, ctx, guild=False):
        current_guild = utils.get_guild(self.bot, ctx.message)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        await audiocontroller.udisconnect()

    @commands.command(name='reset', description=config.HELP_DISCONNECT_LONG, help=config.HELP_DISCONNECT_SHORT,
                      aliases=['rs', 'restart'])
    async def _reset(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        await utils.guild_to_audiocontroller[current_guild].stop_player()
        await current_guild.voice_client.disconnect(force=True)

        guild_to_audiocontroller[current_guild] = AudioController(
            self.bot, current_guild)
        await guild_to_audiocontroller[current_guild].register_voice_channel(ctx.author.voice.channel)

        await ctx.send("{} Connected to {}".format(":white_check_mark:", ctx.author.voice.channel.name))

    @commands.command(name='changechannel', description=config.HELP_CHANGECHANNEL_LONG,
                      help=config.HELP_CHANGECHANNEL_SHORT, aliases=['cc'])
    async def _change_channel(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        vchannel = await utils.is_connected(ctx)
        if vchannel == ctx.author.voice.channel:
            await ctx.send("{} Already connected to {}".format(":white_check_mark:", vchannel.name))
            return

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        await utils.guild_to_audiocontroller[current_guild].stop_player()
        await current_guild.voice_client.disconnect(force=True)

        guild_to_audiocontroller[current_guild] = AudioController(
            self.bot, current_guild)
        await guild_to_audiocontroller[current_guild].register_voice_channel(ctx.author.voice.channel)

        await ctx.send("{} Switched to {}".format(":white_check_mark:", ctx.author.voice.channel.name))

    @commands.command(name='ping', description=config.HELP_PING_LONG, help=config.HELP_PING_SHORT)
    async def _ping(self, ctx):
        await ctx.send("Pong")

    @commands.command(name='setting', description=config.HELP_SHUFFLE_LONG, help=config.HELP_SETTINGS_SHORT,
                      aliases=['settings', 'set'])
    @commands.check_any(commands.is_owner(), commands.has_guild_permissions(administrator=True))
    async def _settings(self, ctx, *args):

        sett = guild_to_settings[ctx.guild]

        if len(args) == 0:
            await ctx.send(embed=await sett.format())
            return

        args_list = list(args)
        args_list.remove(args[0])

        response = await sett.write(args[0], " ".join(args_list), ctx)

        if response is None:
            await ctx.send("`Error: Setting not found`")
        elif response is True:
            await ctx.send("Setting updated!")

    @commands.command(name='register', aliases=['reg', 'setup'])
    @commands.is_owner()
    async def register(self, ctx):
        guild = utils.get_guild(self.bot, ctx.message)
        guild_to_settings[guild] = Settings(guild)
        guild_to_audiocontroller[guild] = AudioController(self.bot, guild)

        sett = guild_to_settings[guild]

        try:
            await guild.me.edit(nick=sett.get('default_nickname'))
        except:
            pass

        if config.GLOBAL_DISABLE_AUTOJOIN_VC == True:
            return

        vc_channels = guild.voice_channels

        if sett.get('vc_timeout') == False:
            if sett.get('start_voice_channel') == None:
                try:
                    await guild_to_audiocontroller[guild].register_voice_channel(guild.voice_channels[0])
                except Exception as e:
                    print(e)

            else:
                for vc in vc_channels:
                    if vc.id == sett.get('start_voice_channel'):
                        try:
                            await guild_to_audiocontroller[guild].register_voice_channel(
                                vc_channels[vc_channels.index(vc)])
                        except Exception as e:
                            print(e)
        await ctx.reply('One time setup done.')


def setup(bot):
    bot.add_cog(General(bot))
