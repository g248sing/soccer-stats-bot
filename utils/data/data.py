from datetime import timedelta
from io import BufferedIOBase, BytesIO
from pathlib import Path
import threading
from nextcord import client, file

import pandas as pd
import matplotlib.font_manager as fm
from PIL import Image
import structlog

from utils import Singleton
from utils.data import NEGATIVE_COLS
from utils.data.scraper import Scraper
from utils.sharefile import ShareFile


pd.options.mode.chained_assignment = None
pd.set_option('display.max_columns', None)

BASE_PATH = Path('./data/')
BASE_STATIC_PATH = Path('./data_static')

# fonts used for plotting
FONT_DIR = BASE_STATIC_PATH.joinpath('fonts')
FONTS = ['slabo.ttf', 'spectral.ttf', 'spacegrotesk.ttf',
         'rubik.ttf', 'robotoslab.ttf', 'neuton.ttf']

# Fbref and Statsbomb logos for citing
_FBREF_LOGO_PATH =  BASE_STATIC_PATH.joinpath('img/fb-logo.png')
_SB_LOGO_PATH = BASE_STATIC_PATH.joinpath('img/SB_Regular_Alt.png')
_FCD_QR_PATH = BASE_STATIC_PATH.joinpath('img/fcd-qr.png')

FBREF_LOGO = Image.open(ShareFile.download_static(_FBREF_LOGO_PATH))
SB_LOGO = Image.open(ShareFile.download_static(_SB_LOGO_PATH))
FCD_QR = Image.open(ShareFile.download_static(_FCD_QR_PATH))

log = structlog.get_logger(__name__)

class _PlayersData(metaclass=Singleton):
    SEASONS = ['2017-2018', '2018-2019','2019-2020', '2020-2021', '2021-2022', '2022-2023']
    CURR_SEASON = '2022-2023'

    def __init__(self) -> None:
        # load fonts
        for font in FONTS:
            font_path = FONT_DIR.joinpath(font)
            try:
                ShareFile.download_static(font_path)
                if font_path.exists():
                    fm.fontManager.addfont(str(font_path))
            except Exception as e:
                log.error(f"Can't load font: {font}. Error: {e}")
        
        # contains full data for every seasons
        self.datas = {}
        self.gk_datas = {}
        for season in self.SEASONS:
            data_path = BASE_PATH.joinpath(f'df{season}.csv')
            gk_data_path = BASE_PATH.joinpath(f'df{season}_gk.csv')
            df = self._read_data(data_path)
            df_gk = self._read_data(gk_data_path)
            self.datas[season] = df
            self.gk_datas[season] = df_gk
        

        
    def _read_data(self, data_path: Path):
        df = None
        try:
            # [get From Cloud]
            data_buff = ShareFile.get_file_client(data_path).read()
            df = pd.read_csv(data_buff , encoding='utf-8')
        except Exception as e:
            log.error(f"Can't load {data_path}", exc_info=e)
            df = None
        return df

    def _process_player_df(self, df: pd.DataFrame) -> pd.DataFrame:
        if df['Age'].dtype == 'str':
                df['Age'].apply(self._clean_age, convertDType=True)

        # save these permanently in data? current season table would be dynamic
        df['True Interceptions'] = df['Interceptions'] + df['Blocks_Pass']
        df['PAdj True Interceptions'] = df['PAdj Interceptions'] + df['PAdj Blocks_Pass']
        df['PAdj True Tackles+Interceptions'] = df['PAdj TrueTackle'] + df['PAdj True Interceptions']

        # df = df.rename(columns={
        #     '90s': 'Nineties',
        #     'NpxG' : 'Non-penalty xG',
        #     'npG' : 'Non-penalty goals',
        #     'Progressive_passes' : 'Progressive passes',
        #     'Passes_into_finalthird' : 'Passes into final third',
        #     'Passes_into_box' : 'Passes into box',
        #     'SCA' : 'Shot-creating actions',
        #     'Dribbles_Successful' : 'Successful dribbles',
        #     'Carries_Progressive' : 'Progressive carries',
        #     'Carries_into_final3rd' : 'Carries into the final third',
        #     'Carries_into_box' : 'Carries into the box',
        #     'Progressive_Passes_Received' : 'Progressive passes received',
        #     'Fouled' : 'Fouls drawn'
        # })

        return df
    
    def _process_gk_df(self, df: pd.DataFrame) -> pd.DataFrame:
        if df['Age'].dtype == 'str':
                df['Age'].apply(self._clean_age, convertDType=True)
        return df
    
    def _clean_age(self, age: str):
        # it's year-days in recent data so only keep the year
        return int(age.split('-')[0])

    def get_player_data(self, season: str, idx: int):
        if season not in self.SEASONS:
            raise ValueError(
                f'No season data named {season}', 
                f'choose from {self.SEASONS}')
        df = self.datas[season]
        if idx >= len(df):
            raise ValueError(f'idx should be in {0}-{len(df)-1}')
        return df[idx, :].copy()
        
    def get_players_data(self, season: str):
        if season not in self.SEASONS:
            raise ValueError(
                f'No season data named {season}', 
                f'choose from {self.SEASONS}')
        return self.datas[season].copy()
    
    def get_gk_data(self, season: str):
        if season not in self.SEASONS:
            raise ValueError(
                f'No season data named {season}', 
                f'choose from {self.SEASONS}')
        return self.gk_datas[season].copy()
    
    @staticmethod
    def compute_percentiles(df: pd.DataFrame, cols):
        """
        NOTE: Modifies the input dataframe, doesn't create a copy
        """
        for col in cols:
            if col in NEGATIVE_COLS:
                df[f'_Percentile_{col}'] = 100-df[col].rank(pct=True)*100
            else:
                df[f'_Percentile_{col}'] = df[col].rank(pct=True)*100
        return df
    
    def scrape_data(self, season):
        # TODO: Log this
        print(f'Scraping data...')
        sc = Scraper()
        df = self._process_player_df(sc.get_players_data(season))
        gk_df = self._process_gk_df(sc.get_gk_data(season, df))
        
        buffer = BytesIO()
        df.to_csv(buffer, encoding='utf-8')
        buffer.seek(0)
        data_path = BASE_PATH.joinpath(f'df{season}.csv')

        try:
            ShareFile.get_file_client(data_path).write(buffer.read())
        except Exception as e:
            # TODO: Log
            log(f"Can't write scaped data to {data_path}", exc_info=e)

        buffer_gk = BytesIO()
        gk_df.to_csv(buffer_gk, encoding='utf-8')
        buffer_gk.seek(0)
        gk_data_path = BASE_PATH.joinpath(f'df{season}_gk.csv')
        
        try:
            ShareFile.get_file_client(gk_data_path).write(buffer_gk.read())
        except:
            # TODO: Log
            print(f"Can't write scaped data to {gk_data_path}")
        
        print(f'Scraping data for season {season} completed!')
        self.datas[season] = df
        self.gk_datas[season] = gk_df

PlayersData = _PlayersData()

def setup(bot):
    pass
