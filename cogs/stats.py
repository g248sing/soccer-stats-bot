import structlog
from typing import List
from itertools import chain
from unicodedata import name

import nextcord
from nextcord import Message, SelectOption, Interaction, SlashOption
from nextcord.ext import commands
from nextcord.ext.commands import Context
from nextcord.ext.commands.bot import Bot
from nextcord.ui import Select


from utils.objects import TESTING_GUILD_IDS
from utils.heavy_task import make_heavy_task

from utils.data import (
    PlayersData, 
    RT2POS, 
    RADAR_TYPES, 
    RT_COLS,
    SHOOTING_COLS,
    PASSING_COLS,
    ADV_PASSING_COLS,
    CREATION_COLS,
    POSESSION_COLS,
    DEFENCE_COLS,
    ADV_DEFENCE_COLS,
    NEGATIVE_COLS
)
from utils.data.plots import radar_plot
from utils.objects import Emoji


def get_radar_plots(interaction: Interaction, player1_info, player2_info, stat_cols):
    """

    """
    buffer = radar_plot(player1_info, player2_info, stat_cols)
    p1_name = player1_info['name']
    p2_name = player2_info['name']
    season = player1_info['season']
    return interaction.send(file=nextcord.File(buffer, filename=f'radar_{p1_name}_{p2_name}_{season}.png'))


class SelectStats(nextcord.ui.View):
    
    MIN_COLS = 1
    MAX_COLS = 15

    SELECT_OPTIONS = {
     'Shooting':  [SelectOption(label=season, value=season) for season in SHOOTING_COLS],
     'Passing':  [SelectOption(label=season, value=season) for season in PASSING_COLS],
     'Advanced Passing':  [SelectOption(label=season, value=season) for season in ADV_PASSING_COLS],
     'Creation':  [SelectOption(label=season, value=season) for season in CREATION_COLS],
     'Posession':  [SelectOption(label=season, value=season) for season in POSESSION_COLS],
     'Defence':  [SelectOption(label=season, value=season) for season in DEFENCE_COLS],
     'Advanced Defence':  [SelectOption(label=season, value=season) for season in ADV_DEFENCE_COLS],
     'Negative': [SelectOption(label=season, value=season) for season in NEGATIVE_COLS]
    }

    def __init__(self, bot: Bot, ctx: Context, display_msg: Message, n: int):
        super().__init__()
        self.bot = bot
        self.ctx = ctx
        self.display_msg = display_msg
        self.n = n
        self.select_labels = list(self.SELECT_OPTIONS.keys())
        self.select_views = {
            k: Select(placeholder=k, min_values=0, max_values=max(len(self.SELECT_OPTIONS[k]), self.MAX_COLS), options=self.SELECT_OPTIONS[k])
            for k in self.select_labels
        }
        self.selected_cnts = {k : 0 for k in self.select_labels}
        self.selected_cols = {k : [] for k in self.select_labels}

        self._index = 0
        self.children.append(self.active_view)

    @property
    def index(self):
        return self._index
    
    @index.setter
    def index(self, val):
        max_val = len(self.select_labels) - 1
        if val > max_val:
            val = max_val
        if val < 0:
            val = 0
        self._index = val

    @property
    def active_view(self):
        return self.select_views[self.select_labels[self.index]]

    # @nextcord.ui.button(label=f'Prev', style=nextcord.ButtonStyle.primary, row = 4)
    # async def prev(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
    #     self.index -= 1
    #     self.children[-1] = self.active_view
    #     await interaction.response.edit_message(content="Select Stats", view=self)
    #     pass
    
    @nextcord.ui.button(label=f'Next', style=nextcord.ButtonStyle.primary, row=4)
    async def next(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self._update()

        self.index += 1
        self.children[-1] = self.active_view
        if self.index == len(self.select_labels) - 1:
            button.disabled = True

        await interaction.response.edit_message(content="**Select Stats**", view=self)
    
    @nextcord.ui.button(label=f'Done', style=nextcord.ButtonStyle.success, row=4)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self._update()
        
        cols = list(chain(*self.selected_cols.values()))
        if len(cols) > self.MAX_COLS:
            cols = cols[:self.MAX_COLS]
            await self.display_msg.edit(content=self.display_string(f"Will keep first {self.MAX_COLS} cols"))
        await self.display_msg.delete()
        self.stop()
        await interaction.response.edit_message(content="Select Season", view=SelectPlayers(self.bot, self.ctx, self.n, cols))

    async def _update(self):
        self.selected_cols[self.select_labels[self.index]] = self.active_view.values
        self.selected_cnts[self.select_labels[self.index]] = len(self.active_view.values)
        await self.display_msg.edit(content=self.display_string())
        

    def display_string(self, extra: str="") -> str:
        return f"**Selected**: {sum(self.selected_cnts.values())} (keep it between {self.MIN_COLS}-{self.MAX_COLS} columns)\n" \
             + (f"*{extra}*" if extra != "" else "")

class SelectPlayers(nextcord.ui.View):

    """
    This view will sequentially show dropboxes to select a player. Finally, the
    appropriate stats will be send back.
    """

    SEASON_OPTIONS = [SelectOption(label=season, value=season) for season in PlayersData.SEASONS]
    logger = structlog.get_logger()

    def __init__(self, bot: Bot, interaction: Interaction, num_player: int, cols: List[str]=None):
        super().__init__()
        self.bot = bot
        self.interaction = interaction
        self.player = 1
        self.num_player = num_player
        self.df = None
        self.player_info = {
            1: {
                'radar_type': None,
                'league': None,
                'team': None,
                'name': None,
                'season': None,
                # a pandas series containing the player data
                'data': None
            },
            2: {
                'radar_type': None,
                'league': None,
                'team': None,
                'name': None,
                'season': None,
                # a pandas Series containing the player data
                'data': None
            }
        }
        self.cols = cols
        self.keys = ('season', 'radar_type', 'league', 'team', 'player')
        self.curr = 0
        self.handlers = (
            self._season_handler, 
            self._rt_handler, 
            self._league_handler,
            self._team_handler, 
            self._player_handler
        )

    async def _season_handler(self, season: str):
        # every player stat will be of the same season
        for pi in range(1, self.num_player + 1):
            self.player_info[self.player]['season'] = season
        return [SelectOption(label=rt, value=rt) for rt in RADAR_TYPES]
        
    async def _rt_handler(self, rt: str):
        posns = RT2POS[rt]
        season = self.player_info[self.player]['season']
        # get the season data if it's the first player
        if self.player == 1:
            if rt != 'Goalkeepers':
                self.df = PlayersData.get_players_data(season)
            else:
                self.df = PlayersData.get_gk_data(season)
        if self.cols is None:
            self.cols = RT_COLS[rt]
        cols = self.cols

        # every player stat will be of the same season
        for pi in range(1, self.num_player + 1):
            self.player_info[pi]['radar_type'] = rt
        if self.player == 1:
            self.df = self.df.query("(Position in @posns) & (Nineties>=5.0)")
            self.df = self.df[['Player', 'Squad', 'Competition', 'Nineties'] + cols]
            # compute percentiles
            self.df = PlayersData.compute_percentiles(self.df, cols)

        leagues = self.df.Competition.unique().tolist()
        league_options = [SelectOption(label=league, value=league) for league in leagues]
        return league_options

    async def _league_handler(self, league: str):
        self.player_info[self.player]['league'] = league
        filtered_data = self.df[self.df['Competition'] == league]
        self.player_info[self.player]['data'] = filtered_data
        teams = filtered_data.Squad.unique().tolist()
        team_options = [SelectOption(value=team, label=team) for team in teams]
        return team_options

    async def _team_handler(self, team: str):
        """
        !! This has high chance of exceeding the 25 limit !!
        """
        self.player_info[self.player]['team'] = team
        pdata = self.player_info[self.player]['data']
        pdata = pdata[pdata['Squad'] == team]
        self.player_info[self.player]['data'] = pdata
        players = pdata.Player.unique().tolist()
        player_options = [SelectOption(
            value=player, label=player) for player in players]
        return player_options

    async def _player_handler(self, player: str):
        self.player_info[self.player]['name'] = player
        pdata = self.player_info[self.player]['data']
        self.player_info[self.player]['data'] = pdata[pdata['Player'] == player]
        return None

    @nextcord.ui.select(placeholder="---", options=SEASON_OPTIONS)
    async def _player_select(self, select: nextcord.ui.Select, interaction: nextcord.Interaction):
        # don't do anything if anyone else try to stick their nose ( unless he's the owner :CHEEKYSMILE: )
        # if interaction.author != interaction.user and not await self.bot.is_owner(interaction.user):
        #     return
        self.interaction = interaction
        try:
            next_options =  await self.handlers[self.curr](select.values[0])
        except Exception as e:
            self.logger.error(f'Error while selecting: {e}')
            self.stop()
            if interaction.message:
                await interaction.message.delete()
            await self.interaction.response.send_message(f"Can't load data :/ Error: {e}")
            return
        if next_options != None:
            select.options = next_options
        select.placeholder = "---"  #! BUG: not resetting to "---" on android app
        self.curr += 1

        # if first response then delete the original reply and send new hidden newreply
        # if self.curr == 1:
        #     await interaction.message.delete()
        #     text = f"Player {self.player}" + f"\nChoose {self.keys[self.curr]}:"
        #     await interaction.response.send_message(content=text, view=self, ephemeral=True)
        # after receiving the last detail for a player
        if self.curr == len(self.keys):
            # if data of more players are needed
            if self.player < self.num_player:
                self.player += 1
                # start from the leagues
                self.curr = 2
                # TODO: should we just store league options statically?
                leagues = self.df.Competition.unique().tolist()
                select.options = [SelectOption(label=league, value=league) for league in leagues]
                text = f"Player {self.player}" + f"\nChoose {self.keys[self.curr]}:"
                await interaction.response.edit_message(content=text, view=self)
            else:
                select.disabled = True
                await interaction.response.edit_message(content='Crunching numbers...', view=None)
                try:
                    foo = make_heavy_task(get_radar_plots, self.interaction)
                    foo(self.player_info[1], self.player_info[2], self.cols)
                except Exception:
                    await interaction.response.send_message(f'Are you trying to kill me here?? Wait for previous tasks bro :/')
        # send selection box for next attributes
        else:
            text = f"Player {self.player}" + f"\nChoose {self.keys[self.curr]}:"
            await interaction.response.edit_message(content=text, view=self)


class Stats(commands.Cog):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

    @nextcord.slash_command(name="stat", guild_ids=TESTING_GUILD_IDS, description="stat")
    async def stat_slash(
        self, 
        interaction: Interaction, 
    ):
        pass

    @stat_slash.subcommand(name="player_radar", description="Player radar plots")
    async def player_radars_slash(
        self, 
        interaction: Interaction, 
        n: int = SlashOption(
            name="type", 
            description='type of radar plot', 
            choices={"solo": 1, "vs": 2},
            required=True
            )
    ):
        await interaction.response.send_message(
                content="Select Season",
                view=SelectPlayers(self.bot, interaction, n),
                ephemeral=True)
    
    @commands.group(brief=f"Get statistics. For detailed help do, .help stat")
    async def stat(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            pass

    @stat.command(brief="[n=1] Player radar plots (n = number of players, default=1)")
    async def radar(self, ctx: Context, n: int=1):
        if n in (1, 2):
            await ctx.reply(
                content="Select Season",
                view=SelectPlayers(self.bot, ctx, n))
        else:
            ...
    
    @stat.command(brief="Game of paitence it is :CHEEKYSMILE:") 
    async def proradar(self, ctx: Context, n: int=1):
        if n in (1, 2):
            disp_msg = await ctx.reply(content="Temp")
            select_view = SelectStats(self.bot, ctx, disp_msg, n)
            await ctx.reply(content="**Select Stats**", view=select_view)

def setup(bot):
    bot.add_cog(Stats(bot))
