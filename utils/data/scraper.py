TEXT_COLS_MAP = {
    'Player': 'Player',
    'Nation': 'Nation',
    'Pos': 'Position',
    'Squad': 'Squad',
    'Comp': 'Competition',
    'Age': 'Age',
    'Born': 'Born',
    'Playing Time_MP': 'Matches Played',
    'Playing Time_Starts': 'Matches Started',
    'Playing Time_Min': 'Minuted Played',
    # 'Playing Time_90s': 'Nineties',
    '90s': 'Nineties',
}

STAT_COLS_MAP = {
    # Goals and shots
    'Standard_Gls' : ('Goals', 1), # need to make per 90
    'Standard_Sh': ('Shots', 1), # need to make per 90
    'Standard_SoT': ('Shots_on_Target', 1), # need to make per 90
    'Standard_SoT%': ('Shots_on_Target%', 0),
    'Standard_G/Sh': ('Goals/Shot', 0),
    'Standard_G/SoT': ('Goals/Shots_on_Target', 0),
    # avg. dist
    'Standard_Dist': ('Shot_Distance', 0),
    # FK and PK
    'Standard_FK' : ('Freekicks', 1), # need to make per 90
    'Standard_PK' : ('Penalties_scored', 1), # need to make per 90
    'Standard_PKatt' : ('Penalties_attempted', 1), # need to make per 90
    # Expected values
    'Expected_xG': ('xG', 1), # need to make per 90
    'Expected_npxG': ('Non-penalty xG', 1), # need to make per 90
    'Expected_npxG/Sh': ('NpxG/Shot', 0),
    'Expected_G-xG': ('Goals-xG', 1), # need to make per 90
    'Expected_np:G-xG': ('NpGoals-xG', 1), # need to make per 90
    'Performance_G-PK': ('Non-penalty goals', 1), # need to make per 90
    
    'Total_Cmp': ('Passes_Completed', 1), # need to make per 90
    'Total_Att': ('Passes_Attempted', 1), # need to make per 90
    'Total_Cmp%': ('Pass_Completion%', 0),
    'Total_TotDist': ('Passes_TotalDistance', 1), # need to make per 90
    'Total_PrgDist': ('Passes_ProgressiveDistance', 1), # need to make per 90
    'Short_Cmp': ('Shortpasses_Completed', 1), # need to make per 90
    'Short_Att': ('Shortpasses_Attempted', 1), # need to make per 90
    'Short_Cmp%': ('Shortpass_Completion%', 0),
    'Medium_Cmp': ('Mediumpasses_Completed', 1),	# need to make per 90
    'Medium_Att': ('Mediumpasses_Attempted', 1), # need to make per 90
    'Medium_Cmp%': ('Mediumpass_Completion%', 0),
    'Long_Cmp': ('Longpasses_Completed', 1),	# need to make per 90
    'Long_Att': ('Longpasses_Attempted', 1), # need to make per 90
    'Long_Cmp%': ('Longpass_Completion%', 0),
    'Ast': ('Assists', 1), # need to make per 90
    'xA': ('xA', 1), # need to make per 90
    'xAG': ('xAG', 1), # need to make per 90
    'A-xAG': ('Assists-xAG', 1), # need to make per 90
    'KP': ('KeyPasses', 1), # need to make per 90
    '1/3': ('Passes into final third', 1), # need to make per 90
    'PPA': ('Passes into box', 1), # need to make per 90
    'CrsPA': ('Crosses_into_box', 1), # need to make per 90
    'Progression_PrgP': ('Progressive passes', 1), # need to make per 90
    'Pass Types_Live': ('Live_Passes', 1), # need to make per 90
    'Pass Types_Dead': ('Dead_ball_passes', 1), # need to make per 90
    'Pass Types_FK': ('FreeKick_passes', 1), # need to make per 90
    'Pass Types_TB': ('ThroughBalls', 1), # need to make per 90
    # 'Pass Types_Press': ('Under_Pressure_passes', 1), # need to make per 90
    'Pass Types_Sw': ('Switches', 1), # need to make per 90
    'Pass Types_Crs': ('Crosses', 1), # need to make per 90
    'Pass Types_CK': ('CornerKick_passes', 1), # need to make per 90
    'Corner Kicks_In': ('CornerKicks_Inswinging', 1), # need to make per 90
    'Corner Kicks_Out': ('CornerKicks_Outswinging', 1), # need to make per 90
    'Corner Kicks_Str': ('CornerKicks_Straight', 1), # need to make per 90
    # 'Height_Ground': ('Ground_passes', 1), # need to make per 90
    # 'Height_Low': ('Low_passes', 1), # need to make per 90
    # 'Height_High': ('High_passes', 1), # need to make per 90
    # 'Body Parts_Left': ('Passes_Leftfoot', 1), # need to make per 90
    # 'Body Parts_Right': ('Passes_Rightfoot', 1), # need to make per 90
    # 'Body Parts_Head': ('Head_passes', 1), # need to make per 90
    'Pass Types_TI': ('ThrowIns', 1), # need to make per 90
    # 'Body Parts_Other': ('Passes_other_body_parts', 1), # need to make per 90
    'Outcomes_Off': ('Offside_passes', 1), # need to make per 90
    # 'Outcomes_Out': ('Passes_Out_of_bounds', 1), # need to make per 90
    # 'Outcomes_Int': ('Passes_Intercepted', 1), # need to make per 90
    'Outcomes_Blocks': ('Passes_Blocked', 1), # need to make per 90
    'SCA_SCA': ('Shot-creating actions', 1), # need to make per 90
    'SCA Types_PassLive': ('SCA_PassLive', 1), # need to make per 90
    'SCA Types_PassDead': ('SCA_PassDead', 1), # need to make per 90
    'SCA Types_TO': ('SCA_Dribbles', 1), # need to make per 90
    'SCA Types_Sh': ('SCA_Shots', 1), # need to make per 90
    'SCA Types_Fld': ('SCA_Fouls_drawn', 1), # need to make per 90
    'SCA Types_Def': ('SCA_Defensive_actions', 1), # need to make per 90
    'GCA_GCA': ('GCA', 1), # need to make per 90
    'GCA Types_PassLive': ('GCA_PassLive', 1), # need to make per 90
    'GCA Types_PassDead': ('GCA_PassDead', 1), # need to make per 90
    'GCA Types_TO': ('GCA_Dribbles', 1), # need to make per 90
    'GCA Types_Sh': ('GCA_Shots', 1), # need to make per 90
    'GCA Types_Fld': ('GCA_Fouls_drawn', 1), # need to make per 90
    'GCA Types_Def': ('GCA_Defensive_actions', 1), # need to make per 90

    'Tackles_Tkl': ('Tackles_Attempted', 1), # need to make per 90
    'Tackles_TklW': ('Tackles_Won', 1), # need to make per 90 
    'Tackles_Def 3rd': ('Tackles_Def_3rd', 1), # need to make per 90 
    'Tackles_Mid 3rd': ('Tackles_Mid_3rd', 1), # need to make per 90 
    'Tackles_Att 3rd': ('Tackles_Att_3rd', 1), # need to make per 90
    
    'Challenges_Tkl': ('Dribblers_Tackled', 1), # need to make per 90
    'Challenges_Att': ('Dribbles_Contested', 1), # need to make per 90
    'Challenges_Tkl%': ('Dribblers_Tackled%', 0),
    'Challenges_Lost': ('Dribbled_Past', 1), # need to make per 90

    # 'Pressures_Press': ('Pressures', 1), # need to make per 90 
    # 'Pressures_Succ': ('Successful_pressures', 1), # need to make per 90
    # 'Pressures_%': ('Pressures_success%', 0),
    # 'Pressures_Def 3rd': ('Pressures_Def_3rd', 1), # need to make per 90
    # 'Pressures_Mid 3rd': ('Pressures_Mid_3rd', 1), # need to make per 90
    # 'Pressures_Att 3rd': ('Pressures_Att_3rd', 1), # need to make per 90

    'Blocks_Blocks': ('Blocks', 1), # need to make per 90
    'Blocks_Sh': ('Blocks_Shots', 1), # need to make per 90
    # 'Blocks_ShSv': ('Blocks_Shots_on_target', 1), # need to make per 90
    'Blocks_Pass': ('Blocks_Pass', 1), # need to make per 90

    'Int': ('Interceptions', 1), # need to make per 90
    'Tkl+Int': ('Tackles+Interceptions', 1), # need to make per 90
    'Clr': ('Clearances', 1), # need to make per 90
    'Err': ('Mistakes Leading to a Shot', 1), # need to make per 90
    
    'Touches_Touches': ('Touches', 1), # need to make per 90
    'Touches_Def Pen': ('Touches_Def_Pen', 1), # need to make per 90
    'Touches_Def 3rd': ('Touches_Def_3rd', 1), # need to make per 90
    'Touches_Mid 3rd': ('Touches_Mid_3rd', 1), # need to make per 90
    'Touches_Att 3rd': ('Touches_Att_3rd', 1), # need to make per 90
    'Touches_Att Pen': ('Touches_Att_Pen', 1), # need to make per 90
    'Touches_Live': ('Touches_Live', 1), # need to make per 90

    'Take-Ons_Succ': ('Successful dribbles', 1), # need to make per 90
    'Take-Ons_Att': ('Dribbles_Attempted', 1), # need to make per 90
    'Take-Ons_Succ%': ('Dribbles_Success%', 0),
    # 'Take-Ons_#Pl':( '#Players_dribbled_past', 1), # need to make per 90
    # 'Take-Ons_Megs': ('Nutmegs', 1), # need to make per 90
    # TODO(lazy): Add new tackled while dribbling stats

    'Carries_Carries': ('Carries', 1), # need to make per 90
    'Carries_TotDist': ('Carries_TotalDistance', 1), # need to make per 90
    'Carries_PrgDist': ('Carries_ProgressiveDistance', 1), # need to make per 90
    'Carries_PrgC': ('Progressive carries', 1), # need to make per 90
    'Carries_1/3': ('Carries into the final third', 1), # need to make per 90
    'Carries_CPA': ('Carries into the box', 1), # need to make per 90
    'Carries_Mis': ('Miscontrols', 1), # need to make per 90
    'Carries_Dis': ('Dispossessed', 1), # need to make per 90

    # 'Receiving_Targ': ('Pass_Target', 1), # need to make per 90
    'Receiving_Rec': ('Passes_Received', 1), # need to make per 90
    # 'Receiving_Rec%': ('Pass_Receive%', 0),
    'Receiving_PrgR': ('Progressive passes received', 1), # need to make per 90

    'Performance_CrdY': ('Yellow_Cards', 1), # need to make per 90
    'Performance_CrdR': ('Red_Cards', 1), # need to make per 90
    'Performance_2CrdY': ('Second_Yellow_Card', 1), # need to make per 90
    'Performance_Fls': ('Fouls', 1), # need to make per 90
    'Performance_Fld': ('Fouls drawn', 1), # need to make per 90
    'Performance_Off': ('Offsides', 1), # need to make per 90
    'Performance_TklW': ('TacklesWon', 1), # need to make per 90
    'Performance_PKwon': ('PenaltiesWon', 1), # need to make per 90
    'Performance_OG': ('OwnGoals', 1), # need to make per 90

    'Performance_Recov': ('Ball_Recoveries', 1), # need to make per 90

    'Aerial Duels_Won': ('Aerial Duels_Won', 1), # need to make per 90
    'Aerial Duels_Lost': ('Aerial Duels_Lost', 1), # need to make per 90
    'Aerial Duels_Won%': ('Aerial Duels_Won%', 0),
    
    'Poss': ('Possession%', 0)
}

# 'Progressions'  == 'Progressive_passes' + 'Carries_Progressive',
# 'NpxG+xA' = 'NpxG' + 'xA'
# 'NpG+A' = 'npG' + 'Assists'
# 'Turnover' = 'Miscontrols' + 'Dribbles_Attempted' - 'Dribbles_Successful'
# 'TrueTackle' = 'Tackles_Tkl' + 'Performance_Fls' + 'Vs Dribbles_Past'
# 'TrueTackleWin%' = ('Tackles_Tkl' / 'TrueTackle') * 100

# pAdj_mult = 2/(1 + e^(-0.1*(x-50)))

PADJ_COLS = (
    'TrueTackle',
    'Tackles_Attempted',
    'Tackles_Won',
    'Tackles_Def_3rd',
    'Tackles_Mid_3rd',
    'Tackles_Att_3rd',
    # 'Pressures',
    # 'Successful_pressures',
    # 'Pressures_Def_3rd',
    # 'Pressures_Mid_3rd',
    # 'Pressures_Att_3rd',
    'Blocks',
    'Blocks_Shots',
    # 'Blocks_Shots_on_target',
    'Blocks_Pass',
    'Interceptions',
    'Tackles+Interceptions',
    'Clearances',
)

STAT_COLS_MAP_GK = {
    'Performance_GA': ('Goals Against', 1),
    'Performance_SoTA': ('Shots on Target Against', 1),
    'Performance_Saves': ('Saves', 1),
    'Performance_Save%': ('Save %', 0),
    'Performance_CS%': ('Clean Sheet %', 0),

    'Penalty Kicks_PKatt': ('PK Against', 1),
    'Penalty Kicks_PKA': ('PK Allowed', 1),
    'Penalty Kicks_PKsv': ('PK Saved', 1),
    'Penalty Kicks_PKm': ('PK Missed', 1),
    'Penalty Kicks_Save%': ('PK Save %', 0),

    'Goals_FK': ('Free Kick Goals', 1),
    'Goals_CK': ('Corner Kick Goals', 1),
    'Goals_OG': ('Own Goals', 1),

    'Expected_PSxG': ('PSxG', 1),
    'Expected_PSxG/SoT': ('PSxG per Shot on Target', 1),
    'Expected_PSxG+/-': ('PSxG +/-', 1),
    
    'Launched_Cmp': ('Launch Passes Completed', 1),
    'Launched_Att': ('Launch Passes Attempted', 1),
    'Launched_Cmp%': ('Lauch Pass Completion%', 0),

    'Passes_Att': ('Passes Attempted', 1),
    'Passes_Thr': ('Throws Attempted', 1),
    'Passes_Launch%': ('Launch %', 0),
    'Passes_AvgLen': ('Average Pass length (yards)', 0),

    'Goal Kicks_Att': ('Goal Kicks Attempted', 1),
    'Goal Kicks_Launch%': ('Goal Kick Launch%', 0),
    'Goal Kicks_AvgLen': ('Average Goal Kick Length', 0),  
    
    'Crosses_Opp': ('Crosses Against', 1),   
    'Crosses_Stp': ('Crosses Stopped', 1),   
    'Crosses_Stp%' : ('Cross Stop%', 0), 
    
    
    'Sweeper_#OPA': ('Defensive Actions Outside PA', 1),
    'Sweeper_AvgDist': ('Avg. Dist. of Defensive Actions from Goal', 1),
    'Poss': ('Possession%', 0)

}

from typing import Dict, List, Tuple, Union
import pandas as pd
import numpy as np
import structlog

from utils import Singleton

class Scraper:
    CURR_SEASON = '2022-2023'
    logger = structlog.get_logger()

    def __init__(self) -> None:
        ...
    

    def get_players_data(self, season: str) -> pd.DataFrame:
        player_urls, team_urls = self._get_fbref_urls(season)
        cdf = self._get_cdf(player_urls, team_urls)
        # process the data (convert to per 90, rename columns, add new fields)
        cdf = self._process_player_cdf(cdf)
        return cdf

    
    def get_gk_data(self, season: str, players_cdf) -> pd.DataFrame:
        gk_urls, _ = self._get_fbref_gk_urls(season)
        cdf = self._get_cdf(gk_urls)
        cdf = self._process_gk_cdf(cdf)
        cdf = cdf.merge(players_cdf, validate='one_to_one')
        return cdf

    @classmethod
    def _get_cdf(cls, urls: Dict[str, str], team_urls: Dict[str, str]=None):
        # get all the player stats
        dfs = [cls._get_df(url) for url in urls.values()]
        cdf = None
        # merge player stats into a single df
        for df in dfs:
            df.drop(columns=['Rk'], inplace=True)
            cdf = df if cdf is None else cdf.merge(df, validate='one_to_one')
        
        if team_urls is not None:
            # get possession stats for teams (needed for pAdj)
            teamdf = cls._get_df(team_urls['Possession'])
            # keep only the reuqired columns
            teamdf = teamdf[['Squad', 'Comp', 'Poss']]
            cdf = cdf.merge(teamdf, on=['Squad', 'Comp'], validate='many_to_one')
        cdf.sort_values(by=['Comp', 'Squad', 'Player'], inplace=True)

        return cdf

    @classmethod
    def _get_df(cls, url: str, table_num: int=0) -> pd.DataFrame:
        df = pd.read_html(url)
        # generally returns list
        if isinstance(df, List):
            if len(df) <= table_num:
                return None
            df = df[table_num]
        
        # need to fix columns (currently they are tuples)
        print(url)
        cols = df.columns
        # print(cols)
        ncols = []  # to store new columns
        # process col names
        for col in cols:
            ncols.append(cls._process_col_name(col))
        df.columns = ncols

        # col labels (are repeated at some rows in the data)
        labels = [col[1] for col in cols]
        # find rows with column labels
        to_delete = df[df.isin(labels).all(1)].index
        # delete such rows
        df.drop(to_delete, axis=0, inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df
    
    @classmethod
    def _process_col_name(cls, col: Union[Tuple, str]) -> str:
        ncol = col
        if isinstance(col, tuple):
            if col[0].startswith('Unnamed'):
                ncol = col[1]
            else:
                ncol = '_'.join(col)
        return ncol

    @classmethod
    def _process_player_cdf(cls, cdf: pd.DataFrame) -> pd.DataFrame:
        cdf = cdf.apply(pd.to_numeric, errors="ignore")
        # set which will store all the final columns
        column_set = {col for col in TEXT_COLS_MAP.values()}
        # rename all the required text columns
        cdf.rename(columns = TEXT_COLS_MAP, inplace=True)

        stat_map = {}
        for old_name, (new_name, _) in STAT_COLS_MAP.items():
            stat_map[old_name] = new_name
            column_set.add(new_name)
        
        # rename all the stat columns
        cdf.rename(columns = stat_map, inplace=True)

        # normalised some stats to per 90 mins
        for _, (new_name, norm) in STAT_COLS_MAP.items():
            if norm == 1:
                cdf[new_name] = cdf[new_name].astype(float) / cdf['Nineties'].astype(float)
        
        to_drop_cols = [col for col in cdf.columns if col not in column_set]
        cdf.drop(columns=to_drop_cols, inplace=True)

        # more fields
        cdf['Progressions'] = cdf['Progressive passes'] + cdf['Progressive carries']
        cdf['NpxG+xA'] = cdf['Non-penalty xG'] + cdf['xA']
        cdf['NpG+A'] = cdf['Non-penalty goals'] + cdf['Assists']
        
        cdf['Turnover'] = cdf['Miscontrols'] + cdf['Dribbles_Attempted'] - cdf['Successful dribbles']
        
        cdf['TrueTackle'] = cdf['Tackles_Attempted'] + cdf['Fouls drawn'] + cdf['Dribbled_Past']
        cdf['TrueTackleWin%'] = (cdf['Tackles_Attempted'] / cdf['TrueTackle']) * 100

        # get PAdj multiplier for every team
        padj_multiplier = cdf['Possession%'].apply(cls._PAdj_multiplier)

        for col in PADJ_COLS:
            cdf[f'PAdj {col}'] = cdf[col] * padj_multiplier

        return cdf

    @classmethod
    def _process_gk_cdf(cls, cdf: pd.DataFrame) -> pd.DataFrame:

        cdf = cdf.apply(pd.to_numeric, errors="ignore")
        # set which will store all the final columns
        column_set = {col for col in TEXT_COLS_MAP.values()}
        # rename all the required text columns
        cdf.rename(columns = TEXT_COLS_MAP, inplace=True)

        stat_map = {}
        for old_name, (new_name, _) in STAT_COLS_MAP_GK.items():
            stat_map[old_name] = new_name
            column_set.add(new_name)
        
        # rename all the stat columns
        cdf.rename(columns = stat_map, inplace=True)

        # normalised some stats to per 90 mins
        for _, (new_name, norm) in STAT_COLS_MAP_GK.items():
            if norm == 1:
                cdf[new_name] = cdf[new_name].astype(float) / cdf['Nineties'].astype(float)
        
        to_drop_cols = [col for col in cdf.columns if col not in column_set]
        cdf.drop(columns=to_drop_cols, inplace=True)
        
        # more fields
        cdf['GSAA %'] = cdf['PSxG per Shot on Target'] * 100

        return cdf


    @staticmethod
    def _PAdj_multiplier(possession: np.array):
        # scaled sigmoid or shifted tanh (whatever you prefer :CHEEKYSMILE: )
        return 2 / (1 + np.exp(-0.1*(possession-50)))



    @classmethod
    def _get_fbref_urls(cls, season: str) -> Tuple[Dict[str, str], Dict[str, str]]:
        if season != cls.CURR_SEASON:
            fbref_player_urls = {
                'Standard': f'https://fbref.com/en/comps/Big5/{season}/stats/players/{season}-Big-5-European-Leagues-Stats',
                'Shooting': f'https://fbref.com/en/comps/Big5/{season}/shooting/players/{season}-Big-5-European-Leagues-Stats',
                'Passing': f'https://fbref.com/en/comps/Big5/{season}/passing/players/{season}-Big-5-European-Leagues-Stats',
                'Pass_types': f'https://fbref.com/en/comps/Big5/{season}/passing_types/players/{season}-Big-5-European-Leagues-Stats',
                'GCA': f'https://fbref.com/en/comps/Big5/{season}/gca/players/{season}-Big-5-European-Leagues-Stats',
                'Defense': f'https://fbref.com/en/comps/Big5/{season}/defense/players/{season}-Big-5-European-Leagues-Stats',
                'Possession': f'https://fbref.com/en/comps/Big5/{season}/possession/players/{season}-Big-5-European-Leagues-Stats',
                'Misc': f'https://fbref.com/en/comps/Big5/{season}/misc/players/{season}-Big-5-European-Leagues-Stats',
            }
            fbref_team_urls = {
                'Possession': f'https://fbref.com/en/comps/Big5/{season}/possession/squads/{season}-Big-5-European-Leagues-Stats'
            }
        else:
            fbref_player_urls = {
                'Standard': f'https://fbref.com/en/comps/Big5/stats/players/Big-5-European-Leagues-Stats',
                'Shooting': f'https://fbref.com/en/comps/Big5/shooting/players/Big-5-European-Leagues-Stats',
                'Passing': f'https://fbref.com/en/comps/Big5/passing/players/Big-5-European-Leagues-Stats',
                'Pass_types': f'https://fbref.com/en/comps/Big5/passing_types/players/Big-5-European-Leagues-Stats',
                'GCA': f'https://fbref.com/en/comps/Big5/gca/players/Big-5-European-Leagues-Stats',
                'Defense': f'https://fbref.com/en/comps/Big5/defense/players/Big-5-European-Leagues-Stats',
                'Possession': f'https://fbref.com/en/comps/Big5/possession/players/Big-5-European-Leagues-Stats',
                'Misc': f'https://fbref.com/en/comps/Big5/misc/players/Big-5-European-Leagues-Stats',
            }
            fbref_team_urls = {
                
                'Possession': f'https://fbref.com/en/comps/Big5/possession/squads/Big-5-European-Leagues-Stats'
            }

        return (fbref_player_urls, fbref_team_urls)

    @classmethod
    def _get_fbref_gk_urls(cls, season: str) -> Tuple[Dict[str, str], Dict[str, str]]:
        if season != cls.CURR_SEASON:
            fbref_gk_urls = {
                'Goalkeeping': f'https://fbref.com/en/comps/Big5/{season}/keepers/players/{season}-Big-5-European-Leagues-Stats',
                'Advanced_Goalkeeping': f'https://fbref.com/en/comps/Big5/{season}/keepersadv/players/{season}-Big-5-European-Leagues-Stats',
            }
            fbref_team_urls = {
                'Possession': f'https://fbref.com/en/comps/Big5/{season}/possession/squads/{season}-Big-5-European-Leagues-Stats'
            }
        else:
            fbref_gk_urls = {
                'Goalkeeping': f'https://fbref.com/en/comps/Big5/keepers/players/Big-5-European-Leagues-Stats',
                'Advanced_Goalkeeping': f'https://fbref.com/en/comps/Big5/keepersadv/players/Big-5-European-Leagues-Stats',
            }
            fbref_team_urls = {
                'Possession': f'https://fbref.com/en/comps/Big5/possession/squads/Big-5-European-Leagues-Stats'
            }

        return (fbref_gk_urls, fbref_team_urls)
