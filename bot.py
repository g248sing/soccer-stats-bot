import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Gurveer Singh/Desktop/fcd-bot-prod/named-sequencer-426022-f3-20bc589561ca.json"
import structlog
from dotenv import load_dotenv
from nextcord.ext import commands

from utils.objects import TESTING_GUILD_IDS
from utils.logging import setup

load_dotenv()

setup("bot-code")
log = structlog.get_logger(__name__)

bot = commands.Bot(os.getenv('BOT_PREFIX', '$'), case_insensitive=True)
bot.owner_ids = [1245827533270814821]

def load_cogs():
    for cog in os.listdir('./cogs'):
        if cog.endswith('.py'):
            try:
                bot.load_extension(f'cogs.{cog[:-3]}')
            except commands.ExtensionAlreadyLoaded:
                bot.reload_extension(f'cogs.{cog[:-3]}')
    # for module in ['commands.general', 'commands.music', 'plugins.button']:
    #     try:
    #         bot.load_extension(f'music.{module}')
    #     except commands.ExtensionAlreadyLoaded:
    #         bot.reload_extension(f'music.{module}')
    log.info("All cogs (re)loaded")


@bot.command()
async def load(ctx):
    load_cogs()
    

@bot.slash_command(guild_ids=TESTING_GUILD_IDS)
async def ping(interaction):
    await interaction.response.send_message("Pong!")

@bot.event
async def on_ready():
    load_cogs()
    for guild in bot.guilds:
        try:
            log.info(f"Rolling out commands for: {guild.name}")
            await guild.rollout_application_commands()
        except Exception as e:
            log.warn(f"Can't rollout commands for {guild.name}({guild.id}): {e}", exc_info=e, server=guild_id)
    log.info(f'Bot ready', name=bot.user.name, id=bot.user.id)


@bot.command()
async def servers(ctx):
    guilds = list(bot.guilds)
    await ctx.send(f"Connected on {str(len(guilds))} servers:")
    await ctx.send('\n'.join(guild.name + " " + str(guild.id) for guild in guilds))


bot.run(os.getenv('DISCORD_TOKEN'))
